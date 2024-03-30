import os
parent_dir = os.path.dirname(os.path.dirname(__file__))
csv_filename = "client_ids.csv"
client_csv_path = os.path.join(parent_dir, csv_filename)
db_filename = 'data.db'
db_path = os.path.join(parent_dir, db_filename)

