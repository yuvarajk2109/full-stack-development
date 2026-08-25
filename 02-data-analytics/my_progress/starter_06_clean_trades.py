from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "messy-trades-raw.csv"

df = pd.read_csv(DATA_PATH)

# TODO, each with a one-line comment explaining your reasoning:
# 1. Drop the row with missing quantity (can't be safely reconstructed).
current_length = len(df)
df.dropna(inplace=True, subset=['quantity'])
after_removed = len(df)
print(f"a. {current_length - after_removed} row(s) dropped.")

# 2. Recompute the missing value as quantity * price.
df['quantity'] = df['quantity'].astype(float)
missing_value = df['value'].isna()
df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]
print(f"b. Recomputed missing value as quantity * price for a total of {missing_value.sum()} record(s).")

# 3. Backfill the missing client_name from another row with the same client_id.
missing_name = df['client_name'].isna().sum()
df['client_name'] = df.groupby('client_id')['client_name'].transform('first')
print(f"c. {missing_name} client(s)' names have been backfilled from another row with the same client ID")

# 4. Parse trade_date correctly, resolving the ambiguous DD/MM/YYYY row using the
#    surrounding trade_id sequence, not an assumption.
df['trade_date'] = pd.to_datetime(df['trade_date'], format='mixed', dayfirst=True)
print(f"d. Format of Trade Date after parsing:", df['trade_date'].dtype)

# 5. Normalise asset_class casing without turning "ETF" into "Etf" (use a canonical mapping).
ASSET_CLASSES = {
    "equity": "Equity",
    "bond": "Bond",
    "etf": "ETF",
    "crypto": "Crypto"
}
df['asset_class'] = df['asset_class'].str.lower().map(ASSET_CLASSES)
print(f"e. Distinct Classes after normalisation:",", ".join(list(df['asset_class'].unique())))

# 6. Drop the exact duplicate row.
current_length = len(df)
df.drop_duplicates(inplace=True)
after_removed = len(df)
print(f"f. Removed {current_length - after_removed} duplicate row(s)")

# 7. Flag (don't drop) the quantity outlier, with a one-sentence investigation note.
equity_quantities = df.loc[df['asset_class'] == 'Equity', "quantity"]
threshold = equity_quantities.quantile(0.75)
outliers = df[(df['asset_class'] == 'Equity') & (df['quantity'] > threshold * 5)]
print(f"g. Flagged (NOT DROPPED) {len(outliers)} quantities.")
print(outliers[['trade_id', 'instrument', 'quantity']])

print(f"\nFinal row count: {len(df)}")