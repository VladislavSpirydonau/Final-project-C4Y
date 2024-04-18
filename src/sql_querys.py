query_age_model = ('''
WITH mean_deposite as (
    select 
         client_id,
         AVG(balance) as mean_balance,
         MAX(balance) as max_balance,
         MIN(balance) as min_balance,
         MAX(balance)-MIN(balance) as dif_balance,
         currency
    from balances
    group by 1
)
Select * 
from client
left join client_products
on client.client_id = client_products.client_id
left join mean_deposite
on client.client_id = mean_deposite.client_id''')


query_training_model = ('''
WITH max_deposite as (
    select 
         client_id,
         MAX(balance) as max_balance,
         currency
    from balances
    group by 1
)
Select * 
from inv_campaign_eval
left join client
on inv_campaign_eval.client_id = client.client_id
left join client_products
on inv_campaign_eval.client_id = client_products.client_id
left join max_deposite
on inv_campaign_eval.client_id = max_deposite.client_id''')

query_square_sum = ('''
Select * 
from inv_campaign_eval
left join balances
on inv_campaign_eval.client_id = balances.client_id''')
