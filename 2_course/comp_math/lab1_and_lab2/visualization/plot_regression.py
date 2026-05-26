import plotly.graph_objects as go
import numpy as np


def plot_regression(x_raw, y, model):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_raw,
        y=y,
        mode='markers',
        name='Обучающая выборка',
        marker=dict(
            size=6,
            color='#64B5F6'
        )
    ))

    x_line = np.linspace(-5, 5, 100)
    X_line = np.column_stack([np.ones(100), x_line])
    y_line = model.predict(X_line)

    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        name='Регрессия',
        line=dict(color='#FF6B6B', width=2)
    ))

    x_min, x_max = -5, 5
    y_min, y_max = -10, 10

    fig.update_layout(
        xaxis_title='x',
        yaxis_title='y',
        width=700,
        height=500,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            range=[x_min, x_max],
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            range=[y_min, y_max],
            fixedrange=True
        ),
        margin=dict(l=50, r=50, t=60, b=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    return fig
