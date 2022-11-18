import pandas as pd
import numpy as np
import random
from main import set_sessions
from datetime import timedelta, datetime
from pandas.core.base import PandasObject


def random_timestamp(range_days=1, range_hours=00):
    return datetime(2022, 1, 1, 00, 00, 00) + timedelta(days=range_days, hours=range_hours) * random.random()


def generate_df(rows_to_generate=1000, number_customers=10, number_products=100, write_csv=False, print_result=False):
    df = pd.DataFrame({'customer_id': np.random.randint(1, number_customers, rows_to_generate),
                       'product_id': np.random.randint(1, number_products, rows_to_generate),
                       'timestamp': sorted(random_timestamp() for _ in range(rows_to_generate))})

    set_sessions(df)

    if write_csv:
        df.to_csv("res.csv")
        print("csv written.")
    if print_result:
        print(df)


if __name__ == '__main__':
    df = pd.read_csv('data.csv', sep=';', parse_dates=['timestamp'],
                     dtype={'customer_id': np.uint32,
                            'product_id': np.uint32})
    PandasObject.set_sessions = set_sessions    # Делает из функции метод, который можно вызывать из датафрейма
    df.set_sessions()
    # generate_df() # - запустит генерацию датафрейма на 1к записей и проставит на нём сессии
    print(df.info())
