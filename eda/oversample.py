import smogn
import pandas as pd

df = pd.read_csv('../data/train_processed.csv')

df = smogn.smoter(data=df, y='price', k=9, samp_method='extreme', pert=0.01)

df.to_csv('../data/train_oversampled2.csv', index=False)