import pandas as pd
import numpy as np


class PnLCore:

    COLS = {'qty_col': 'qty', 'price_col': 'price', 'date_col': 'date', 'side_col': 'side',
            'unwind_price_col': 'unwind_price', 'pnl_col': 'pnl'}

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

        # Queues
        self.queue = data.reset_index(drop=True).to_dict(orient='index')
        self.stack = []

        # Default column names
        _ = [self.__setattr__(k, v) for k, v in {**self.COLS, **kwargs}.items()]

        # Data
        self.raw_data = data
        self.pnls = pd.DataFrame(columns=['unwind_qty', self.unwind_price_col, self.price_col])

    # Properties

    @property
    def side(self):
        """Returns Side of current stack"""
        return self.stack[0][self.side_col]

    @property
    def stack_df(self):
        """Returns current stack as DataFrame, with cumulative position"""
        df = pd.DataFrame(self.stack)
        df['qty_cumsum'] = abs(df[self.qty_col]).cumsum()
        return df

    @property
    def qty(self):
        """Return current stack cumulated position"""
        return abs(sum([el[self.qty_col] for el in self.stack]))

    # Stack Functions

    def stack_munched(self, el):
        """Returns current stack as DataFrame, with cumulative position and level of stack being consumed
        by new batch"""
        df = self.stack_df
        df['munched'] = (df['qty_cumsum'] <= abs(el[self.qty_col])).shift(1).replace(np.NaN, True)
        return df

    def to_stack(self, el):
        pass

    # Quantity Checks

    def same_side(self, el):
        return True if el[self.side_col] == self.side else False

    def same_qty(self, el):
        return True if abs(el[self.qty_col]) == self.qty else False

    def less_qty(self, el):
        return True if abs(el[self.qty_col]) < self.qty else False

    def more_qty(self, el):
        return True if abs(el[self.qty_col]) > self.qty else False

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

        df = dm.loc[dm['munched'] == True]
        df_bal = df.copy().tail(1)
        dq = dm.loc[dm['munched'] == False]

        balance = max(df['qty_cumsum']) - abs(el[self.qty_col])

        df['unwind_date'] = el[self.date_col]
        df[self.unwind_price_col] = el[self.price_col]

        df['unwind_qty'] = df[self.qty_col].tolist()[:-1] + [abs(df_bal[self.qty_col].tolist()[0]) - balance]
        df_bal[self.qty_col] = abs(balance) if self.side == 'BUY' else -abs(balance)

        dq = pd.concat([df_bal, dq], sort=False, ignore_index=True)

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = list(dq.reset_index(drop=True).to_dict(orient='index').values())

    def same_qty_func(self, el):
        """New batch has same quantity than stacked one"""
        df = self.stack_df

        df[self.qty_col] = df[self.qty_col]
        df['unwind_qty'] = df[self.qty_col]
        df['unwind_date'] = el[self.date_col]
        df[self.unwind_price_col] = el[self.price_col]

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = []

    def more_qty_func(self, el):
        """New batch has more quantity than stacked one"""
        df = self.stack_df

        df[self.qty_col] = df[self.qty_col]
        df['unwind_qty'] = df[self.qty_col]
        df['unwind_date'] = el[self.date_col]
        df[self.unwind_price_col] = el[self.price_col]

        balance = abs(el[self.qty_col]) - max(df['qty_cumsum'])
        el[self.qty_col] = abs(balance) if el[self.side_col] == 'BUY' else -abs(balance)

        self.pnls = pd.concat([self.pnls, df], sort=False, ignore_index=True)
        self.stack = [el]

    # Results Functions

    def sanitize(self):
        """Removes process-related columns, and ensure quantities have proper sign"""
        if self.pnls.empty:
            return 0

        df = self.pnls
        df = df.drop(columns=['munched', 'qty_cumsum'], errors='ignore')

        df.loc[df[self.side_col] == 'BUY', 'unwind_qty'] = abs(df['unwind_qty'])
        df.loc[df[self.side_col] == 'SELL', 'unwind_qty'] = -abs(df['unwind_qty'])

        self.pnls = df

    def compute_pnls(self):
        """Computes the P&L"""
        self.pnls[self.pnl_col] = self.pnls['unwind_qty'] * \
                                  (self.pnls[self.unwind_price_col] - self.pnls[self.price_col])
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
        df = pd.DataFrame(self.stack)
        df['wgt_avg_px'] = df[self.qty_col] * df[self.price_col]

        dq = df.copy().head(1)
        dq[self.qty_col] = df[self.qty_col].sum()
        dq[self.price_col] = df['wgt_avg_px'].sum() / df[self.qty_col].sum()

        dq['qty_cumsum'] = abs(dq[self.qty_col]).cumsum()
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

    def __init__(self, data, method='fifo', **kwargs):
        self.calc = self.METHODS[method](data=data, **kwargs).run()

    # Properties

    @property
    def pnls(self):
        return self.calc.pnls


if __name__ == '__main__':

    df = pd.DataFrame()

    df['qty'] = [1, 2, 9, -5, -1, 2]
    df['price'] = [10, 12, 15, 12, 11, 12]

    df['side'] = 'BUY'
    df.loc[df['qty'] < 0, 'side'] = 'SELL'

    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-04', '2020-01-04']

    fifo = FIFO(data=df).run()
    lifo = LIFO(data=df).run()
    avgr = AVG(data=df).run()

    df = df.rename(columns={'price': 'foo_price'})

    calc = PnLMethods(data=df, method='fifo', price_col='foo_price')

    print(fifo.pnls[fifo.pnl_col].sum())
    print(lifo.pnls[lifo.pnl_col].sum())
    print(avgr.pnls[avgr.pnl_col].sum())
    print(calc.pnls[avgr.pnl_col].sum())

    print()
