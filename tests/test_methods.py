from pnl_report.methods import PnLMethods, FIFO, LIFO, AVG

import pandas as pd


def test_1():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    fifo = FIFO(data=df).run()

    assert [k['pnl'] for k in fifo.pnls] == [2, 0, -6, -4]


def test_2():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    lifo = LIFO(data=df).run()
    assert [k['pnl'] for k in lifo.pnls] == [-15, -4]


def test_3():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    avgr = AVG(data=df).run()

    ls = [round(k['pnl'], 2) for k in avgr.pnls]

    assert ls == [-10.42, -3.08]


def test_4():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    df2 = pd.DataFrame()

    df2['qty'] = [1, 2, 9, -5, -1, 2]
    df2['price'] = [10, 12, 15, 12, 11, 12]

    fifo = FIFO(data=df).run()
    wfifo = PnLMethods(data=df2, method='fifo').run()

    assert fifo.pnls == wfifo.pnls


def test_5():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    df2 = pd.DataFrame()

    df2['qty'] = [1, 2, 9, -5, -1, 2]
    df2['price'] = [10, 12, 15, 12, 11, 12]

    lifo = LIFO(data=df).run()
    wlifo = PnLMethods(data=df2, method='lifo').run()

    assert lifo.pnls == wlifo.pnls


def test_6():

    df = pd.DataFrame()
    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    df2 = pd.DataFrame()
    df2['qty'] = [1, 2, 9, -5, -1, 2]
    df2['price'] = [10, 12, 15, 12, 11, 12]

    avgr = AVG(data=df).run()
    wavgr = PnLMethods(data=df2, method='avg').run()

    assert avgr.pnls == wavgr.pnls


def test_7():

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    fifo = FIFO(data=df).run()

    df2 = pd.DataFrame()

    df2['MY_QTY_COL_NAME'] = [1, 2, 9, -5, -1, 2]
    df2['MY_PX_COL_NAME'] = [10, 12, 15, 12, 11, 12]

    fifo2 = FIFO(data=df2, price_col='MY_PX_COL_NAME', qty_col='MY_QTY_COL_NAME').run()

    assert [k['price'] for k in fifo.pnls] == [k['MY_PX_COL_NAME'] for k in fifo2.pnls]
    assert [k['qty'] for k in fifo.pnls] == [k['MY_QTY_COL_NAME'] for k in fifo2.pnls]
