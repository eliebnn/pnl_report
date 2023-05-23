from pnl_report.report import PnLReport

import pandas as pd


def test_1():
    # Providing Price, Algebraic Quantity and Dates

    df1 = pd.DataFrame()

    df1['qty'] = [1, 7, 9, -5, -1, 2, -2]
    df1['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    df1['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05', '2020-04-15']
    df1['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']

    report = PnLReport(data=df1, method='fifo').run()

    # Per Ticker Report

    df = report.reports['RDSA'].pnls

    tmp = pd.DataFrame({
        'unwind_qty': [1, 4, 2],
        'unwind_price': [8.5, 8.5, 35.2],
        'price': [10, 12, 12],
        'pnl': [-1.5, -14, 46.4],
        'qty': [1.0, 7.0, 3.0],
        'date': ['2020-01-01', '2020-01-02', '2020-01-02'],
        'ticker': ['RDSA'] * 3,
        'side': ['BUY'] * 3,
        'unwind_date': ['2020-01-04', '2020-01-04', '2020-04-15'],
    })

    df['pnl'] = df['pnl'].apply(lambda x: round(x, 2))
    tmp['pnl'] = tmp['pnl'].apply(lambda x: round(x, 2))

    df['price'] = df['price'].astype(float)
    tmp['price'] = tmp['price'].astype(float)

    df['unwind_qty'] = df['unwind_qty'].astype(float).apply(lambda x: round(x, 2))
    tmp['unwind_qty'] = tmp['unwind_qty'].astype(float).apply(lambda x: round(x, 2))

    assert df.equals(tmp)


def test_2():
    # Providing Price, Algebraic Quantity and Dates

    df1 = pd.DataFrame()

    df1['qty'] = [1, 7, 9, -5, -1, 2, -2]
    df1['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    df1['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05', '2020-04-15']
    df1['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']

    report = PnLReport(data=df1, method='fifo').run()

    # Per Ticker Report

    df = report.reports['GOOG'].pnls

    tmp = pd.DataFrame({
        'unwind_qty': [1.0],
        'unwind_price': [25.0],
        'price': [15.0],
        'pnl': [10.0],
        'qty': [9.0],
        'date': ['2020-01-03'],
        'ticker': ['GOOG'],
        'side': ['BUY'],
        'unwind_date': ['2020-04-04'],
    })

    df['pnl'] = df['pnl'].apply(lambda x: round(x, 2))
    tmp['pnl'] = tmp['pnl'].apply(lambda x: round(x, 2))

    df['price'] = df['price'].astype(float)
    tmp['price'] = tmp['price'].astype(float)

    df['unwind_qty'] = df['unwind_qty'].astype(float).apply(lambda x: round(x, 2))
    tmp['unwind_qty'] = tmp['unwind_qty'].astype(float).apply(lambda x: round(x, 2))

    assert df.equals(tmp)


# if __name__ == '__main__':

    # Providing Price, Algebraic Quantity and Dates

    # df1 = pd.DataFrame()
    #
    # df1['qty'] = [1, 7, 9, -5, -1, 2, -2]
    # df1['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    # df1['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05', '2020-04-15']
    # df1['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']
    #
    # report1 = PnLReport(data=df1, method='fifo').run()
    # result1 = report1.result_pnl
    #
    # # Per Ticker Report
    #
    # rdsa_pnl = report1.reports['RDSA']
    # goog_pnl = report1.reports['GOOG']
    #
    # # Providing Price and Algebraic Quantity. No Date.
    #
    # df2 = pd.DataFrame()
    #
    # df2['qty'] = [1, 7, 9, -5, -1, 2, -2]
    # df2['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    # df2['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']
    #
    # report2 = PnLReport(data=df2, method='fifo').run()
    # result2 = report2.result_pnl

    # print()
