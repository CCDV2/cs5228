import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./data/train_processed.csv')
price = df['price'].values

bins = 100
# log_price = np.log(price)
log_price = price
hist = np.histogram(log_price, bins)
print(hist)
m, s = log_price.mean(), log_price.std()
# s -= 0.1
print(m, s)
mn, mx = log_price.min(), log_price.max()
x = np.linspace(mn, mx, 100)
y = 1 / (2 * np.pi) ** 0.5 * s * np.exp(-0.5 * ((x - m) / s) ** 2) 
scale = hist[0].max() / y.max()
y *= scale
# y *= 2000
plt.hist(log_price, bins=bins)
plt.plot(x, y)
plt.show()

