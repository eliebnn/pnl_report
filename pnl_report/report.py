from pnl_report.methods import PnLMethods, DataFormat

from functools import reduce
import pandas as pd
import numpy as np


class PnLReport:

    def __init__(self, data, id_col='ticker', method='fifo', **kwargs):

        self.raw_data = data
        self.pnls = pd.DataFrame()

        self.reports = {k: None for k in data[id_col].dropna().unique().tolist()}
        self.inputs = {**{'id_col': id_col, 'method': method}, **kwargs}
        self.cols = {**DataFormat.COLS, **kwargs}

    # Properties

    @property
    def result_pnl(self):
        """Returns a DF, with unwind dates as index, with P&L time series for each ticker"""
        st_dt = min(self.pnls['unwind_date'])
        ed_dt = max(self.pnls['unwind_date'])
        ls = list(self.reports.keys())

        idx = range(int(st_dt), int(ed_dt) + 1) if isinstance(st_dt, (int, float)) else pd.date_range(st_dt, ed_dt)
        df = pd.DataFrame(index=idx, columns=ls)

        dfs = [df]

        for c in ls:
            sub_df = self.reports[c].pnls

            if sub_df.shape[0]:
                sub_df = sub_df.loc[sub_df['unwind_date'] >= st_dt]
                sub_df['pnl_cumsum'] = sub_df[self.cols['pnl_col']].cumsum()
                sub_df = sub_df.drop_duplicates(subset=['unwind_date'], keep='last')
                sub_df = sub_df[['unwind_date', 'pnl_cumsum']].groupby('unwind_date').sum()
                sub_df = sub_df.rename(columns={'pnl_cumsum': c})

                dfs.append(sub_df)

        df = reduce(lambda l, r: l.drop(columns=[r.columns[0]]).merge(r, left_index=True, right_index=True,
                                                                      how='left'), dfs).ffill().replace(np.NaN, 0)

        df['pnl_total'] = df.sum(axis=1)

        return df

    # Data Functions

    def set_data(self):
        """Sets the trade data for each ticker"""
        for k in self.reports.keys():
            df = self.raw_data.loc[self.raw_data[self.inputs['id_col']] == k]
            self.reports[k] = PnLMethods(data=df, **self.inputs).run()

    def set_pnl(self):
        """Set P&L DataFrame attribute by concat P&L of each ticker"""
        self.pnls = pd.DataFrame()

        for k in self.reports.keys():
            self.pnls = pd.concat([self.pnls, self.reports[k].pnls], sort=False).reset_index(drop=True)

        self.pnls = self.pnls.sort_values(by='unwind_date') if self.pnls.shape[1] else self.pnls

        return self

    def run(self):

        self.set_data()
        self.set_pnl()

        return self

    def clean(self):
        """Cleaning the dataset keeps open trades, by keeping stacked content."""
        raw_data_ls = []

        for k in self.reports.keys():
            df = self.reports[k].stack_df.drop(columns=['qty_cumsum'], errors='ignore')
            self.reports[k] = PnLMethods(data=df, **self.inputs).run()
            raw_data_ls.append(df)

        self.raw_data = pd.concat(raw_data_ls, sort=False, ignore_index=True)

        return self


class PnLProjection(PnLReport):
    """To be used to assess the P&L resulting in potential trades"""
    def __init__(self, data, trades, **kwargs):
        super().__init__(data=data, **kwargs)
        self._trades = trades
        super().run().clean()
        self.run()

    @property
    def trades(self):
        """If no date column is provided, it will take the max existing one from raw_data, plus cumulative days"""
        return DataFormat.fmt(df=self._trades.copy(), cols=self.cols)

    def run(self):
        """Computes P&L based on potential trades. It cleans the data set first, aka it keeps only open trades"""
        ls = set(list(self.reports.keys())).difference(set(self.trades[self.inputs['id_col']].unique().tolist()))
        _ = [self.reports.pop(k) for k in ls]

        self.raw_data = pd.concat([self.raw_data, self.trades], sort=False, ignore_index=True)
        super().run()
        self.print()

        return self

    def print(self):
        """Prints the P&L results per ticker"""
        res = self.result_pnl.tail(1).reset_index(drop=True).to_dict(orient='index')[0]
        _ = [print(f"Projected P&L for {k}: {v}") for k, v in res.items()]


if __name__ == '__main__':

    df = pd.DataFrame()

    df['qty'] = [12, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['ticker'] = ['RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'GOOG US']

    df['side'] = 'BUY'
    df.loc[df['qty'] < 0, 'side'] = 'SELL'

    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-05-04', '2020-06-10']

    rep = PnLReport(df).run().clean()
    res = rep.result_pnl

    # P&L Projection

    dq = pd.DataFrame()

    dq['qty'] = [-3, -2, -5]
    dq['price'] = [10, 12, 14]
    dq['ticker'] = ['GOOG US', 'RDSA LN', 'RDSA LN']

    proj = PnLProjection(df, trades=dq)

    print()
