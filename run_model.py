import sys
import os

from dwave.cloud import Client

sys.path.insert(1, os.getcwd() + '/cqm')

from load_data import DataLoader
from single_period_cqm import SinglePeriod

def main():
    print("\nHello world.")
    client = Client.from_config(config_file = 'config.conf')
    modelData = DataLoader('data/sample-data.csv', 10000)
    with open('API_key.txt') as file:
        token = file.readline()
    model = SinglePeriod(modelData, token)
    model.run()
    client.close()
    

if __name__ == '__main__':
    main()