# P&L Report
The package allows to compute P&L Report using FIFO, LIFO and AVG calculation methods.

- FIFO: https://www.investopedia.com/terms/f/fifo.asp
- LIFO: https://www.investopedia.com/terms/l/lifo.asp
- AVG: https://www.investopedia.com/terms/a/averagecostmethod.asp

# Data Required

Required data is a DataFrame. Several set of columns are possibles:
1. Price, absolute quantity, side: side is either BUY or SELL
2. Price, algebraic quantity: +qty for BUY, -qty for SELL

You can also provide a date column. If None, one will be created containing 0, 1, 2, ..., N.

The repo will automatically add the missing columns, or data precision.

# Example

```python

```



