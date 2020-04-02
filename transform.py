import pandas as pd


def to_record(first_day, row, prev_day, key):
    delta = row['date']-first_day
    new = row[key] - prev_day[key]
    record = {
        'date': row['date'],
        'state': row['state'],
        'fips': row['fips'],
        'day_num': delta.days,
        'new': new,
        'value': row[key],
        'type': key
    }
    if prev_day[key] > 0:
        record['growth'] = new / float(prev_day[key])
    return record


def transform_data(in_file, out_file, min_cases):
    data = pd.read_csv(in_file)
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
            if first_day is None:
                first_day = row['date']
                first_day_by_fips[fips] = first_day

            new_data.append(to_record(first_day, row, prev_day, 'cases'))
            new_data.append(to_record(first_day, row, prev_day, 'deaths'))
        prev_day_by_fips[fips] = row

    df = pd.DataFrame(new_data)
    df.to_csv(out_file, index=False, header=True)


transform_data('us-states.csv', 'us-states-normalized.csv', 100)
