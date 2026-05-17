import joblib
import pandas as pd

model = joblib.load("models/churn_model.pkl")

model_columns = joblib.load(
    "models/model_columns.pkl"
)


def predict_churn(data):

    input_df = pd.DataFrame([data])

    # Add missing columns
    for col in model_columns:

        if col not in input_df.columns:
            input_df[col] = 0

    # Ensure column order
    input_df = input_df[model_columns]

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }