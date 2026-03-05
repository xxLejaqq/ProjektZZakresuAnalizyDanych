import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
import country_converter as coco

cc = coco.CountryConverter()

class ColumnDropper(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        return X.drop(columns = self.columns, axis=1, errors='ignore')

class ChangeNameCountry(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['Country_cc'] = cc.convert(names=X['Country'], to='name_short', not_found='not_found')
        return X

class AddRegion(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['Region_cc'] = cc.convert(names=X['Country_cc'], to='UNregion', not_found='not_found')
        return X

class TransPower(BaseEstimator, TransformerMixin):
    
    def __init__(self, column, power=2):
        self.column = column
        self.power = power

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.column] = X[self.column] ** self.power
        return X

class TransLog(BaseEstimator, TransformerMixin):
    
    def __init__(self, column, epsilon=1e-9):
        self.column = column
        self.epsilon = epsilon

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.column] = np.log(X[self.column] + self.epsilon)
        return X

class OneH(BaseEstimator, TransformerMixin):
    
    def __init__(self, column):
        self.column = column
        self.ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    def fit(self, X, y=None):
        self.ohe.fit(X[[self.column]])
        return self

    def transform(self, X):
        X = X.copy()
        encoded = self.ohe.transform(X[[self.column]])
        encoded_df = pd.DataFrame(
            encoded,
            columns=self.ohe.get_feature_names_out([self.column]),
            index=X.index)
        X = X.drop(self.column, axis=1)
        X = pd.concat([X, encoded_df], axis=1)
        return X

class ChangeToBinnary(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.columns] = X[self.columns].apply(lambda x: 0 if x < 0.5 else 1)
        return X



