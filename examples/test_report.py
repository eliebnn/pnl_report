from pnl_report.report import PnLReport

import pandas as pd

if __name__ == '__main__':

    # Providing Price, Algebraic Quantity and Dates

    df1 = pd.DataFrame()

    df1['qty'] = [1, 7, 9, -5, -1, 2, -2]
    df1['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    df1['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05', '2020-04-15']
    df1['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']

    report1 = PnLReport(data=df1, method='fifo').run()
    result1 = report1.result_pnl

    # Per Ticker Report

    rdsa_pnl = report1.reports['RDSA']
    goog_pnl = report1.reports['GOOG']

    # Providing Price and Algebraic Quantity. No Date.

    df2 = pd.DataFrame()

    df2['qty'] = [1, 7, 9, -5, -1, 2, -2]
    df2['price'] = [10, 12, 15, 8.5, 25, 12, 35.2]
    df2['ticker'] = ['RDSA', 'RDSA', 'GOOG', 'RDSA', 'GOOG', 'GOOG', 'RDSA']

    report2 = PnLReport(data=df2, method='fifo').run()
    result2 = report2.result_pnl

    print()
