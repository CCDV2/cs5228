import pandas as pd
from importlib import import_module

def main(cfg):
    for name, v in cfg.items():
        path = v.get('path', f'./data/{name}.csv')
        df = pd.read_csv(path) # type: pd.DataFrame
        module = import_module('.' + name, package=__name__)
        # update
        for column in df:
            func = getattr(module, v.get(column, column), None)
            if func is not None:
                func(df)
        # add
        for attr in v.get('_add', []):
            func = getattr(module, attr)
            func(df)
        # drop
        if v.get('_drop', []):
            df.drop(columns=v['_drop'], inplace=True)

        df.to_csv(v['save_path'], encoding='utf-8', index=False)
