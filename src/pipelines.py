from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor

# Main pipeline
def main_pipeline(num_features, labeled_features, RFC_params):
   # Create transformers for the numerical and categorical features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    labeled_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='no')),
        ('label', OrdinalEncoder())])

    # Create a column transformer to apply the transformations to the respective columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('label', labeled_transformer, labeled_features)
                ])

    # Full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(**RFC_params))])
    return pipeline

# Pipeline for age
def age_pipeline(num_features, labeled_features, cat_features, GBR_params):
    numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    labeled_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='no')),
        ('label', OrdinalEncoder())])


    # Create a column transformer to apply the transformations to the respective columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features),
            ('label', labeled_transformer, labeled_features)
                ])

    # Full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingRegressor(**GBR_params))])
    return pipeline