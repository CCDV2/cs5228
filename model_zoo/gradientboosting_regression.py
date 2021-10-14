import torch
from .base_model import BaseModel
from sklearn.ensemble import GradientBoostingRegressor


class GradientBoostingRegressionModel(BaseModel):
    def __init__(self, **kwargs) -> None:
        self.model = GradientBoostingRegressor(**kwargs)

    def _collect_data(self, dataloader):
        xs, ys = [], []
        for x, y in dataloader:
            xs.append(x)
            ys.append(y)
        x = torch.cat(xs)
        y = torch.cat(ys)
        return x, y

    def _train(self, train_dataloader):
        X_train, y_train = self._collect_data(train_dataloader)
        print(X_train.shape, y_train.shape)
        self.model.fit(X_train, y_train)

    def _test(self, test_dataloader):
        X_test, y_test = self._collect_data(test_dataloader)
        pred = self.model.predict(X_test)
        return pred, y_test

    def predict(self, train_dataloader, test_dataloader):
        print('training')
        self._train(train_dataloader)
        print('testing')
        return self._test(test_dataloader)
