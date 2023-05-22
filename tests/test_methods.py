from pnl_report.methods import PnLMethods, FIFO, LIFO, AVG

import pandas as pd

if __name__ == '__main__':

    # Providing Price and Algebraic Quantity

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    fifo = FIFO(data=df).run()
    lifo = LIFO(data=df).run()
    avgr = AVG(data=df).run()

    wfifo = PnLMethods(data=df, method='fifo').run()
    wlifo = PnLMethods(data=df, method='lifo').run()
    wavgr = PnLMethods(data=df, method='avg').run()

    print(f"Pure Fifo pnl: {fifo.pnl}")
    print(f"Wrap Fifo pnl: {wfifo.pnl}")
    print('----')

    print(f"Pure Lifo pnl: {lifo.pnl}")
    print(f"Wrap Lifo pnl: {wlifo.pnl}")
    print('----')

    print(f"Pure Avg pnl: {avgr.pnl}")
    print(f"Wrap Avg pnl: {wavgr.pnl}")
    print('----')

    # Columns can be overridden
    # ----------------------------------

    # Providing Price and Algebraic Quantity

    df2 = pd.DataFrame()

    df2['MY_QTY_COL_NAME'] = [1, 2, 9, -5, -1, 2]
    df2['MY_PX_COL_NAME'] = [10, 12, 15, 12, 11, 12]

    fifo2 = FIFO(data=df2, price_col='MY_PX_COL_NAME', qty_col='MY_QTY_COL_NAME').run()
    # All columns that can be updated can be found in DataFormat.COLS

    print(f"Pure Fifo 2 pnl: {fifo2.pnl}")

    print()
