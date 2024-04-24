import sqlite3
import pandas as pd
from src import paths, sql_querys, converting, pipelines, split
import joblib

# Establish database connection
conn = sqlite3.connect(paths.db_path)
cursor = conn.cursor()

# Fetch data from the database
query = sql_querys.query_age_model
df = pd.read_sql_query(query, conn)

# Convert max_balance to numeric
df['max_balance'] = pd.to_numeric(df['max_balance'])

# Convert currency to CZK (Czech Koruna) if necessary
df = converting.converter(df)

# Drop rows with missing values in the 'age' column
df = df.dropna(subset=['age'], how='any')

# Prepare data for modeling
target_column = 'age'
X_train, X_test, y_train, y_test = split.split(df, target_column=target_column)

# Define parameters for GradientBoostingRegressor
GBR_params = {'learning_rate': 0.05, 'loss': 'huber', 'max_depth': 8, 'max_features': 'sqrt',
              'min_samples_leaf': 10, 'min_samples_split': 10, 'n_estimators': 129}

# Define features for the pipeline
num_features = ['max_balance']
cat_features = ['job']
labeled_features = ['marital', 'education', 'gender', 'has_deposits', 'loan', 'has_insurance', 'has_mortgage']

# Create and train the pipeline
pipeline = pipelines.age_pipeline(num_features=num_features, cat_features=cat_features,
                                   labeled_features=labeled_features, GBR_params=GBR_params)
pipeline.fit(X_train, y_train)

# Save the trained pipeline to a file
joblib.dump(pipeline, paths.age_pipeline_path)