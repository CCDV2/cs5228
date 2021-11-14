import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./data/train_processed.csv')
make = df['make'].values

log_make = np.log10(make)
m, s = log_make.mean(), log_make.std()
# s -= 0.1
print(m, s)
mn, mx = log_make.min(), log_make.max()
x = np.linspace(mn, mx, 100)
y = 1 / (2 * np.pi) ** 0.5 * s * np.exp(-0.5 * ((x - m) / s) ** 2)
scale = 1000 / y.max()
y *= scale
# y *= 2000
plt.hist(log_make, bins=100)
plt.plot(x, y)
plt.show()
