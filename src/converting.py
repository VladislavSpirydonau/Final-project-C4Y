import pandas as pd
# function for converting currency rates in data frame
def converter(df, rate={'CZK': 1, 'USD': 23, 'EUR': 25}):
   
    # Select columns with balance parameters
    balance_cols = [col for col in df.columns if 'balance' in col]
    
    # Convert each balance to the rate of its currency
    for col in balance_cols:
        df[col] = df.apply(lambda row: row[col] * rate[row['currency']], axis=1)
    
    return df