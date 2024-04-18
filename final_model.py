import sqlite3
import pandas as pd
from src import paths,sql_querys,converting
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, recall_score
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

# 1. Creating a dataset from database and cleaning the data
conn = sqlite3.connect(paths.db_path)
cursor = conn.cursor()
query = sql_querys.query_training_model
df = pd.read_sql_query(query, conn)
df = df.loc[:,~df.columns.duplicated()]
df.max_balance = pd.to_numeric(df.max_balance)
df.age=pd.to_numeric(df.age)
# 2. Converting balances to CZK
rate = {'CZK': 1, 'USD': 23, 'EUR': 25}
df = converting.converter(df, rate)
# 3. Filling missing values
age_pipeline = joblib.load(paths.age_pipeline_path)
missing_age_indices = df['age'].isnull()
predicted_ages = age_pipeline.predict(df[missing_age_indices])
df.loc[missing_age_indices, 'age'] = predicted_ages
# 4. Creating new feature 
query1 = (sql_querys.query_square_sum)
dif_bal = pd.read_sql_query(query1, conn)
dif_bal = dif_bal.loc[:,~dif_bal.columns.duplicated()]
dif_bal = converting.converter(dif_bal, rate)
dif_bal['balance_diff'] = dif_bal.groupby('client_id')['balance'].diff().fillna(0)
dif_bal['balance_diff_square_sum'] = dif_bal.groupby('client_id')['balance_diff'].transform(lambda x: (x ** 2).sum())
dif_bal.drop(columns=['date', 'balance', 'balance_diff', 'poutcome', 'currency'], inplace=True)
df = df.merge(dif_bal.drop_duplicates(subset=['client_id']), on='client_id', how='left')
# 5. Creating training data
y = df.poutcome
X = df.drop(columns = 'poutcome')
enc = LabelEncoder()
y=enc.fit_transform(y)
# 6. Pipeline
num_features = ['age', 'balance_diff_square_sum', 'max_balance']
labeled_features = ['has_deposits', 'loan', 'has_mortgage','education' ]

# 6.1. Create transformers for the numerical and categorical features
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

labeled_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='no')),
    ('label', OrdinalEncoder())])

# 6.2. Create a column transformer to apply the transformations to the respective columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_features),
        ('label', labeled_transformer, labeled_features)
            ])

# 6.3. Full pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, n_estimators= 150, min_samples_split= 10, min_samples_leaf= 2, max_features= 'sqrt', max_depth= 10, criterion= 'entropy', bootstrap= False))])
# 7. Training and saving the pipeline
#7.1. I test the model before and now how it perform so for actualy training the model for further predictions I can use every data I have
pipeline.fit(X, y)
#7.2. saving my pipeline 
joblib.dump(pipeline, paths.final_pipeline_path)