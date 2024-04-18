import pandas as pd

def converter(df, rate):
   
    # Select columns with balance parameters
    balance_cols = [col for col in df.columns if 'balance' in col]
    
    # Convert each balance to the rate of its currency
    for col in balance_cols:
        df[col] = df.apply(lambda row: row[col] * rate[row['currency']], axis=1)
    
    return df