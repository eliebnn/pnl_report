from pnl_report.methods import FIFO, LIFO, AVG
import random
import datetime as dt
import pandas as pd

random.seed(1)


def run(size=5000, itr=10):
    print()
    print(f"----------------------------------------------")
    print(f"Run with - size: {size}, iter: {itr}")
    df = get_df(size)
    run_fifo(df, itr)
    run_lifo(df, itr)
    run_avg(df, itr)


def get_df(size=5000):
    ls_qty = random.sample(range(-20, 55), 50) * int(2 * size / 100)
    ls_prx = random.sample(range(10, 30), 20) * int(5 * size / 100)

    random.shuffle(ls_qty)
    random.shuffle(ls_prx)

    foo = pd.DataFrame({'qty': ls_qty, 'price': ls_prx})
    foo['side'] = 'BUY'
    foo.loc[foo['qty'] < 0, 'side'] = 'SELL'

    foo.loc[foo['qty'] == 0, 'qty'] = 10
    foo.loc[foo['price'] == 0, 'price'] = 20
    return foo.reset_index(drop=True)


def run_fifo(df, itr=10):
    ls = []
    for i in range(0, itr):
        now = dt.datetime.now()

        FIFO(data=df.copy()).run()

        t = (dt.datetime.now() - now).total_seconds()
        ls.append(t)

    print('FIFO -', f'{df.shape[0]} Trades -', round(sum(ls) / len(ls), 3), 's')


def run_lifo(df, itr=10):
    ls = []
    for i in range(0, itr):
        now = dt.datetime.now()

        LIFO(data=df.copy()).run()

        t = (dt.datetime.now() - now).total_seconds()
        ls.append(t)

    print('LIFO -', f'{df.shape[0]} Trades -', round(sum(ls) / len(ls), 3), 's')


def run_avg(df, itr=10):
    ls = []
    for i in range(0, itr):
        now = dt.datetime.now()

        AVG(data=df.copy()).run()

        t = (dt.datetime.now() - now).total_seconds()
        ls.append(t)

    print('AVG  -', f'{df.shape[0]} Trades -', round(sum(ls) / len(ls), 3), 's')


if __name__ == '__main__':
    run(1000, 10)
    run(2500, 10)
    run(5000, 10)
    run(10000, 5)
    run(20000, 5)
