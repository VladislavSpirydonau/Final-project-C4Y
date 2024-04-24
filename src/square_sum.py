import pandas as pd
from src import converting

def square_sum(df, sql_query, conn):
    """
    Calculates the square sum of the differences in balances for each client and merges it with the provided DataFrame.

    Parameters:
    - df: DataFrame, the input DataFrame to which the result will be merged
    - sql_query: str, SQL query to fetch data from the database
    - conn: database connection object

    Returns:
    - df: DataFrame, the input DataFrame merged with the calculated square sum of balance differences
    """
    # Fetch balance values from the database using the provided SQL query
    dif_bal = pd.read_sql_query(sql_query, conn)
    
    # Convert currency to CZK
    dif_bal = converting.converter(dif_bal)
    
    # Calculate the difference in balances for each client and square it
    dif_bal['balance_diff'] = dif_bal.groupby('client_id')['balance'].diff().fillna(0)
    dif_bal['balance_diff_square_sum'] = dif_bal.groupby('client_id')['balance_diff'].transform(lambda x: (x ** 2).sum())
    
    # Select relevant columns
    dif_bal = dif_bal[['client_id', 'balance_diff_square_sum']]
    
    # Merge the calculated square sum with the input DataFrame
    df = df.merge(dif_bal.drop_duplicates(subset=['client_id']), on='client_id', how='left')
    
    return df