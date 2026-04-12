import pandas as pd
import altair as alt

def create_heatmap(df):
    plot_df = df.copy()
    plot_df['TOTAL_INJURIES'] = plot_df['NUMB_NONFATAL_INJR'] + plot_df['NUMB_FATAL_INJR']

    # aggregate by hour and day of week
    agg = plot_df.groupby(['HOUR', 'DAY_OF_WEEK']).agg(
        crash_count=('CRASH_NUMB', 'count'),
        total_injuries=('TOTAL_INJURIES', 'sum')
    ).reset_index()

    agg['injury_rate'] = (agg['total_injuries'] / agg['crash_count']).round(3)

    # ordered days for the y axis
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # ---- Interactive selection: click a day on the top heatmap to filter the bottom ----
    day_selection = alt.selection_point(fields=['DAY_OF_WEEK'], empty='all')
    hour_selection = alt.selection_interval(encodings=['x'], empty='all')

    # ---- Top heatmap: crash count with interval selection on hours ----
    crash_count_heatmap = alt.Chart(agg).mark_rect().encode(
        x=alt.X('HOUR:O',
                 title='Hour of Day (0 = Midnight)',
                 sort=list(range(24)),
                 axis=alt.Axis(labelAngle=0)),
        y=alt.Y('DAY_OF_WEEK:O',
                 title='Day of Week',
                 sort=day_order),
        color=alt.condition(
            hour_selection & day_selection,
            alt.Color('crash_count:Q',
                       title='Crash Count',
                       scale=alt.Scale(scheme='orangered')),
            alt.value('#e0e0e0')
        ),
        tooltip=[
            alt.Tooltip('DAY_OF_WEEK:O', title='Day'),
            alt.Tooltip('HOUR:O', title='Hour'),
            alt.Tooltip('crash_count:Q', title='Crash Count'),
            alt.Tooltip('injury_rate:Q', title='Injury Rate', format='.3f')
        ]
    ).properties(
        title='Crash Count by Hour and Day — Click & Drag to Select Hours, Click a Row to Select a Day',
        width=700,
        height=280
    ).add_params(
        hour_selection,
        day_selection
    )

    # ---- Bottom heatmap: injury rate, filtered by selections from top ----
    injury_rate_heatmap = alt.Chart(agg).mark_rect().encode(
        x=alt.X('HOUR:O',
                 title='Hour of Day (0 = Midnight)',
                 sort=list(range(24)),
                 axis=alt.Axis(labelAngle=0)),
        y=alt.Y('DAY_OF_WEEK:O',
                 title='Day of Week',
                 sort=day_order),
        color=alt.condition(
            hour_selection & day_selection,
            alt.Color('injury_rate:Q',
                       title='Injury Rate',
                       scale=alt.Scale(scheme='purplered', domain=[0, 1])),
            alt.value('#e0e0e0')
        ),
        tooltip=[
            alt.Tooltip('DAY_OF_WEEK:O', title='Day'),
            alt.Tooltip('HOUR:O', title='Hour'),
            alt.Tooltip('crash_count:Q', title='Crash Count'),
            alt.Tooltip('injury_rate:Q', title='Injury Rate', format='.3f')
        ]
    ).properties(
        title='Injury Rate by Hour and Day — Linked to Selection Above',
        width=700,
        height=250
    )

    # independent color scales so each chart uses its full range
    combined = alt.vconcat(crash_count_heatmap, injury_rate_heatmap).resolve_scale(
        color='independent'
    )

    combined.save('heatmap.html')
    print('Saved to heatmap.html')

def main():
    df = pd.read_csv('cleaned_boston_crashes.csv')
    create_heatmap(df)

if __name__ == '__main__':
    main()