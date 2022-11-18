import pandas as pd
import numpy as np
from main import set_sessions
from pandas.core.base import PandasObject
import unittest

PandasObject.set_sessions = set_sessions    # Делает из функции метод, который можно вызывать из датафрейма


class SetSessionTest(unittest.TestCase):
    def test_wrong_columns(self):
        test_df = pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})
        self.assertEqual(test_df.set_sessions(), 1)

    def test_timestamp_dtype(self):
        test_df = pd.DataFrame({'customer_id': [1], 'timestamp': [2], 'product_id': [3]})
        self.assertEqual(test_df.set_sessions(), 1)

    def test_empty_df(self):
        test_df = pd.DataFrame(columns=['customer_id', 'timestamp', 'product_id'])
        self.assertEqual(test_df.set_sessions(), 1)

    def test_solution_equals_true_ids(self):
        test_df = pd.read_csv('input_data.csv', parse_dates=['timestamp'],
                              dtype={'customer_id': np.uint32,
                                     'product_id': np.uint32,
                                     'true_session_id': np.uint32})
        true_ids = test_df['true_session_id']
        solution = set_sessions(test_df.drop(columns='true_session_id'))['session_id']
        self.assertTrue(true_ids.equals(solution))

