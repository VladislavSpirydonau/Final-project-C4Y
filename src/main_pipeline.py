from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

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