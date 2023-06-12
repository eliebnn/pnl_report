from pnl_report.methods import FIFO
from pnl_report.report import PnLReport
import pandas as pd

# -----


def example1():

    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]

    cls = FIFO(data=df).run()

    return cls


def example2():

    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, 5, 1, 2, 10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'SELL', 'SELL']

    cls = FIFO(data=df).run()

    return cls


def example3():

    df = pd.DataFrame()

    df['quantity'] = [12, 20, 9, 5, 1, 2, 10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'SELL', 'SELL']

    cls = FIFO(data=df, qty_col='quantity').run()

    return cls


def example4():
    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['ticker'] = ['RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'GOOG US']

    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-02-04', '2020-03-01', '2020-03-10']

    return PnLReport(df, extend_date=False).run()


def example5():
    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['ticker'] = ['RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'GOOG US']

    return PnLReport(df, extend_date=False).run()


def example6():
    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['ticker'] = ['RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'GOOG US']

    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-02-04', '2020-03-01', '2020-03-10']

    return PnLReport(df, extend_date=True).run()


if __name__ == '__main__':

    a = example1()
    b = example2()
    c = example3()
    d = example4()
    e = example5()
    f = example6()

    print(a.pnls == b.pnls)
    print(d.result_pnl.reset_index(drop=True) == e.result_pnl.reset_index(drop=True))
