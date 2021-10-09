from . import train

locals().update(train.__dict__) # reuse functions from train.py

# overwrite train functions
def features(df):
    print('test features')