from torch import optim
import torch
from torch.nn.modules.loss import MSELoss
from .base_model import BaseModel
import torch.nn as nn
from torch.optim import SGD
from typing import Tuple, Any
import matplotlib.pyplot as plt

class MLPNetwork(nn.Module):
    def __init__(self, dims=[]):
        # mean=112910.1644, std=134247.8266
        super(MLPNetwork, self).__init__()
        layers = []
        for i in range(1, len(dims)):
            layers.append(nn.Linear(dims[i - 1], dims[i]))
            layers.append(nn.Dropout(p=0.3))
            if i != len(dims) - 1:
                layers.append(nn.Sigmoid())
        self.model = nn.Sequential(*layers)


    def forward(self, x):
        x = self.model(x)
        x = x.mean(dim=1)
        return x

class MLPRegressionModel(BaseModel):
    def __init__(self, epochs=10, lr=1e-3, mean=1500000, std=3000000, MLP={}, **kwargs):
        self.epochs = epochs
        self.lr = lr
        self.net = MLPNetwork(**MLP)
        self.mean = mean
        self.std = std
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _train(self, train_dataloader):
        self.net.train()
        optimizer = SGD(self.net.parameters(),
                        lr=self.lr, momentum=self.momentum)
        loss_function = MSELoss()
        loss_history = []
        for e in range(self.epochs):
            for i, (data, label) in enumerate(train_dataloader):
                data = data.float()
                label = label.float()
                label = (label - self.mean) / self.std
                optimizer.zero_grad()
                output = self.net(data)
                loss = loss_function(output, label)
                loss.backward()
                optimizer.step()
                if i % 50 == 0:
                    print(f'Epoch {e + 1:02d}/{self.epochs:02d}, iter {i:03d}, loss {loss.item():.2f}')
                    # print(f'mean {label.mean()}, std {label.std()}')
                    loss_history.append(loss.item())
        # plt.clf()
        # plt.plot(loss_history)
        # plt.show()

    @torch.no_grad()
    def _test(self, test_dataloader):
        self.net.eval()
        labels = []
        scores = []
        for data, label in test_dataloader:
            data = data.float()
            label = label.float()
            output = self.net(data)
            scores.append(output)
            labels.append(label)
        scores = torch.cat(scores)
        labels = torch.cat(labels)
        scores = scores * self.std + self.mean
        return scores, labels


    def predict(self, train_dataloader, test_dataloader) -> Tuple[Any, Any]:
        self._train(train_dataloader)
        return self._test(test_dataloader)
