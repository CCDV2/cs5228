import pandas as pd
import numpy as np
from pandas.core.algorithms import SelectNFrame
import torch

class SimpleDataset:
    xcols = ['category', 'transmission', 'curb_weight', 'power',
            'engine_cap', 'no_of_owners', 'depreciation', 'coe', 'road_tax', 'dereg_value', 'mileage', 'omv', 'arf']
    ycol = 'price'
    def __init__(self, path, test_path='', frac=0.8, seed=None, is_train=True, **kwargs) -> None:
        if test_path and not is_train:
            path = test_path
        df = pd.read_csv(path)
        if seed is not None:
            np.random.seed(seed)
        np.random.shuffle(df.values)
        self.raw_data = df
        self.xs = df[kwargs.get('xcols', SimpleDataset.xcols)].values
        ycol = kwargs.get('ycol', SimpleDataset.ycol)
        if ycol in df:
            self.ys = df[ycol].values
        else:
            self.ys = np.zeros(len(self.xs))
        if not test_path and frac:
            part = int(len(self.xs) * frac)
            if is_train:
                self.xs = self.xs[:part]
                self.ys = self.ys[:part]
            else:
                self.xs = self.xs[part:]
                self.ys = self.ys[part:]
        
        self.xs = torch.from_numpy(self.xs)
        self.ys = torch.from_numpy(self.ys)

        assert len(self.xs) == len(self.ys)

    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]

    def __len__(self):
        return len(self.xs)
