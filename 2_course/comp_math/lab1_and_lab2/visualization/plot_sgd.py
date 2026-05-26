import numpy as np
import plotly.graph_objects as go
from utils.metrics import mse

def plot_sgd(model, X, y):
    w0_vals = np.linspace(
        min(w[0] for w in model.weights_history) - 0.5,
        max(w[0] for w in model.weights_history) + 0.5,
        100
    )
    w1_vals = np.linspace(
        min(w[1] for w in model.weights_history) - 0.5,
        max(w[1] for w in model.weights_history) + 0.5,
        100
    )
    W0, W1 = np.meshgrid(w0_vals, w1_vals)

    Z = np.zeros_like(W0)
    for i in range(W0.shape[0]):
        for j in range(W0.shape[1]):
            weights = [W0[i, j], W1[i, j]]
            preds = [sum(x[k] * weights[k] for k in range(len(weights))) for x in X]
            Z[i, j] = mse(y, preds)

    fig = go.Figure()

    fig.add_trace(go.Contour(
        x=w0_vals,
        y=w1_vals,
        z=Z,
        colorscale='Viridis',
        contours=dict(
            start=Z.min(),
            end=Z.max(),
            size=(Z.max() - Z.min()) / 15
        ),
        showscale=False,
        name='MSE',
        showlegend=False
    ))

    w0_path = [w[0] for w in model.weights_history]
    w1_path = [w[1] for w in model.weights_history]

    fig.add_trace(go.Scatter(
        x=w0_path,
        y=w1_path,
        mode='lines+markers',
        name='Траектория SGD',
        line=dict(color='#64B5F6', width=2.5),
        marker=dict(size=6, color='#2196F3', symbol='circle-open'),
        showlegend=False
    ))

    optimal_w = [model.weights[0], model.weights[1]]
    fig.add_trace(go.Scatter(
        x=[optimal_w[0]],
        y=[optimal_w[1]],
        mode='markers',
        name='Оптимум (MSE)',
        marker=dict(
            size=12,
            color='gold',
            symbol='star',
            line=dict(width=2, color='black')
        ),
        showlegend=False
    ))

    fig.update_layout(
        xaxis_title="w0 (intercept)",
        yaxis_title="w1 (slope)",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False
        ),
        margin=dict(l=50, r=50, t=60, b=50),
        height=500,
        showlegend=False
    )

    return fig
