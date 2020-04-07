import pandas as pd


def to_record(row, prev_day, key):
    new = row[key] - prev_day[key]
    record = {
        'date': row['date'],
        'state': row['state'],
        'fips': row['fips'],
        'new': new,
        'value': row[key],
        'type': key
    }
    if prev_day[key] > 0:
        record['growth'] = new / float(prev_day[key])
    return record


def project_data(file_name, num_days):
    data = pd.read_csv(file_name + ".csv")
    data['date'] = pd.to_datetime(data['date'])
    new_data = []
    prev_day_by_fips = {}

    for index, row in reversed(data.iterrows()):
        fips = row['fips']
        prev_day = prev_day_by_fips.get(fips)
        if prev_day is None:
            prev_day_by_fips[fips] = row
            continue

        new_data.append(to_record(row, prev_day, 'cases'))
        new_data.append(to_record(row, prev_day, 'deaths'))
        prev_day_by_fips[fips] = row

    df = pd.DataFrame(new_data)
    df.to_csv(file_name + "-normalized.csv", index=False, header=True)


project_data('us-states', num_days)
