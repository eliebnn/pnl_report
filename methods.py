from pnl_report.data_format import DataFormat

import pandas as pd
import numpy as np


class PnLCore:

    def __init__(self, data, **kwargs):
        """Init of the Core class of P&L Calculation.
        The data input needs to be a DataFrame, containing core columns:
        - A Quantity Column: The quantity of the trade. + for a Buy, - for a Sell
        - A Side Column: The side of the trade. BUY for a buy, SELL for a Sell
        - A Price Column: The price of the trade
        - A Date Column: When the trade happens

        See bottom for examples

        ---

        You can override default column names via kwargs.

        """
        # Default column names
        self.fmt = DataFormat
        self.cols = {k: v for k, v in {**self.fmt.COLS, **kwargs}.items()}

        # Queues
        self.queue = self.fmt.fmt(data, self.cols).reset_index(drop=True).to_dict(orient='index')
        self.stack = []

        # Data
        self.raw_data = data
        self.pnls = pd.DataFrame(columns=['unwind_qty', self.cols['unwind_price_col'],
                                          self.cols['price_col'], self.cols['pnl_col']])

    # Properties

    @property
    def pnl(self):
        return self.pnls[self.cols['pnl_col']].sum()

    @property
    def side(self):
        """Returns Side of current stack"""
        return self.stack[0][self.cols['side_col']] if self.stack else 'Stack Empty'

    @property
    def stack_df(self):
        """Returns current stack as DataFrame, with cumulative position"""

        if not self.stack:
            return pd.DataFrame()

        df = pd.DataFrame(self.stack)
        df['qty_cumsum'] = abs(df[self.cols['qty_col']]).cumsum()
        return df

    @property
    def qty(self):
        """Return current stack cumulated position"""
        return abs(sum([el[self.cols['qty_col']] for el in self.stack]))

    # Stack Functions

    def stack_munched(self, el):
        """Returns current stack as DataFrame, with cumulative position and level of stack being consumed
        by new batch"""
        df = self.stack_df
        df['munched'] = (df['qty_cumsum'] <= abs(el[self.cols['qty_col']])).shift(1).replace(np.NaN, True)
        return df

    def to_stack(self, el):
        pass

    # Quantity Checks

    def same_side(self, el):
        return True if el[self.cols['side_col']] == self.side else False

    def same_qty(self, el):
        return True if abs(el[self.cols['qty_col']]) == self.qty else False

    def less_qty(self, el):
        return True if abs(el[self.cols['qty_col']]) < self.qty else False

    def more_qty(self, el):
        return True if abs(el[self.cols['qty_col']]) > self.qty else False

    # Quantity Functions

    def less_qty_func(self, el):
        pass

    def same_qty_func(self, el):
        pass

    def more_qty_func(self, el):
        pass

    # Results Functions

    def compute_pnls(self):
        return self

    def run(self):
        return self


