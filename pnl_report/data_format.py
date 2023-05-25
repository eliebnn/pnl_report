import datetime as dt


class DataFormat:

    COLS = {'qty_col': 'qty', 'price_col': 'price', 'date_col': 'date', 'side_col': 'side',
            'unwind_price_col': 'unwind_price', 'pnl_col': 'pnl'}

    @staticmethod
    def s2q(df, cols=None):
        """Side to Quantity Sign"""
        cols = cols if cols else DataFormat.COLS
        df.loc[:, cols['qty_col']] = abs(df[cols['qty_col']])
        df.loc[df[cols['side_col']] == 'SELL', cols['qty_col']] = -df[cols['qty_col']]
        return df

    @staticmethod
    def q2s(df, cols=None):
        """Quantity Sign to Side"""
        cols = cols if cols else DataFormat.COLS
        df[cols['side_col']] = 'BUY'
        df.loc[df[cols['qty_col']] < 0, cols['side_col']] = 'SELL'
        return df

    @staticmethod
    def to_date(df, cols=None, date=None, **kwargs):
        cols = cols if cols else DataFormat.COLS

        if cols['date_col'] not in df.columns:
            date = dt.datetime.strptime(date, '%Y-%m-%d') if date else dt.datetime.now()
            df['_idx'] = list(range(1, df.shape[0] + 1))

            df[cols['date_col']] = df['_idx'].apply(lambda x: date + dt.timedelta(days=x)).dt.strftime('%Y-%m-%d')
            df = df.drop(columns=['_idx'])

        return df

    @staticmethod
    def fmt(df, cols=None, **kwargs):
        cols = cols if cols else DataFormat.COLS
        df = DataFormat.s2q(df, cols) if cols['side_col'] in df.columns else DataFormat.q2s(df, cols)
        return DataFormat.to_date(df, cols, **kwargs)
