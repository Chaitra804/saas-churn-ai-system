import joblib

from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier # type: ignore

from app.ml.data_loader import (
    load_train_data,
    load_test_data
)

from app.ml.preprocess import preprocess_data
from app.ml.feature_engineering import create_features


TARGET_COLUMN = "Churn"


def train_model():

    # Load datasets
    train_df = load_train_data()
    test_df = load_test_data()

    # Feature engineering
    train_df = create_features(train_df)
    test_df = create_features(test_df)

    # Preprocessing
    train_df, label_encoders = preprocess_data(train_df)
    test_df, _ = preprocess_data(test_df)

    # Split features and target
    X_train = train_df.drop(TARGET_COLUMN, axis=1)
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df.drop(TARGET_COLUMN, axis=1)
    y_test = test_df[TARGET_COLUMN]

    # Train model
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"\nModel Accuracy: {accuracy:.4f}")

    # Save model
    joblib.dump(
        model,
        "models/churn_model.pkl"
    )

    # Save encoders
    joblib.dump(
    X_train.columns.tolist(),
    "models/model_columns.pkl"
   )

    print("\nModel saved successfully!")


if __name__ == "__main__":

    train_model()