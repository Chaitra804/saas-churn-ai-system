import pandas as pd

from sklearn.preprocessing import LabelEncoder

from pandas.api.types import (
    is_numeric_dtype,
    is_string_dtype
)


def preprocess_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric-looking strings
    for col in df.columns:

        try:
            df[col] = pd.to_numeric(df[col])

        except:
            pass

    # Handle missing values
    for col in df.columns:

        # Numeric columns
        if is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(
                df[col].median()
            )

        # String / categorical columns
        elif is_string_dtype(df[col]) or df[col].dtype == "object":

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

    # Encode categorical columns
    label_encoders = {}

    for col in df.columns:

        if (
            is_string_dtype(df[col]) or
            df[col].dtype == "object"
        ):

            le = LabelEncoder()

            df[col] = le.fit_transform(
                df[col].astype(str)
            )

            label_encoders[col] = le

    return df, label_encoders