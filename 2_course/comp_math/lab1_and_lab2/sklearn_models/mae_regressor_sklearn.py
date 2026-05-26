import numpy as np

from sklearn.linear_model import QuantileRegressor


class SklearnMAERegressor():
    def __init__(self):
        self.model = QuantileRegressor(
            quantile=0.5,
            alpha=0.0,
            solver='highs',
            fit_intercept=False
        )
        self.weights = np.array([])

    def fit(self, X, y):
        self.model.fit(X, y)
        self.weights = self.model.coef_

        return self

    def predict(self, X):
        return self.model.predict(X)
