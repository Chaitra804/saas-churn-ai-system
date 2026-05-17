import pandas as pd


def load_train_data():

    df = pd.read_csv("data/raw/train.csv")

    return df


def load_test_data():

    df = pd.read_csv("data/raw/test.csv")

    return df