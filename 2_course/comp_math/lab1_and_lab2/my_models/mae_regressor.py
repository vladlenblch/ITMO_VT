from random import randint


class MyMAERegressor():
    def __init__(self,  learning_rate=0.005, n_iter=5000, decay=0.01):
        self.weights = []
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.decay = decay

    def compute_subgradient(self, X_row, y_true, weights):
        prediction = sum(X_row[i] * weights[i] for i in range(len(weights)))
        error = prediction - y_true

        if error > 0: sign = 1
        elif error < 0: sign = -1
        else: sign = 0

        grad = []
        for i in range(len(weights)):
            grad_i = sign * X_row[i]
            grad.append(grad_i)

        return grad

    def fit(self, X, y):
        self.weights = [0.0 for _ in range(len(X[0]))]

        for i in range(self.n_iter):
            idx = randint(0, len(X) - 1)
            lr = self.learning_rate / (1 + self.decay * i)

            grad = self.compute_subgradient(X[idx], y[idx], self.weights)

            self.weights = [
                self.weights[i] - lr * grad[i] for i in range(len(self.weights))
            ]

        return self

    def predict(self, X):
        predictions = []
        for row in X:
            pred = row[0] * self.weights[0] + row[1] * self.weights[1]
            predictions.append(pred)

        return predictions
