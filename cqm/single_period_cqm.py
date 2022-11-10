from dimod import ConstrainedQuadraticModel
from dimod import Integer
from dimod import quicksum

from dwave.system import LeapHybridCQMSampler

from itertools import product

class SinglePeriodCQM:
    def __init__(self, data, token):
        self.data = data
        self.sampleSet = {}
        self.samplerArgs = {}
        self.sampler = LeapHybridCQMSampler(**self.samplerArgs, token=token)
        self.solution = {}
    
    def build_cqm(self):
        cqm = ConstrainedQuadraticModel()
        data = self.data
        # Add each individual stock as a variable to the model
        x = {stock: Integer("%s" %stock, lower_bound = 0, upper_bound = data.maxShares[stock]) for stock in data.stocks}

        risk = 0
        for stock1, stock2 in product(data.stocks, data.stocks):
            riskCoefficient = data.covarianceMatrix[stock1][stock2] * data.price[stock1] * data.price[stock2]
            risk = risk + riskCoefficient * x[stock1] * x[stock2]
        
        returns = 0
        for stock in data.stocks:
            returns = returns + data.price[stock] * data.averageMonthlyReturns[stock] * x[stock]

        cqm.add_constraint(quicksum([x[stock] * data.price[stock] for stock in data.stocks]) <= data.budget, label = 'upper_budget')
        cqm.add_constraint(quicksum([x[stock] * data.price[stock] for stock in data.stocks]) >= data.budgetThreshold * data.budget, label = 'lower_budget')
        cqm.add_constraint(risk <= 0.0, label='max_risk')

        cqm.set_objective(-1 * returns)

        cqm.substitute_self_loops()

        self.model = cqm

    def getReturns(self, solution):
        returns = 0
        data = self.data
        for stock in solution:
            returns = returns + solution[stock] * data.price[stock] * data.averageMonthlyReturns[stock]
        return returns

    def getRisk(self, solution):
        variance = 0.0
        data = self.data
        for stock1, stock2 in product(solution, solution):
            variance = variance + (solution[stock1] * data.price[stock1] * solution[stock2] * data.price[stock2] * data.covarianceMatrix[stock1][stock2])
        return variance

    def solve_cqm(self):
        data = self.data
        self.sampleSet = self.sampler.sample_cqm(self.model, label="Portfolio Optimization")
        numSamples = len(self.sampleSet.record)
        feasibleSamples = self.sampleSet.filter(lambda d: d.is_feasible)

        if not feasibleSamples:
            raise Exception("No feasible solution could be found for this portfolio")
        else:
            bestFeasible = feasibleSamples.first

            solution = {}

            solution['stocks'] = {stock : int(bestFeasible.sample[stock]) for stock in data.stocks}
            solution['returns'] = self.getReturns(solution['stocks'])
            solution['risk'] = self.getRisk(solution['stocks'])

            cost = sum([data.price[stock] * max(0, solution['stocks'][stock] - data.initialHoldings[stock]) for stock in data.stocks])
            sales = sum([data.price[stock] * max(0, data.initialHoldings[stock] - solution['stocks'][stock]) for stock in data.stocks])

            print(f'Number of feasible solutions found: {len(feasibleSamples)} out of {numSamples} samples')
            print(f'\nBest energy: {self.sampleSet.first.energy: .3f}')
            print(f'\nBest feasible energy: {bestFeasible.energy: .3f}')
            print(f'\n\nOptimized Portfolio Below:')
            print("\n".join("{}\t{:>3}".format(key, value) for key, value in solution['stocks'].items()))
            print(f"\n\nEstimated Returns: {solution['returns']}")
            print(f"\nSales Revenue: {sales:.2f}")
            print(f"\nPuchase Cost: {cost:.2f}")
            print(f"\nRisk (Variance): {solution['risk']:.2f}")

            return solution

    def run(self):
        self.build_cqm()
        self.solution = self.solve_cqm()
