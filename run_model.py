import sys
import os
import click

sys.path.insert(1, os.getcwd() + '/cqm')

from load_data import DataLoader
from single_period_cqm import SinglePeriodCQM

@click.command()
@click.option('-b', '--budget', default = 10000, show_default = True, help = 'Specifies the budget you wish to use for your portfolio.')
@click.option('-l', '--lowerbound', default = 0.98, show_default = True,
            help = 'A decimal value between 0 and 1 that represents the lower bound on the percentage of the budget that can be spent.')
@click.option('-v', '--verbose', default = False, is_flag = True)

def main(budget, lowerbound, verbose):
    print("\nStarting model...\n")
    modelData = DataLoader('data/basic_data.csv', budget, lowerbound, verbose)
    if not os.path.exists('API_key.txt'):
        raise Exception("No API_key.txt file found.")
    with open('API_key.txt') as file:
        token = file.readline()
    model = SinglePeriodCQM(modelData, token)
    model.run()
    

if __name__ == '__main__':
    main()