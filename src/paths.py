import os
parent_dir = os.path.dirname(os.path.dirname(__file__))

csv_filename = "client_ids.csv"
client_csv_path = os.path.join(parent_dir,'data', csv_filename)

db_filename = 'data.db'
db_path = os.path.join(parent_dir, 'data', db_filename)

age_pipeline_file = 'age_pipeline.pkl'
age_pipeline_path = os.path.join(parent_dir, 'pipelines', age_pipeline_file)

final_pipeline_file = 'pipeline_simplified.pkl'
final_pipeline_path = os.path.join(parent_dir, 'pipelines', final_pipeline_file)