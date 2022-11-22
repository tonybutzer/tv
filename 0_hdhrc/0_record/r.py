# Import the library
import argparse
# Create the parser
import pandas as pd

def get_channel_df(csvfile):
    df = pd.read_csv('channels.csv')
    return df

