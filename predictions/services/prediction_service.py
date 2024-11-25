import pandas as pd
from sklearn.preprocessing import LabelEncoder
from io import BytesIO
from sklearn.exceptions import NotFittedError

class PredictionService:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler

    def process_file(self, file):
        try:
            data = pd.read_excel(file)

            data.columns = data.columns.str.strip().str.lower()

            required_columns = ['age', 'fare', 'sex', 'sibsp', 'parch', 'pclass', 'embarked']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            for col in ['age', 'fare']:
                data[col] = data[col].fillna(data[col].median())
            for col in ['sex', 'embarked']:
                data[col] = data[col].fillna(data[col].mode()[0])

            label_encoder_sex = LabelEncoder()
            label_encoder_embarked = LabelEncoder()
            data['sex'] = label_encoder_sex.fit_transform(data['sex'])
            data['embarked'] = label_encoder_embarked.fit_transform(data['embarked'])

            X = self.scaler.transform(data[required_columns])

            predictions = self.model.predict(X)
            data['predictions'] = predictions

            return data

        except NotFittedError:
            raise ValueError("The model is not properly trained.")
        except Exception as e:
            raise ValueError(f"Error processing the file: {e}")

    def save_to_excel(self, data):
        """Save results to an Excel file."""
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
        output.seek(0)
        return output
