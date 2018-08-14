#!/usr/bin/python3

"""This script will execute the scraper.js,
    after that is going to process the data for later consuption"""

import os
import json
import datetime
import pandas as pd
from Naked.toolshed.shell import execute_js

# scraper.js execution
success_scraper = execute_js('scrape.js')
if success_scraper:
    success_combine = execute_js('combine.js')
    if not success_combine:
        print('Error executing combine.js')
        raise Error('combine.js')
else:
    print('Error executing scrape.js')
    raise Error('scrape.js')


def dt_func(seconds):
    return datetime.datetime.utcfromtimestamp(seconds)


the_path = os.getcwd()
data_path = the_path + '../data/'
file_name = 'bitcoin-history.json'
file_path = data_path + file_name
with open(file_path, 'r') as handle:
    parsed = json.load(handle)

df = pd.DataFrame(columns=['Timestamp', 'Open', 'High', 'Low', 'Close',
                           'Volume (BTC)', 'Volume (Currency)', 'Weighted Price (USD)'], data=parsed)

df['Timestamp'] = df['Timestamp'].map(lambda x: dt_func(x))

df['Average'] = (df['High']+df['Low'])/2
df['Date'] = pd.to_datetime(df['Timestamp'])

with pd.option_context('mode.use_inf_as_null', True):
    df.loc[df.isnull().any(axis=1), 1:9] = np.nan
    df.fillna(method='pad', inplace=True)

new_df = df[['Date', 'Average']].copy()
new_df.to_csv(data_path + 'processed-data/processed.csv')