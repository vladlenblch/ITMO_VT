import numpy as np


def generate_linear_data(n_samples=100, noise_level=1.0, true_intercept=0.0, true_slope=1.0, x_range=(-5, 5)):
    x_raw = np.random.uniform(low=x_range[0], high=x_range[1], size=n_samples)

    noise = np.random.normal(loc=0.0, scale=noise_level, size=n_samples)

    y_true = true_intercept + true_slope * x_raw
    y = y_true + noise

    X = np.column_stack([np.ones(n_samples), x_raw])

    return X, y, x_raw
