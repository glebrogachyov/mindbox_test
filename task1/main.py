import pandas as pd
import numpy as np


def set_sessions(df):
    if set(df.columns) != {"customer_id", "timestamp", "product_id"}:
        print('wrong column names')
        return 1
    if df.empty:
        print('dataframe is empty')
        return 1
    if df['timestamp'].dtype != 'datetime64[ns]':
        print('wrong "timestamp" data type')
        return 1
    df['session_id'] = np.dtype('uint32').type(0)

    current_min, one_min_old, two_min_old, three_min_old = dict(), dict(), dict(), dict()
    last_timestamp = df.loc[0, 'timestamp'].replace(second=0, microsecond=0)
    current_min['info'] = last_timestamp
    next_session_id = 0

    def get_last_session_id(customer_id, operation_timestamp) -> int or None:
        nonlocal current_min, one_min_old, two_min_old, three_min_old
        last_entry = current_min.get(customer_id, None) \
                     or one_min_old.get(customer_id, None) \
                     or two_min_old.get(customer_id, None) \
                     or three_min_old.get(customer_id, None)
        if last_entry:
            return last_entry[1] \
                if operation_timestamp - last_entry[0] <= pd.to_timedelta('00:03:00') else None
        return None

    def shift_dict(timestamp, *dictionaries):
        timedelta = timestamp - dictionaries[0]['info']
        if timedelta == pd.to_timedelta('00:01:00'):
            return dict(), *dictionaries[:3]
        if timedelta == pd.to_timedelta('00:02:00'):
            return dict(), dict(), *dictionaries[:2]
        if timedelta == pd.to_timedelta('00:03:00'):
            return dict(), dict(), dict(), dictionaries[0]
        else:
            return dict(), dict(), dict(), dict()

    for index, row in df.iterrows():
        current_timestamp = row['timestamp'].replace(second=0, microsecond=0)

        if current_timestamp != last_timestamp:
            current_min, one_min_old, two_min_old, three_min_old = shift_dict(current_timestamp,
                                                                              current_min, one_min_old, two_min_old)
            last_timestamp = current_timestamp
            current_min['info'] = last_timestamp

        tmp_session_id = get_last_session_id(row['customer_id'], row['timestamp'])

        if tmp_session_id is not None:
            df.loc[index, 'session_id'] = tmp_session_id
            current_min[row['customer_id']] = (row['timestamp'], tmp_session_id)
        else:
            df.loc[index, 'session_id'] = next_session_id
            current_min[row['customer_id']] = (row['timestamp'], next_session_id)
            next_session_id += 1
    return df


