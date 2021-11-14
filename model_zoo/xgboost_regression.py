import xgboost
from .base_model import BaseModel
import torch
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt

class XGBoostRegressionModel(BaseModel):
    def __init__(self, grid_params={}, **kwargs):
        self.model = xgboost.XGBRegressor(
            tree_method="hist", **kwargs)
        self.grid_params = grid_params

    def _collect_data(self, dataloader):
        xs, ys = [], []
        for x, y in dataloader:
            xs.append(x)
            ys.append(y)
        x = torch.cat(xs)
        y = torch.cat(ys)
        return x, y

    def tune(self, train_dataloader):
        X_train, y_train = self._collect_data(train_dataloader)
        reg = GridSearchCV(self.model, self.grid_params, n_jobs=6)
        reg.fit(X_train, y_train)
        print(reg.best_params_)
        self.model = reg.best_estimator_


    def _train(self, train_dataloader):
        if self.grid_params:
            self.tune(train_dataloader)
            return
        X_train, y_train = self._collect_data(train_dataloader)
        y_log_train = np.log(y_train)
        self.mean = float(y_log_train.mean())
        self.std = float(y_log_train.std())
        print(self.mean, self.std)
        y_log_train -= self.mean
        y_log_train /= self.std
        print(X_train.shape, y_log_train.shape)
        self.model.fit(X_train, y_train)

    def _test(self, test_dataloader):
        X_test, y_test = self._collect_data(test_dataloader)
        pred = self.model.predict(X_test)
        # y_log_test = np.log(y_test.numpy())
        # plt.hist(pred * self.std + self.mean, bins=100)
        # plt.hist(y_log_test, bins=100)
        # plt.show()
        # pred = np.exp(pred * self.std + self.mean)
        return pred, y_test

    def predict(self, train_dataloader, test_dataloader):
        print('training')
        self._train(train_dataloader)
        print('testing')
        return self._test(test_dataloader)
