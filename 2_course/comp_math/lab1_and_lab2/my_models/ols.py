from computations.transpose_matrix import transpose
from computations.inverse_matrix import inverse_2_by_2
from computations.multiply_matrix import multiply


class MyOLSRegression():
    def __init__(self):
        self.weights = []

    def fit(self, X, y):
        y_col = [[val] for val in y]

        XT = transpose(X)
        XT_X = multiply(XT, X)
        XT_X_inv = inverse_2_by_2(XT_X)
        XT_X_inv_XT = multiply(XT_X_inv, XT)
        XT_X_inv_XT_y = multiply(XT_X_inv_XT, y_col)
        self.weights = [XT_X_inv_XT_y[0][0], XT_X_inv_XT_y[1][0]]

        return self

    def predict(self, X):
        predictions = []
        for row in X:
            pred = row[0] * self.weights[0] + row[1] * self.weights[1]
            predictions.append(pred)

        return predictions
