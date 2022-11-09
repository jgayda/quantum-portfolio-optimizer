import csv
import pandas as pd

class DataLoader:
    def __init__(self, filepath, budget):
        print("Loading data from file: ", filepath)
        self.filepath = filepath
        self.budget = budget

        self.dataframe = pd.read_csv(filepath, index_col=0)
        stockTickers = []
        for col in self.dataframe:
            stockTickers.append(col)
        self.stockTickers = stockTickers

        self.initialHoldings = {s : 0 for s in self.stockTickers}

        self.maxShares = (self.budget / self.dataframe.iloc[1]).astype(int)

        self.price = self.dataframe.iloc[0]

        self.monthlyReturns = self.dataframe[list(self.stockTickers)].pct_change().iloc[1:]

        self.averageMonthlyReturns = self.monthlyReturns.mean(axis=0)

        self.covarianceMatrix = self.monthlyReturns.cov()
