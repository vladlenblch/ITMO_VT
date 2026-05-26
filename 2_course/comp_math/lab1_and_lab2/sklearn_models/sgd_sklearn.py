import numpy as np

from sklearn.linear_model import SGDRegressor


class SklearnSGDRegressor:
    def __init__(self, learning_rate=0.01, n_iter=500):
        self.model = SGDRegressor(
            learning_rate='adaptive',
            eta0=learning_rate,
            max_iter=1,
            fit_intercept=False,
            shuffle=False,
            random_state=42
        )
        self.weights = np.array([])
        self.weights_history = []
        self.learning_rate = learning_rate
        self.n_iter = n_iter

    def fit(self, X, y):
        self.weights_history = []

        init_idx = np.random.randint(0, len(X) - 1)
        self.model.partial_fit([X[init_idx]], [y[init_idx]])
        self.weights_history.append(self.model.coef_.copy())

        for i in range(1, self.n_iter):
            idx = np.random.randint(0, len(X) - 1)
            self.model.partial_fit([X[idx]], [y[idx]])
            self.weights_history.append(self.model.coef_.copy())

        self.weights = self.model.coef_

        return self

    def predict(self, X):
        return self.model.predict(X)
