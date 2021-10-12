import pandas as pd
from category_encoders import OrdinalEncoder

def ordinal_encoder(column: pd.Series):
    encoder = OrdinalEncoder().fit(column)
    return encoder.transform(column)

def del_outlier(column: pd.Series):
    lower_bound = column.quantile(0.01)
    upper_bound = column.quantile(0.99)
    new_column = column.apply(
            lambda x: None if x <= lower_bound or x >= upper_bound else x
        )
    return new_column

def fill_with_mean(column: pd.Series):
    column.fillna(round(column.mean()), inplace=True)

def data_discretization(column: pd.Series, num: int=15):
    new_column = pd.cut(column, num, labels=range(1, num+1))
    return new_column
