from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1] / "shared"
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])
advisors = pd.read_csv(BASE / "advisors.csv")

# TODO:
# 1. groupby("client_name")["value"].agg(["count", "sum", "mean"])
print("Value by Client", trades.groupby('client_name')['value'].agg(['count', 'sum', 'mean']))

# 2. pivot_table: index=instrument, columns=side, values=value, aggfunc=sum, fill_value=0
print("\nPivot Table\n", trades.pivot_table(index='instrument', columns='side', values='value', aggfunc='sum', fill_value=0))

# 3. merge trades with advisors on "advisor", then total value by team
merged = trades.merge(advisors, on='advisor', how='left')

# 4. set_index("trade_date") and resample("W")["value"].sum()
date_index = trades.set_index('trade_date')
print(f"\nWeekly Total Value", date_index.resample('W')['value'].sum())

# 5. 3-5 one-line takeaways as comments, each citing a specific number above
"""
1. The agg() function makes it easier to view more useful data in the same place.
2. The pivot table so efficiently mimics an Excel pivot table, 
and given more dynamism in the variables, it would be such a useful function.
3. Similarly, merge is a very 'English' way of making a join that just works.
"""