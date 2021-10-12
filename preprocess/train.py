from os import X_OK
import pandas as pd
import numpy as np
import time
from . import utils

def listing_id(df: pd.DataFrame):
    # del
    pass

def title(df: pd.DataFrame):
    # del
    pass

def make(df: pd.DataFrame):
    # fill missing values by checking the attribute 'title'
    df['make'] = df.apply(
        lambda row: row['title'].split()[0].lower() if pd.isna(row['make']) else row['make'],
        axis=1
    )


def model(df: pd.DataFrame):
    pass

def description(df: pd.DataFrame):
    # del
    pass

def manufactured(df: pd.DataFrame):
    # fill missing values with other cars of the same model
    miss_bool = df.manufactured.isnull() 
    df_tmp = df.dropna(
        subset=["model", "manufactured"]
    ).drop_duplicates(
        subset=['model'], keep='first', inplace=False
    ).set_index('model')
    df.loc[miss_bool, 'manufactured'] = df.loc[miss_bool, 'model'].apply(
        lambda x: df_tmp.manufactured[x] if x in df_tmp.manufactured else None
    )

    # fill missing values with original_reg_date or reg_date
    df['manufactured'] = df.apply(
        lambda row: time.strptime(
            row['reg_date'] if pd.isna(row['original_reg_date']) else row['original_reg_date'], '%d-%b-%Y'
        ).tm_year if pd.isna(row['manufactured']) or row['manufactured'] > 2022 else row['manufactured'],
        axis=1
    )


def original_reg_date(df: pd.DataFrame):
    # fill missing values with reg_date
    df["original_reg_date"].fillna(df["reg_date"], inplace=True)

    # TODO: convert to timestamp
    # df['original_reg_date'] = df['original_reg_date'].apply(
    #     lambda x: time.strptime(x,'%d-%b-%Y').tm_year if isinstance(x, str) else x
    # )


def reg_date_customized(df: pd.DataFrame):
    # fillmissing values with original_reg_date
    df["reg_date"].fillna(df["original_reg_date"], inplace=True)

    # TODO: convert to timestamp
    # df['reg_date'] = df['reg_date'].apply(
    #     lambda x: time.strptime(x,'%d-%b-%Y').tm_year if isinstance(x, str) else x
    # )


def type_of_vehicle(df: pd.DataFrame):
    pass

def category(df: pd.DataFrame):
    # ordinal encoding
    df['category'] = utils.ordinal_encoder(df['category'])


def transmission(df: pd.DataFrame):
    # ordinal encoding
    df['transmission'] = utils.ordinal_encoder(df['transmission'])


def curb_weight(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["curb_weight"])


def power(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["power"])


def fuel_type(df: pd.DataFrame):
    # del
    pass

def engine_cap(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["engine_cap"])


def no_of_owners(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["no_of_owners"])


def depreciation(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["depreciation"])


def coe(df: pd.DataFrame):
    # delete outliers
    df["coe"] = utils.del_outlier(df["coe"])

    # fill missing values with mean value
    utils.fill_with_mean(df["coe"])


def road_tax(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["road_tax"])

    # equal-width discretization into #num segments
    df["road_tax"] = utils.data_discretization(df["road_tax"], num=15)


def dereg_value(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["dereg_value"])


def mileage(df: pd.DataFrame):
    # delete outliers
    df["mileage"] = utils.del_outlier(df["mileage"])

    # fill missing values with mean value
    utils.fill_with_mean(df["mileage"])

    # equal width discretization into #num segments
    df["mileage"] = utils.data_discretization(df["mileage"], num=15)


def omv(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["omv"])


def arf(df: pd.DataFrame):
    # fill missing values with mean value
    utils.fill_with_mean(df["arf"])


def opc_scheme(df: pd.DataFrame):
    # del
    pass

def lifespan(df: pd.DataFrame):
    # del
    pass

def eco_category(df: pd.DataFrame):
    # del
    pass

def features(df: pd.DataFrame):
    # del
    pass

def accessories(df: pd.DataFrame):
    # del
    pass

def indicative_price(df: pd.DataFrame):
    # del
    pass

def price(df: pd.DataFrame):
    pass