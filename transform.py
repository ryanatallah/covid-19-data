from matplotlib import pyplot as plt
import csv
import pandas as pd

def transform_data(in_file, out_file, min_cases):
    data = pd.read_csv(in_file);
    data['date'] = pd.to_datetime(data['date'])
    new_data = []
    first_day_by_fips = {}
    prev_day_by_fips = {}

    for index, row in data.iterrows():
        fips = row['fips']
        prev_day = prev_day_by_fips.get(fips)
        if prev_day is None:
            prev_day_by_fips[fips] = row
            continue
        if row['cases'] >= min_cases:
            first_day = first_day_by_fips.get(fips)
            if first_day == None:
                first_day = row['date']
                first_day_by_fips[fips] = first_day
            delta = row['date']-first_day
            new_row = row
            new_row['day_num'] = delta.days
            new_cases = row['cases'] - prev_day['cases']
            new_row['new_cases'] = new_cases
            if prev_day['cases'] > 0:
                new_row['cases_growth'] = new_cases / float(prev_day['cases'])
            new_deaths = row['deaths'] - prev_day['deaths']
            new_row['new_deaths'] = new_deaths
            if prev_day['deaths'] > 0:
                new_row['deaths_growth'] = new_deaths / float(prev_day['deaths'])
            new_data.append(new_row)
        prev_day_by_fips[fips] = row

    df = pd.DataFrame(new_data)
    df.to_csv(out_file, index=False, header=True)


transform_data('us-states.csv', 'us-states-normalized.csv', 100)
transform_data('us-counties.csv', 'us-counties-normalized.csv', 48)
