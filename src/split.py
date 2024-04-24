from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def split(df, target_column, test_size=0.2, random_state=42):
    """
    Splits the dataframe into features (X) and target variable (y), and further splits them into training and testing sets.

    Parameters:
    - df: DataFrame, the input data
    - target_column: str, the name of the target column
    - test_size: float, optional, default=0.2, the proportion of the dataset to include in the test split
    - random_state: int, optional, default=42, controls the randomness of the split

    """
    # Separate features (X) and target variable (y)
    y = df[target_column]
    X = df.drop(columns=target_column)
    
    # Encode the target variable using LabelEncoder
    enc = LabelEncoder()
    y = enc.fit_transform(y)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test
