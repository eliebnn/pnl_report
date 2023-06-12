import datetime as dt

import pandas as pd

from pnl_report.data_format import DataFormat


def test_1():
    # Providing Price and Algebraic Quantity
    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    ls = list(range(1, 7))

    df = DataFormat.fmt(df, DataFormat.COLS)
    tmp = pd.DataFrame({
        'qty': [1, 2, 9, -5, -1, 2],
        'price': [10, 12, 15, 12, 11, 12],
        'side': ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY'],
        'date': ls,
    })

    assert df.equals(tmp)


def test_2():
    # Providing Price and Absolute Quantity, and Side
    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, 5, 1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]
    df['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']

    ls = list(range(1, 7))

    df = DataFormat.fmt(df, DataFormat.COLS)
    tmp = pd.DataFrame({
        'qty': [1, 2, 9, -5, -1, 2],
        'price': [10, 12, 15, 12, 11, 12],
        'side': ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY'],
        'date': ls,
    })

    assert df.equals(tmp)


def test_3():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]
    df['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']
    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05']

    df = DataFormat.fmt(df, DataFormat.COLS)

    tmp = pd.DataFrame({
        'qty': [1, 2, 9, -5, -1, 2],
        'price': [10, 12, 15, 12, 11, 12],
        'side': ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY'],
        'date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05'],
    })

    assert df.equals(tmp)
