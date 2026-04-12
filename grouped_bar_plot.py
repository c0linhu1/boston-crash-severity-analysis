import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_grouped_bar():
    df = pd.read_csv('cleaned_boston_crashes.csv')

    # filter out 'Other' categories
    df = df[df['WEATHER_SIMPLE'] != 'Other']
    df = df[df['LIGHTING_SIMPLE'] != 'Other']

    lighting_order = ['Daylight', 'Dark - Lighted', 'Dark - Unlighted', 'Dawn/Dusk']
    weather_order = ['Clear', 'Cloudy', 'Rain', 'Snow/Ice', 'Fog']

    color_map = {
        'Daylight': '#2c7bb6',
        'Dark - Lighted': '#fdae61',
        'Dark - Unlighted': '#d7191c',
        'Dawn/Dusk': '#abd9e9'
    }

    # get road types (excluding Other)
    road_types = sorted([r for r in df['ROAD_SIMPLE'].unique() if r != 'Other'])

    # helper to compute severity rates for a subset
    def compute_rates(subset):
        grouped = subset.groupby(['WEATHER_SIMPLE', 'LIGHTING_SIMPLE']).agg(
            total_crashes=('IS_SEVERE', 'count'),
            severe_crashes=('IS_SEVERE', 'sum')
        ).reset_index()
        grouped['severity_rate'] = (grouped['severe_crashes'] / grouped['total_crashes'] * 100).round(1)
        grouped = grouped[grouped['total_crashes'] >= 5]
        return grouped

    # build traces for each road surface filter (All + each road type)
    fig = go.Figure()

    datasets = [('All Road Surfaces', df)] + [(rt, df[df['ROAD_SIMPLE'] == rt]) for rt in road_types]

    traces_per_dataset = len(lighting_order)  # one trace per lighting condition
    num_datasets = len(datasets)

    for i, (label, subset) in enumerate(datasets):
        rates = compute_rates(subset)

        for lighting in lighting_order:
            light_data = rates[rates['LIGHTING_SIMPLE'] == lighting]

            fig.add_trace(go.Bar(
                x=light_data['WEATHER_SIMPLE'],
                y=light_data['severity_rate'],
                name=lighting,
                marker_color=color_map.get(lighting, '#999'),
                customdata=light_data[['total_crashes', 'severe_crashes']].values,
                hovertemplate=(
                    '<b>%{x}</b> — ' + lighting + '<br>'
                    'Severity Rate: %{y}%<br>'
                    'Total Crashes: %{customdata[0]}<br>'
                    'Severe Crashes: %{customdata[1]}<br>'
                    '<extra></extra>'
                ),
                visible=(i == 0),  # only show "All" by default
                showlegend=(i == 0)
            ))

    # build dropdown buttons
    buttons = []
    for i, (label, _) in enumerate(datasets):
        visibility = [False] * (num_datasets * traces_per_dataset)
        for j in range(traces_per_dataset):
            visibility[i * traces_per_dataset + j] = True

        # show legend only for the active dataset's traces
        legend_updates = [False] * (num_datasets * traces_per_dataset)
        for j in range(traces_per_dataset):
            legend_updates[i * traces_per_dataset + j] = True

        buttons.append(dict(
            label=label,
            method='update',
            args=[
                {'visible': visibility, 'showlegend': legend_updates},
                {'title': f'Crash Severity Rate by Weather and Lighting — Boston (2025)<br><sup>Road Surface: {label}</sup>'}
            ]
        ))

    fig.update_layout(
        title=dict(
            text='Crash Severity Rate by Weather and Lighting Conditions — Boston (2025)',
            font=dict(size=18),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        xaxis_title='Weather Condition',
        yaxis_title='Severity Rate (%)',
        barmode='group',
        font=dict(size=12),
        height=650,
        width=1000,
        plot_bgcolor='white',
        legend_title_text='Lighting Condition',
        yaxis=dict(range=[0, 100]),
        margin=dict(t=120, b=60, l=70, r=70),
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                x=0.02,
                xanchor='left',
                y=1.2,
                yanchor='top',
                bgcolor='white',
                bordercolor='#ccc',
                borderwidth=1,
                font=dict(size=12),
                pad=dict(r=10, t=10)
            )
        ],
        annotations=[
            dict(
                text='Road Surface:',
                x=0.02, y=1.25,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=12, color='#555'),
                xanchor='right'
            )
        ]
    )

    fig.write_html('grouped_bar.html')
    print('Saved to grouped_bar.html')

if __name__ == '__main__':
    create_grouped_bar()