import sys
import os

sys.path.insert(1, os.getcwd() + '/cqm')

from load_data import DataLoader
from single_period_cqm import SinglePeriodCQM

def main():
    print("\nStarting model...\n")
    modelData = DataLoader('data/sample-data.csv', 10000)
    with open('API_key.txt') as file:
        token = file.readline()
    model = SinglePeriodCQM(modelData, token)
    model.run()
    

if __name__ == '__main__':
    main()