class PnLCalculation(PnLCore):

    def __init__(self, data, **kwargs):
        super().__init__(data=data, **kwargs)

    def less_qty_func(self, el):
        """New batch has less quantity than stacked one"""
        dm = self.stack_munched(el)

        df = dm.loc[dm['munched'] == True].drop(columns='munched')
        dq = dm.loc[dm['munched'] == False].drop(columns='munched')

        df_bal = df.copy().tail(1)

        balance = max(df['qty_cumsum']) - abs(el[self.cols['qty_col']])

        df['unwind_date'] = el[self.cols['date_col']]
        df[self.cols['unwind_price_col']] = el[self.cols['price_col']]

        df['unwind_qty'] = \
            df[self.cols['qty_col']].tolist()[:-1] + [abs(df_bal[self.cols['qty_col']].tolist()[0]) - balance]
        df_bal[self.cols['qty_col']] = abs(balance) if self.side == 'BUY' else -abs(balance)

        dq = pd.concat([df_bal, dq], sort=False, ignore_index=True)

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = list(dq.reset_index(drop=True).to_dict(orient='index').values())

    def same_qty_func(self, el):
        """New batch has same quantity than stacked one"""
        df = self.stack_df

        df[self.cols['qty_col']] = df[self.cols['qty_col']]
        df['unwind_qty'] = df[self.cols['qty_col']]
        df['unwind_date'] = el[self.cols['date_col']]
        df[self.cols['unwind_price_col']] = el[self.cols['price_col']]

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = []

    def more_qty_func(self, el):
        """New batch has more quantity than stacked one"""
        df = self.stack_df

        df[self.cols['qty_col']] = df[self.cols['qty_col']]
        df['unwind_qty'] = df[self.cols['qty_col']]
        df['unwind_date'] = el[self.cols['date_col']]
        df[self.cols['unwind_price_col']] = el[self.cols['price_col']]

        balance = abs(el[self.cols['qty_col']]) - max(df['qty_cumsum'])
        el[self.cols['qty_col']] = abs(balance) if el[self.cols['side_col']] == 'BUY' else -abs(balance)

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = [el]

    # Results Functions

    def sanitize(self):
        """Removes process-related columns, and ensure quantities have proper sign"""
        if self.pnls.empty:
            return 0

        df = self.pnls
        df = df.drop(columns=['munched', 'qty_cumsum'], errors='ignore')

        df.loc[df[self.cols['side_col']] == 'BUY', 'unwind_qty'] = abs(df['unwind_qty'])
        df.loc[df[self.cols['side_col']] == 'SELL', 'unwind_qty'] = -abs(df['unwind_qty'])

        self.pnls = df

    def compute_pnls(self):
        """Computes the P&L"""
        self.pnls[self.cols['pnl_col']] = \
            self.pnls['unwind_qty'] * (self.pnls[self.cols['unwind_price_col']] - self.pnls[self.cols['price_col']])
        return self

    def run(self):
        """Runs the various steps, going through each batch"""
        for el in self.queue.values():

            if not self.stack:
                self.to_stack(el)
                continue

            if self.same_side(el):
                self.to_stack(el)
                continue

            if self.less_qty(el):
                self.less_qty_func(el)
                continue

            if self.same_qty(el):
                self.same_qty_func(el)
                continue

            if self.more_qty(el):
                self.more_qty_func(el)
                continue

        self.sanitize()
        self.compute_pnls()

        return self

# ----------------------
# Calculations Methods -
# ----------------------


class FIFO(PnLCalculation):
    """FIRST IN FIRST OUT"""
    def __init__(self, data, **kwargs):
        super().__init__(data=data, **kwargs)

    # Stack Functions

    def to_stack(self, el):
        self.stack.append(el)


class LIFO(PnLCalculation):
    """LAST IN FIRST OUT"""
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

    # Stack Functions

    def to_stack(self, el):
        self.stack.insert(0, el)


class AVG(PnLCalculation):
    """AVERAGED AS THEY COME"""
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

    # Properties

    @property
    def stack_df(self):
        """Overrides to average every new batch into the existing batch"""

        if not self.stack:
            return pd.DataFrame()

        df = pd.DataFrame(self.stack)
        df['wgt_avg_px'] = df[self.cols['qty_col']] * df[self.cols['price_col']]

        dq = df.copy().head(1)
        dq[self.cols['qty_col']] = df[self.cols['qty_col']].sum()
        dq[self.cols['price_col']] = df['wgt_avg_px'].sum() / df[self.cols['qty_col']].sum()

        dq['qty_cumsum'] = abs(dq[self.cols['qty_col']]).cumsum()
        return dq.drop(columns=['wgt_avg_px'])

    # Stack Functions

    def to_stack(self, el):
        self.stack.append(el)

# ----------------------
# Calculations Wrapper -
# ----------------------


class PnLMethods:
    """Wrapper for the various Calculation Methods"""
    METHODS = {'fifo': FIFO, 'lifo': LIFO, 'avg': AVG}
    COLS = DataFormat.COLS

    def __init__(self, data, method='fifo', **kwargs):
        self.calc = self.METHODS[method](data=data, **kwargs)

    def run(self):
        return self.calc.run()


if __name__ == '__main__':

    foo = pd.DataFrame()

    foo['qty'] = [1, 2, 9, -5, -1, 2]
    foo['price'] = [10, 12, 15, 12, 11, 12]

    bar = DataFormat.fmt(foo, DataFormat.COLS)

    foo['side'] = 'BUY'
    foo.loc[foo['qty'] < 0, 'side'] = 'SELL'

    foo['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05']

    fifo = FIFO(data=foo).run()
    lifo = LIFO(data=foo).run()
    avgr = AVG(data=foo).run()

    foo = foo.rename(columns={'price': 'foo_price'})

    calc = PnLMethods(data=foo, method='fifo', price_col='foo_price').run()

    print(fifo.pnls[fifo.cols['pnl_col']].sum())
    print(lifo.pnls[lifo.cols['pnl_col']].sum())
    print(avgr.pnls[avgr.cols['pnl_col']].sum())
    print(calc.pnls[avgr.cols['pnl_col']].sum())

    print()
