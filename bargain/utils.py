import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder


def ordinal_encoder(column: pd.Series):
    encoder = OrdinalEncoder().fit(column)
    return encoder.transform(column)


def onehot_encoder(column: pd.Series):
    encoder = OneHotEncoder().fit(column)
    return encoder.transform(column)


def del_outlier(column: pd.Series, lower_val: float = 0.01, upper_val: float = 0.99):
    lower_bound = column.quantile(lower_val)
    upper_bound = column.quantile(upper_val)
    new_column = column.apply(
        lambda x: None if x <= lower_bound or x >= upper_bound else x
    )
    return new_column


def fill_with_mean(column: pd.Series):
    column.fillna(round(column.mean()), inplace=True)


def data_discretization(column: pd.Series, num: int = 15):
    new_column = pd.cut(column, num, labels=range(1, num+1))
    return new_column
