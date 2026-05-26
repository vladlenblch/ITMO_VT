import plotly.graph_objects as go


def plot_data_points(x_raw, y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_raw,
        y=y,
        mode='markers',
        name='Data points',
        marker=dict(
            size=6,
            color='#64B5F6'
        )
    ))

    x_min, x_max = -5, 5
    y_min, y_max = -10, 10

    fig.update_layout(
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
        margin=dict(l=50, r=50, t=60, b=50)
    )
    return fig
