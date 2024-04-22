query_age_model = ('''
WITH mean_deposite as (
    select 
         client_id,
         MAX(balance) as max_balance,
         currency
    from balances
    group by 1
)
SELECT 
    client.client_id,
    client.age,
    client.job,
    client.marital,
    client.education,
    client.gender,
    client_products.has_deposits,
    client_products.loan,
    client_products.has_insurance,
    client_products.has_mortgage,
    mean_deposite.max_balance,
    mean_deposite.currency
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
SELECT 
    inv_campaign_eval.client_id,
    inv_campaign_eval.poutcome,
    client.age,
    client.job,
    client.marital,
    client.education,
    client.gender,
    client_products.has_deposits,
    client_products.loan,
    client_products.has_insurance,
    client_products.has_mortgage,
    max_deposite.max_balance,
    max_deposite.currency
from inv_campaign_eval
left join client
on inv_campaign_eval.client_id = client.client_id
left join client_products
on inv_campaign_eval.client_id = client_products.client_id
left join max_deposite
on inv_campaign_eval.client_id = max_deposite.client_id''')



query_square_sum_ev = ('''
Select
    balances.date, 
    balances.client_id,
    balances.balance,
    balances.currency
from balances
left join inv_campaign_eval
    on balances.client_id = inv_campaign_eval.client_id
WHERE inv_campaign_eval.client_id is null; ''')

query_square_sum_train = ('''
Select 
    balances.date,                     
    balances.client_id,
    balances.balance,                      
    balances.currency 
from inv_campaign_eval
left join balances
    on inv_campaign_eval.client_id = balances.client_id''')

query_square_sum = ('''
Select * 
from inv_campaign_eval
left join balances
on inv_campaign_eval.client_id = balances.client_id''')


query_evaluation = ('''WITH mean_deposite AS (
    SELECT 
        client_id,
        MAX(balance) AS max_balance,
        currency
    FROM balances
    GROUP BY client_id
)
SELECT 
    client.client_id,
    client.age,
    client.job,
    client.marital,
    client.education,
    client.gender,
    client_products.has_deposits,
    client_products.loan,
    client_products.has_insurance,
    client_products.has_mortgage,
    mean_deposite.max_balance,
    mean_deposite.currency
FROM client
LEFT JOIN inv_campaign_eval ON client.client_id = inv_campaign_eval.client_id
LEFT JOIN client_products ON client.client_id = client_products.client_id
LEFT JOIN mean_deposite ON client.client_id = mean_deposite.client_id
WHERE inv_campaign_eval.client_id IS NULL;''')


