import pandas as pd

class DataLoader:
    def __init__(self, filepath, budget, budgetThreshold, verbose):
        print("Loading stock data from file: ", filepath)
        self.settings = {"isVerbose" : verbose}
        self.filepath = filepath
        self.budget = budget

        if budgetThreshold is None:
            self.budgetThreshold = 0.96 
        else:
            self.budgetThreshold = budgetThreshold

        self.dataframe = pd.read_csv(filepath, index_col=0)
        stocks = []
        for col in self.dataframe:
            stocks.append(col)
        self.stocks = stocks

        self.initialHoldings = {stock : 0 for stock in self.stocks}

        self.maxShares = (self.budget / self.dataframe.iloc[1]).astype(int)

        self.price = self.dataframe.iloc[0]

        self.monthlyReturns = self.dataframe[list(self.stocks)].pct_change().iloc[1:]

        self.averageMonthlyReturns = self.monthlyReturns.mean(axis=0)

        self.covarianceMatrix = self.monthlyReturns.cov()

        if self.settings["isVerbose"]:
            print(f"\nData loaded:")
            print(f"Running model with {len(stocks)} available stocks: ",stocks)
            print(f"Max number of holdings: ", self.maxShares)
