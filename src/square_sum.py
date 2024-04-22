import pandas as pd 
from src import converting

def square_sum(df,sql_query,conn):
    dif_bal = pd.read_sql_query(sql_query, conn)
    
    dif_bal = converting.converter(dif_bal)
    dif_bal['balance_diff'] = dif_bal.groupby('client_id')['balance'].diff().fillna(0)
    dif_bal['balance_diff_square_sum'] = dif_bal.groupby('client_id')['balance_diff'].transform(lambda x: (x ** 2).sum())
    dif_bal = dif_bal[['client_id', 'balance_diff_square_sum']]
    df = df.merge(dif_bal.drop_duplicates(subset=['client_id']), on='client_id', how='left')
    return df