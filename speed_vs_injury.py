import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


# boxplot
def speed_vs_injuries(df):
    """Interactive box plot - speed limit vs injury count - colored by weather"""

    # dropping the nulls/NaNs in the speed limit column
    plot_df = df.dropna(subset = ['SPEED_LIMIT']).copy()
    valid_speeds = [20, 25, 30, 35, 40, 45, 50, 55, 65]
    plot_df = plot_df[plot_df['SPEED_LIMIT'].isin(valid_speeds)]

    plot_df['TOTAL_INJURIES'] = plot_df['NUMB_NONFATAL_INJR'] + plot_df['NUMB_FATAL_INJR']

    # so we have even spacing on the x axis
    plot_df['SPEED_LIMIT'] = plot_df['SPEED_LIMIT'].astype(int).astype(str)

    fig = px.box(
        plot_df,
        x = 'SPEED_LIMIT',
        y = 'TOTAL_INJURIES',
        color = 'WEATHER_SIMPLE',
        title = 'Injury Distribution by Speed Limit and Weather Condition in Boston (2025)',
        labels = {
            'SPEED_LIMIT': 'Speed Limit (mph)',
            'TOTAL_INJURIES': 'Total Injuries',
            'WEATHER_SIMPLE': 'Weather'
        },
        category_orders = {
            'SPEED_LIMIT': ['20', '25', '30', '35', '40', '45', '50', '55', '65'],
            'WEATHER_SIMPLE': ['Clear', 'Cloudy', 'Rain', 'Snow/Ice', 'Fog', 'Other']
        },
        color_discrete_map = {
            'Clear': 'blue',
            'Cloudy': 'gray',
            'Rain': 'green',
            'Snow/Ice': 'purple',
            'Fog': 'orange',
            'Other': 'brown'
        }
    )

    fig.update_layout(
        width = 1000,
        height = 600
    )

    fig.show()

def main():
    df = pd.read_csv('cleaned_boston_crashes.csv')
    speed_vs_injuries(df)

if __name__ == '__main__':
    main()
