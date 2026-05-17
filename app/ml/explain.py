import shap
import joblib

model = joblib.load("models/churn_model.pkl")

def explain_prediction(X):

    explainer = shap.Explainer(model)

    shap_values = explainer(X)

    return shap_values