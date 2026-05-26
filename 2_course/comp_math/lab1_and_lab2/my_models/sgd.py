from random import randint

from utils.metrics import mse


class MySGDRegressor:
    def __init__(self, learning_rate=0.01, n_iter=500, decay=0.1):
        self.weights = []
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.decay = decay
        self.loss_history = []
        self.weights_history = []

    def compute_gradient(self, X_row, y_true, weights):
        prediction = sum(X_row[i] * weights[i] for i in range(len(weights)))
        error = prediction - y_true

        grad = []
        for i in range(len(weights)):
            grad_i = 2 * X_row[i] * error
            grad.append(grad_i)

        return grad

    def fit(self, X, y):
        self.weights = [0.0 for _ in range(len(X[0]))]
        self.loss_history = []
        self.weights_history = []

        for i in range(self.n_iter):
            idx = randint(0, len(X) - 1)
            lr = self.learning_rate / (1 + self.decay * i)

            grad = self.compute_gradient(X[idx], y[idx], self.weights)

            self.weights = [
                self.weights[i] - lr * grad[i] for i in range(len(self.weights))
            ]

            self.weights_history.append(self.weights.copy())
            predictions = self.predict(X)
            self.loss_history.append(mse(y, predictions))

        return self

    def predict(self, X):
        predictions = []
        for row in X:
            pred = row[0] * self.weights[0] + row[1] * self.weights[1]
            predictions.append(pred)

        return predictions
