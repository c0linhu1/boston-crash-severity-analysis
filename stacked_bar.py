import altair as alt
import pandas as pd

def create_stacked_bar():
    df = pd.read_csv('cleaned_boston_crashes.csv')

    # filter out 'Other' weather
    df = df[df['WEATHER_SIMPLE'] != 'Other']

    # group by weather and severity, count crashes
    grouped = df.groupby(['WEATHER_SIMPLE', 'CRASH_SEVERITY_DESCR']).size().reset_index(name='count')

    weather_order = ['Clear', 'Cloudy', 'Rain', 'Snow/Ice', 'Fog']
    severity_order = ['Fatal injury', 'Non-fatal injury', 'Property damage only (none injured)']
    severity_colors = ['#c23b22', '#f4a261', '#2c7bb6']

    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('WEATHER_SIMPLE:O',
                 title='Weather Condition',
                 sort=weather_order,
                 axis=alt.Axis(labelAngle=0, labelFontSize=12, titleFontSize=13)),
        y=alt.Y('count:Q',
                 title='Number of Crashes',
                 stack='zero',
                 axis=alt.Axis(labelFontSize=11, titleFontSize=13)),
        color=alt.Color('CRASH_SEVERITY_DESCR:N',
                         title='Crash Severity',
                         sort=severity_order,
                         scale=alt.Scale(domain=severity_order, range=severity_colors),
                         legend=alt.Legend(labelFontSize=11, titleFontSize=12)),
        order=alt.Order('CRASH_SEVERITY_DESCR:N', sort='descending'),
        tooltip=[
            alt.Tooltip('WEATHER_SIMPLE:O', title='Weather'),
            alt.Tooltip('CRASH_SEVERITY_DESCR:N', title='Severity'),
            alt.Tooltip('count:Q', title='Crash Count')
        ]
    ).properties(
        title=alt.Title(
            text='Crash Severity Breakdown by Weather Condition (Boston, 2025)',
            fontSize=16,
            anchor='middle'
        ),
        width=600,
        height=400
    )

    chart.save('stacked_bar.html')
    print('Saved to stacked_bar.html')

if __name__ == '__main__':
    create_stacked_bar()