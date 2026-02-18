import pandas as pd 
import numpy as np

def get_data():
    df = pd.read_csv('2025_Crashes.csv', low_memory = False)

    df = df[df['CITY_TOWN_NAME'] == 'BOSTON'].copy()

    # remove rows where features are unknown/not reported
    df = df[df['CRASH_SEVERITY_DESCR'] != 'Unknown']
    df = df[df['WEATH_COND_DESCR'] != 'Not reported']
    df = df[df['WEATH_COND_DESCR'] != 'Unknown']
    df = df[df['ROAD_SURF_COND_DESCR'] != 'Not reported']
    df = df[df['ROAD_SURF_COND_DESCR'] != 'Unknown']
    df = df[df['AMBNT_LIGHT_DESCR'] != 'Not reported']
    df = df[df['AMBNT_LIGHT_DESCR'] != 'Unknown']
    
    # dropping rows with null values for lat and lon columns
    df = df.dropna(subset = ('LAT', 'LON'))

    # creating binary severity variable - 1 for any type of injury 0 if just property damage
    df['IS_SEVERE'] = df['CRASH_SEVERITY_DESCR'].apply(
        lambda x: 1 if 'injury' in x.lower() or 'fatal' in x.lower() else 0
    )

    # parse datetime and get time features
    df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATETIME'])
    df['MONTH'] = df['CRASH_DATE'].dt.month_name()
    df['DAY_OF_WEEK'] = df['CRASH_DATE'].dt.day_name()
    df['HOUR'] = df['CRASH_DATE'].dt.hour

    # if weekend then 1 if not 0
    df['IS_WEEKEND'] = df['DAY_OF_WEEK'].isin(['Saturday', 'Sunday']).astype(int)

    # simplifying weather
    df['WEATHER_SIMPLE'] = df['WEATH_COND_DESCR'].apply(simplify_weather)
    df['ROAD_SIMPLE'] = df['ROAD_SURF_COND_DESCR'].apply(simplify_road)
    df['LIGHTING_SIMPLE'] = df['AMBNT_LIGHT_DESCR'].apply(simplify_light)

    # creating NaN values for values that are NULL in speed limit column
    df['SPEED_LIMIT'] = pd.to_numeric(df['SPEED_LIMIT'], errors = 'coerce')

    # initial dataset has too many features
    specific_cols = [
        'CRASH_NUMB', 'CRASH_DATE', 'HOUR', 'DAY_OF_WEEK', 'MONTH', 'IS_WEEKEND',
        'CRASH_SEVERITY_DESCR', 'IS_SEVERE',
        'NUMB_VEHC', 'NUMB_NONFATAL_INJR', 'NUMB_FATAL_INJR',
        'WEATH_COND_DESCR', 'WEATHER_SIMPLE',
        'ROAD_SURF_COND_DESCR', 'ROAD_SIMPLE',
        'AMBNT_LIGHT_DESCR', 'LIGHTING_SIMPLE',
        'MANR_COLL_DESCR', 'SPEED_LIMIT',
        'RDWY_JNCT_TYPE_DESCR', 'TRAF_CNTRL_DEVC_TYPE_DESCR',
        'LAT', 'LON'
    ]
    
    df = df[specific_cols]

    return df

def simplify_weather(w):
    """Simplifying weather/environmental conditions"""
    w = str(w).lower()

    if 'clear' in w:
        return 'Clear'
    elif 'rain' in w:
        return 'Rain'
    elif 'snow' in w or 'sleet' in w or 'blizzard' in w:
        return 'Snow/Ice'
    elif 'cloud' in w or 'overcast' in w:
        return 'Cloudy'
    elif 'fog' in w:
        return 'Fog'
    else:
        return 'Other'


def simplify_road(r):
    """Simplifying road conditions - mostly combining ice features"""
    r = str(r).lower()
    if 'dry' in r:
        return 'Dry'
    elif 'wet' in r:
        return 'Wet'
    elif 'snow' in r or 'ice' in r or 'slush' in r:
        return 'Snow/Ice'
    else:
        return 'Other'


def simplify_light(l):
    """Combining/creating lighting categories"""
    l = str(l).lower()
    if 'daylight' in l:
        return 'Daylight'
    elif 'dark' in l and 'lighted' in l:
        return 'Dark - Lighted'
    elif 'dark' in l:
        return 'Dark - Unlighted'
    elif 'dawn' in l or 'dusk' in l:
        return 'Dawn/Dusk'
    else:
        return 'Other'

def main():

    df = get_data()
    df.to_csv('cleaned_boston_crashes.csv')
    print('saved to cleaned_boston_crashes.csv')
    print(df.shape)
    
if __name__ == '__main__':
    main()