import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    data_path = os.path.join(BASE_DIR,  'training' '/train_and_test2.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The file {data_path} does not exist.")
    
    data = pd.read_csv(data_path)
    data.columns = data.columns.str.strip().str.lower()

    required_columns = ['age', 'fare', 'sex', 'sibsp', 'parch', 'pclass', 'embarked', '2urvived']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for col in ['age', 'fare']:
        data[col].fillna(data[col].median())

    for col in ['sex', 'embarked']:
        data[col].fillna(data[col].mode()[0])

    label_encoder = LabelEncoder()
    data['sex'] = label_encoder.fit_transform(data['sex'])
    data['embarked'] = label_encoder.fit_transform(data['embarked'])

    columns_to_use = ['age', 'fare', 'sex', 'sibsp', 'parch', 'pclass', 'embarked']
    X = data[columns_to_use]
    y = data['2urvived']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(C=0.5, random_state=42, max_iter=200, solver='lbfgs')
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")

    model_path = os.path.join(BASE_DIR, 'predictions', 'models', 'titanic_model.pkl')
    scaler_path = os.path.join(BASE_DIR, 'predictions', 'models', 'scaler.pkl')
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved at {model_path}")
    print(f"Scaler saved at {scaler_path}")

except Exception as e:
    print(f"Error during training: {e}")
