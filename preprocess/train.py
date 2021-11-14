from os import X_OK
import pandas as pd
import numpy as np
import time

import json
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
        lambda row: row['title'].split()[0].lower(
        ) if pd.isna(row['make']) else row['make'],
        axis=1
    )
    df['make'] = utils.ordinal_encoder(df['make'])

def make_oh(df: pd.DataFrame):
    oh = pd.get_dummies(df['make'])
    return oh

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
            row['reg_date'] if pd.isna(
                row['original_reg_date']) else row['original_reg_date'], '%d-%b-%Y'
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
    df['type_of_vehicle'] = utils.ordinal_encoder(df['type_of_vehicle'])

def type_of_vehicle_oh(df: pd.DataFrame):
    oh = pd.get_dummies(df['type_of_vehicle'])
    return oh


def category(df: pd.DataFrame):
    # ordinal encoding
    df['category'] = utils.ordinal_encoder(df['category'])

def category_oh(df: pd.DataFrame):
    oh = pd.get_dummies(df['category'])
    return oh

def category_multilabel(df: pd.DataFrame):
    categoires = {}
    cnt = 0
    for i, row in df.iterrows():
        cats = row['category']
        cats_list = cats.split(',')
        for cat in cats_list:
            cat = cat.strip()
            if cat not in categoires:
                categoires[cat] = cnt
                cnt += 1
    a = np.zeros((len(df), cnt), dtype=np.int32)
    for i, row in df.iterrows():
        cats = row['category']
        cats_list = cats.split(',')
        idx = [categoires[cat.strip()] for cat in cats_list]
        a[i, idx] = 1
    multilabel_df = pd.DataFrame(a, columns=list(categoires.keys()))
    return multilabel_df



def transmission(df: pd.DataFrame):
    # ordinal encoding
    df['transmission'] = utils.ordinal_encoder(df['transmission'])

def transmission_oh(df: pd.DataFrame):
    oh = pd.get_dummies(df['transmission'])
    return oh

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
    df["depreciation"] = utils.del_outlier(
        df["depreciation"], lower_val=0.0, upper_val=0.99)
    # fill missing values with mean value
    utils.fill_with_mean(df["depreciation"])


def coe(df: pd.DataFrame):
    # delete outliers
    df["coe"] = utils.del_outlier(df["coe"], lower_val=0.01, upper_val=1.0)

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


def _vague_match(s: str, patterns):
    def to_words(s: str):
        s = s.replace('-', ' ').replace('(', ' ').replace(')', ' ')
        return s.split()

    def similarity(words, pattern):
        sim = 0
        for w in words:
            for p in pattern:
                if w in p:
                    sim += 1
                    break
        return sim

    words = to_words(s)
    words_patterns = [(to_words(p), i) for i, p in enumerate(patterns)]
    similarity = [(similarity(words, wp), wp, i) for wp, i in words_patterns]
    similarity.sort(reverse=True)
    return patterns[similarity[0][2]]

def import_price(df: pd.DataFrame):
    with open('./data/brand_mapping.json', 'r') as f:
        brand_mapping = json.load(f)
    with open('./data/gov_price.json', 'r') as f:
        d = json.load(f)
    def add_import_price(row):
        title = row['title'].lower()
        make = row['make']
        try:
            if type(make) is float:
                make = title.split()[0]
            if make not in d:
                if make in brand_mapping:
                    make = brand_mapping[make]
                    if make == 'others': return 0
                else:
                    return 0
        except Exception as e:
            print(e, title, make)
            return 0
        model = _vague_match(title, list(d[make].keys()))
        price = list(d[make][model].values())[-1]
        return price

    df['import_price'] = df.apply(add_import_price, axis=1)

def scale_factor(df: pd.DataFrame):
    df['scale_factor'] = df['price'] / df['import_price']
    df['scale_factor'] = df.apply(
        lambda x: None if x['scale_factor'] is None or x['scale_factor'] > 10 else x.scale_factor, axis=1)
    utils.fill_with_mean(df['scale_factor'])
    # df['scale_factor'].fillna(0, inplace=True)
