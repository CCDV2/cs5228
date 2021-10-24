import pandas as pd
from importlib import import_module


def main(cfg):
    for name, v in cfg.items():
        if name == 'train':
            df_train = pd.read_csv('./data/train.csv')
            df_test = pd.read_csv('./data/test.csv')

            df = pd.concat([df_test, df_train])
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

            assert len(df) == len(df_test) + len(df_train)
            df_t = df[:len(df_test)]
            df_t = df_t.drop(columns='price')
            df_t.to_csv('./data/test_processed.csv',
                        encoding='utf-8', index=False)
            df[len(df_test):].to_csv('./data/train_processed.csv',
                                     encoding='utf-8', index=False)
        elif name == 'test':
            continue
        else:
            path = v.get('path', f'./data/{name}.csv')
            df = pd.read_csv(path)  # type: pd.DataFrame
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
