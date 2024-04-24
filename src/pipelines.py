from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder

# Main pipeline for classification
def main_pipeline(num_features, labeled_features, RFC_params):
    """
    Construct a main pipeline for classification tasks.

    Parameters:
    num_features (list): List of numerical feature names.
    labeled_features (list): List of categorical feature names.
    RFC_params (dict): Parameters for Random Forest Classifier.

    Returns:
    pipeline (Pipeline): Constructed pipeline for classification.
    """
    # Create transformers for the numerical and categorical features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),  # Impute missing values with median
        ('scaler', StandardScaler())])  # Scale numerical features

    labeled_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='no')),  # Impute missing values with 'no'
        ('label', OrdinalEncoder())])  # Encode categorical features

    # Create a column transformer to apply the transformations to the respective columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('label', labeled_transformer, labeled_features)
        ])

    # Construct the full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),  # Preprocess data
        ('classifier', RandomForestClassifier(**RFC_params))])  # Apply Random Forest Classifier
    return pipeline

# Pipeline for regression based on age
def age_pipeline(num_features, labeled_features, cat_features, GBR_params):
    """
    Construct a pipeline for regression based on age.

    Parameters:
    num_features (list): List of numerical feature names.
    labeled_features (list): List of categorical feature names.
    cat_features (list): List of categorical feature names.
    GBR_params (dict): Parameters for Gradient Boosting Regressor.

    Returns:
    pipeline (Pipeline): Constructed pipeline for regression.
    """
    # Define transformers for numerical and categorical features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),  # Impute missing values with median
        ('scaler', StandardScaler())])  # Scale numerical features

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),  # Impute missing values with 'unknown'
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])  # One-hot encode categorical features

    labeled_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='no')),  # Impute missing values with 'no'
        ('label', OrdinalEncoder())])  # Encode categorical features

    # Create a column transformer to apply the transformations to the respective columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features),
            ('label', labeled_transformer, labeled_features)
        ])

    # Construct the full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),  # Preprocess data
        ('regressor', GradientBoostingRegressor(**GBR_params))])  # Apply Gradient Boosting Regressor
    return pipeline