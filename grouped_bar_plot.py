import plotly.express as px
import pandas as pd

def create_grouped_bar():
    df = pd.read_csv('cleaned_boston_crashes.csv')

    # filter out 'Other' categories
    df = df[df['WEATHER_SIMPLE'] != 'Other']
    df = df[df['LIGHTING_SIMPLE'] != 'Other']

    # compute severity rate per weather + lighting combo
    grouped = df.groupby(['WEATHER_SIMPLE', 'LIGHTING_SIMPLE']).agg(
        total_crashes=('IS_SEVERE', 'count'),
        severe_crashes=('IS_SEVERE', 'sum')
    ).reset_index()

    grouped['severity_rate'] = (grouped['severe_crashes'] / grouped['total_crashes'] * 100).round(1)

    # filter out combos with very few crashes to avoid misleading rates
    grouped = grouped[grouped['total_crashes'] >= 5]

    color_map = {
        'Daylight': '#2c7bb6',
        'Dark - Lighted': '#fdae61',
        'Dark - Unlighted': '#d7191c',
        'Dawn/Dusk': '#abd9e9'
    }

    fig = px.bar(
        grouped,
        x = 'WEATHER_SIMPLE',
        y = 'severity_rate',
        color = 'LIGHTING_SIMPLE',
        color_discrete_map = color_map,
        barmode = 'group',
        hover_data = {
            'total_crashes': True,
            'severe_crashes': True,
            'severity_rate': True
        },
        labels = {
            'WEATHER_SIMPLE': 'Weather Condition',
            'severity_rate': 'Severity Rate (%)',
            'LIGHTING_SIMPLE': 'Lighting',
            'total_crashes': 'Total Crashes',
            'severe_crashes': 'Severe Crashes'
        },
        title = 'Crash Severity Rate by Weather and Lighting Conditions — Boston (Jan 2025)'
    )

    # dropdown to filter by road surface
    road_types = df['ROAD_SIMPLE'].unique()
    road_types = [r for r in road_types if r != 'Other']

    buttons = [dict(label = 'All Road Surfaces', method = 'update',
                    args = [{'visible': [True] * len(fig.data)},
                          {'title': 'Crash Severity Rate by Weather and Lighting Conditions — Boston (Jan 2025)'}])]

    fig.update_layout(
        xaxis_title = 'Weather Condition',
        yaxis_title = 'Severity Rate (%)',
        font = dict(size = 12),
        height = 600,
        width = 1000,
        plot_bgcolor ='#f9f9f9',

        legend_title_text = 'Lighting Condition',
        yaxis = dict(range = [0, 100])
    )

    fig.show()
    fig.write_html('grouped_bar.html')


if __name__ == '__main__':
    create_grouped_bar()