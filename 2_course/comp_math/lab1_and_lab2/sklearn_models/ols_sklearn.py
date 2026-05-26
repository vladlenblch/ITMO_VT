import numpy as np

from sklearn.linear_model import LinearRegression


class SklearnOLSRegression():
    def __init__(self):
        self.model = LinearRegression(fit_intercept=False)
        self.weights = np.array([])

    def fit(self, X, y):
        self.model.fit(X, y)
        self.weights = self.model.coef_

        return self

    def predict(self, X):
        return self.model.predict(X)
