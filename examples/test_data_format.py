from pnl_report.data_format import DataFormat

import pandas as pd


if __name__ == '__main__':

    # Providing Price and Algebraic Quantity

    df1 = pd.DataFrame()

    df1['qty'] = [1, 2, 9, -5, -1, 2]
    df1['price'] = [10, 12, 15, 12, 11, 12]

    df1 = DataFormat.fmt(df1, DataFormat.COLS)

    # Providing Price and Absolute Quantity, and Side

    df2 = pd.DataFrame()

    df2['qty'] = [1, 2, 9, 5, 1, 2]
    df2['price'] = [10, 12, 15, 12, 11, 12]
    df2['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']

    df2 = DataFormat.fmt(df2, DataFormat.COLS)

    # Providing Price and Algebraic Quantity, Side and Date

    df3 = pd.DataFrame()

    df3['qty'] = [1, 2, 9, -5, -1, 2]
    df3['price'] = [10, 12, 15, 12, 11, 12]
    df3['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']
    df3['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05']

    df3 = DataFormat.fmt(df3, DataFormat.COLS)

    print()
