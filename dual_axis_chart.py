import pandas as pd
import plotly.graph_objects as go

def speed_vs_crashes(df):
    """Dual-axis chart - speed limit vs crash count and severity rate"""

    plot_df = df.dropna(subset=['SPEED_LIMIT']).copy()
    valid_speeds = [20, 25, 30, 35, 40, 45, 50, 55, 65]
    plot_df = plot_df[plot_df['SPEED_LIMIT'].isin(valid_speeds)]
    plot_df['SPEED_LIMIT'] = plot_df['SPEED_LIMIT'].astype(int)

    agg = plot_df.groupby('SPEED_LIMIT').agg(
        crash_count=('CRASH_NUMB', 'count'),
        severe_crashes=('IS_SEVERE', 'sum')
    ).reset_index()

    agg['severity_rate'] = (agg['severe_crashes'] / agg['crash_count'] * 100).round(1)
    agg['SPEED_LIMIT'] = agg['SPEED_LIMIT'].astype(str)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=agg['SPEED_LIMIT'],
        y=agg['crash_count'],
        name='Total Crashes',
        marker=dict(
            color=agg['crash_count'],
            colorscale='Blues',
            showscale=False,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        yaxis='y1',
        hovertemplate=(
            '<b>Speed Limit: %{x} mph</b><br>'
            'Total Crashes: %{y}<br>'
            '<extra></extra>'
        )
    ))

    fig.add_trace(go.Scatter(
        x=agg['SPEED_LIMIT'],
        y=agg['severity_rate'],
        name='Severity Rate (%)',
        mode='lines+markers',
        marker=dict(
            size=10,
            color='crimson',
            symbol='circle',
            line=dict(color='white', width=2)
        ),
        line=dict(color='crimson', width=3),
        yaxis='y2',
        hovertemplate=(
            '<b>Speed Limit: %{x} mph</b><br>'
            'Severity Rate: %{y}%<br>'
            '<extra></extra>'
        )
    ))

    fig.update_layout(
        title=dict(
            text='Crash Count and Severity Rate by Speed Limit in Boston (2025)',
            font=dict(size=18),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text='Speed Limit (mph)', font=dict(size=13)),
            categoryorder='array',
            categoryarray=['20', '25', '30', '35', '40', '45', '50', '55', '65'],
            tickfont=dict(size=12),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text='Total Crashes', font=dict(size=13, color='steelblue')),
            tickfont=dict(color='steelblue', size=11),
            showgrid=True,
            gridcolor='rgba(200,200,200,0.4)',
            zeroline=False
        ),
        yaxis2=dict(
            title=dict(text='Severity Rate (%)', font=dict(size=13, color='crimson')),
            tickfont=dict(color='crimson', size=11),
            overlaying='y',
            side='right',
            range=[0, 100],
            showgrid=False,
            zeroline=False,
            ticksuffix='%'
        ),
        legend=dict(
            x=0.99,
            y=0.99,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.85)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1,
            font=dict(size=12)
        ),
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='white',
        width=1000,
        height=600,
        margin=dict(t=80, b=60, l=70, r=70),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            bordercolor='rgba(0,0,0,0.2)'
        ),
        annotations=[
            dict(
                text='Severity rate = % of crashes resulting in injury or fatality',
                xref='paper', yref='paper',
                x=0, y=-0.12,
                showarrow=False,
                font=dict(size=11, color='gray'),
                xanchor='left'
            )
        ]
    )

    fig.write_html('dual_axis.html')
    print('Saved to dual_axis.html')

def main():
    df = pd.read_csv('cleaned_boston_crashes.csv')
    speed_vs_crashes(df)

if __name__ == '__main__':
    main()