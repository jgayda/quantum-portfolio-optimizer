import sys
import os

sys.path.insert(1, os.getcwd() + '/cqm')

from load_data import DataLoader
from single_period_cqm import SinglePeriod

def main():
    print("\nHello world.")
    modelData = DataLoader('data/sample-data.csv', 10000)
    model = SinglePeriod(modelData)
    model.run()
    

if __name__ == '__main__':
    main()