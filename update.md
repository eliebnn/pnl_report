# Updates

- **19/06/2023**: fixed stack_munched & less_qty_func. [+2, +5, -2] queue of trades would have created an erroneous results, as -2 unwind has less than +2+5=+7, but has exact same number as +2. The resulting indexing used to be wrong. 