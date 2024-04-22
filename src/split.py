from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def split(df, target_column, test_size=0.2, random_state=42):
    y = df[target_column]
    X = df.drop(columns = target_column)
    enc = LabelEncoder()
    y=enc.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

