import sqlite3
import pandas as pd
from src import paths,sql_querys,converting, pipelines, square_sum
import joblib
from sklearn.preprocessing import LabelEncoder

# 1. Creating a dataset from database and cleaning the data
conn = sqlite3.connect(paths.db_path)
cursor = conn.cursor()
query = sql_querys.query_training_model
df = pd.read_sql_query(query, conn)

df.max_balance = pd.to_numeric(df.max_balance)
df.age=pd.to_numeric(df.age)

# 2. Converting balances to CZK
df = converting.converter(df)

# 3. Filling missing values
age_pipeline = joblib.load(paths.age_pipeline_path)
missing_age_indices = df['age'].isnull()
predicted_ages = age_pipeline.predict(df[missing_age_indices])
df.loc[missing_age_indices, 'age'] = predicted_ages

# 4. Creating new feature 
query1 = (sql_querys.query_square_sum)
df = square_sum.square_sum(df,query1,conn)

# 5. Creating training data
y = df.poutcome
X = df.drop(columns = 'poutcome')
enc = LabelEncoder()
y=enc.fit_transform(y)

# 6.Pipeine
# 6.1 Preparing parametrs for pipeline function
num_features = ['age', 'balance_diff_square_sum', 'max_balance']
labeled_features = ['has_deposits', 'loan', 'has_mortgage','education' ]
RFC_params = {'random_state':42, 'n_estimators': 150, 'min_samples_split': 10,
                                            'min_samples_leaf':2, 'max_features': 'sqrt', 'max_depth': 10, 'criterion':'entropy', 'bootstrap': False}
# 6.2 calling the pipeline function
pipeline = pipelines.main_pipeline(num_features,labeled_features,RFC_params)

# 7. Training and saving the pipeline
#7.1. I test the model before and now how it perform so for actualy training the model for further predictions I can use every data I have
pipeline.fit(X, y)
#7.2. saving my pipeline 
joblib.dump(pipeline, paths.final_pipeline_path)
