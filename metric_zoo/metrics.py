from sklearn.metrics import mean_squared_error

MSE = lambda x, y, **kwargs: mean_squared_error(y, x, **kwargs)