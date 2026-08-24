from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "trades.csv"

# TODO:
# 1. Load DATA_PATH into a DataFrame.
df = pd.read_csv(DATA_PATH)
print("First 5 Rows")
print(df.head())

# 2. Select SELL-only trades (trade_id, client_name, value) using .loc + boolean indexing.
print("\nSELL-only Trades")
print(df.loc[df['side'] == 'SELL', ['trade_id', 'side', 'client_name', 'value']])

# 3. groupby("client_name")["value"].sum() and compare against your Module 3 totals.
print("\nValue by Client Name")
print(df.groupby('client_name')['value'].sum().head(3))

# 4. df["advisor"].unique() for the distinct advisors.
print("\nAll Advisors")
print(df['advisor'].unique())

# 5. Print a line-count comparison, and comment on what groupby is doing underneath.
print("\nLine Count Comparison")
print("Total No. of Records: ", len(df))
print("SELL-only Trades: ", len(df[df['side'] == 'SELL']))
print("No. of Advisors: ", len(df['advisor'].unique()))