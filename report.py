from pnl_report.methods import PnLMethods

from functools import reduce
import pandas as pd
import numpy as np


class PnLReport:

    def __init__(self, data, id_col='ticker', method='fifo', **kwargs):

        self.raw_data = data
        self.pnls = pd.DataFrame()

        self.reports = {k: None for k in data[id_col].dropna().unique().tolist()}
        self.inputs = {**{'id_col': id_col, 'method': method}, **kwargs}
        self.cols = {**PnLMethods.COLS, **kwargs}

    # Properties

    @property
    def result_pnl(self):

        st_dt = min(self.pnls['unwind_date'])
        ed_dt = max(self.pnls['unwind_date'])
        ls = list(self.reports.keys())

        df = pd.DataFrame(index=pd.date_range(st_dt, ed_dt), columns=ls)
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

        for k in self.reports.keys():
            df = self.raw_data.loc[self.raw_data[self.inputs['id_col']] == k]
            self.reports[k] = PnLMethods(data=df, **self.inputs).run()

    def set_pnl(self):

        self.pnls = pd.DataFrame()

        for k in self.reports.keys():
            self.pnls = pd.concat([self.pnls, self.reports[k].pnls], sort=False).reset_index(drop=True)

        self.pnls = self.pnls.sort_values(by='unwind_date') if self.pnls.shape[1] else self.pnls

        return self

    def run(self):

        self.set_data()
        self.set_pnl()

        return self


if __name__ == '__main__':

    df = pd.DataFrame()

    df['qty'] = [10, 20, 9, -5, -1, -2, -10]
    df['price'] = [10, 12, 14, 25, 12, 12, 22.5]
    df['ticker'] = ['RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'RDSA LN', 'GOOG US', 'GOOG US']

    df['side'] = 'BUY'
    df.loc[df['qty'] < 0, 'side'] = 'SELL'

    df['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-05-04', '2020-06-10']

    rep = PnLReport(df).run()
    res = rep.result_pnl

    print()
