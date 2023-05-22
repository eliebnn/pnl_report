# P&L Report
The package allows to compute P&L Report using FIFO, LIFO and AVG calculation methods.

- FIFO: https://www.investopedia.com/terms/f/fifo.asp
- LIFO: https://www.investopedia.com/terms/l/lifo.asp
- AVG: https://www.investopedia.com/terms/a/averagecostmethod.asp

# Dependencies

Dependencies: pandas, numpy, functools

# Data Required

Required data is a DataFrame. Several set of columns are possibles:
1. Price, absolute quantity, side: side is either BUY or SELL
2. Price, algebraic quantity: +qty for BUY, -qty for SELL

You can also provide a date column. If None, one will be created containing 0, 1, 2, ..., N.

The repo will automatically add the missing columns, or data precision.

**Note**: There is no filtering nor sorting based on date values. Rows are processed as they come. MAke sure your 
DataFrame is properly sorted beforehand.

# Example

Examples can be found for:
- Data Format: pnl_report.examples.test_data_format.py
- Calculation Methods: pnl_report.examples.test_methods.py
- Report: pnl_report.examples.test_report.py

### Data Format

```python
from pnl_report.data_format import DataFormat
import pandas as pd

df1 = pd.DataFrame()

df1['qty'] = [1, 2, 9, -5, -1, 2]
df1['price'] = [10, 12, 15, 12, 11, 12]

df1 = DataFormat.fmt(df1, DataFormat.COLS)

# Providing Price and Absolute Quantity, and Side

df2 = pd.DataFrame()

df2['qty'] = [1, 2, 9, 5, 1, 2]
df2['price'] = [10, 12, 15, 12, 11, 12]
df2['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']

df2 = DataFormat.fmt(df2, DataFormat.COLS)

# Providing Price and Algebraic Quantity, Side and Date

df3 = pd.DataFrame()

df3['qty'] = [1, 2, 9, -5, -1, 2]
df3['price'] = [10, 12, 15, 12, 11, 12]
df3['side'] = ['BUY', 'BUY', 'BUY', 'SELL', 'SELL', 'BUY']
df3['date'] = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-04-04', '2020-04-05']

df3 = DataFormat.fmt(df3, DataFormat.COLS)
```

### Calculation Methods

```python
from pnl_report.methods import PnLMethods, FIFO, LIFO, AVG
import pandas as pd

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
```

### P&L Report

```python
from pnl_report.report import PnLReport
import pandas as pd

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
```


