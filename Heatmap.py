
# heatmap
def hour_vs_day_heatmap(df):
    """Altair heatmap - hour of day vs day of week, colored by crash count and injury rate.
    Saves both heatmaps to a single HTML file.
    """

    plot_df = df.copy()
    plot_df['TOTAL_INJURIES'] = plot_df['NUMB_NONFATAL_INJR'] + plot_df['NUMB_FATAL_INJR']

    # aggregate by hour and day of week
    agg = plot_df.groupby(['HOUR', 'DAY_OF_WEEK']).agg(
        crash_count = ('CRASH_NUMB', 'count'),
        total_injuries = ('TOTAL_INJURIES', 'sum')
    ).reset_index()

    agg['injury_rate'] = agg['total_injuries'] / agg['crash_count']

    # ordered days for the y axis
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    crash_count_heatmap = alt.Chart(agg).mark_rect().encode(
        x = alt.X('HOUR:O',
                  title = 'Hour of Day (0 = Midnight)',
                  sort = list(range(24)),
                  axis = alt.Axis(labelAngle = 0)),
        y = alt.Y('DAY_OF_WEEK:O',
                  title = 'Day of Week',
                  sort = day_order),
        color = alt.Color('crash_count:Q',
                          title = 'Crash Count',
                          scale = alt.Scale(scheme = 'orangered')),
        tooltip = [
            alt.Tooltip('DAY_OF_WEEK:O', title = 'Day'),
            alt.Tooltip('HOUR:O', title = 'Hour'),
            alt.Tooltip('crash_count:Q', title = 'Crash Count'),
            alt.Tooltip('injury_rate:Q', title = 'Injury Rate', format = '.3f')
        ]
    ).properties(
        title = 'Crash Count by Hour and Day (Boston, 2025)',
        width = 700,
        height = 300
    )

    injury_rate_heatmap = alt.Chart(agg).mark_rect().encode(
        x = alt.X('HOUR:O',
                  title = 'Hour of Day (0 = Midnight)',
                  sort = list(range(24)),
                  axis = alt.Axis(labelAngle = 0)),
        y = alt.Y('DAY_OF_WEEK:O',
                  title = 'Day of Week',
                  sort = day_order),
        color = alt.Color('injury_rate:Q',
                          title = 'Injury Rate',
                          scale = alt.Scale(scheme = 'purplered', domain = [0, 1])),
        tooltip = [
            alt.Tooltip('DAY_OF_WEEK:O', title = 'Day'),
            alt.Tooltip('HOUR:O', title = 'Hour'),
            alt.Tooltip('crash_count:Q', title = 'Crash Count'),
            alt.Tooltip('injury_rate:Q', title = 'Injury Rate', format = '.3f')
        ]
    ).properties(
        title = 'Injury Rate by Hour and Day (Boston, 2025)',
        width = 700,
        height = 250
    )

    # independent color scales so each chart uses its full range
    combined = alt.vconcat(crash_count_heatmap, injury_rate_heatmap).resolve_scale(
        color = 'independent'
    )
    combined.save('hour_vs_day_heatmap.html')