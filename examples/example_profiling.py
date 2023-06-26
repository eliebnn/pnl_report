import cProfile
import datetime as dt
import io
import pstats
import random
from pstats import SortKey

import pandas as pd

from pnl_report.methods import FIFO

random.seed(1)


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


def main(size=5000):
    df = get_df(size=size)
    now = dt.datetime.now()

    FIFO(data=df.copy()).run()

    print('Time Taken:', (dt.datetime.now() - now).total_seconds(), 's')
    print()


def run(size=5000, max_output=10):
    print(f"\r\nProfiling for {size} Trades.")
    print('-----------------------------')
    pr = cProfile.Profile()
    pr.enable()

    main(size)

    pr.disable()
    s = io.StringIO()

    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME)
    ps.print_stats(max_output)

    print(s.getvalue())


if __name__ == '__main__':

    run(5000, max_output=10)
    run(15000, max_output=10)
    run(30000, max_output=20)
