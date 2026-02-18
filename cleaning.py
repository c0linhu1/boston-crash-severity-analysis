import pandas as pd 
import numpy as np

def get_data():
    df = pd.read_csv('2025_Crashes.csv', low_memory = False)

    df = df[df['CITY_TOWN_NAME'] == 'BOSTON'].copy()

    return df


def main():

    df = get_data()
    #df.to_csv('boston_crashes.csv')
    # print('saved to boston_crashes.csv')
    print(df.shape)
if __name__ == '__main__':
    main()