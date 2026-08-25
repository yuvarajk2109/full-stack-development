from pathlib import Path
import pandas as pd
import numpy as np

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

pd.set_option('display.precision', 2)

# TODO:
# 1. Print df.shape and describe() on the numeric columns.
print("Shape of Dataframe:", df.shape)
num_cols = df.select_dtypes(include = np.number)
print("Numerical Columns:", ', '.join(list(num_cols.columns)))
print("Description of Numerical Columns\n", num_cols.describe())

# 2. Segment by currency: count and mean value per currency. Note the mixing anomaly.
print("\nValue by Currency - COUNT and MEAN")
print(df.groupby('currency')['value'].agg(['count', 'mean']))

# 3. Segment by client_name: highest total value, and highest trade count (may differ).
print("\nTrade Value by Client")
print(df.groupby('client_name')['value'].sum().sort_values(ascending=False))
print("\nTrade Count by Client")
print(df.groupby('client_name')['value'].count().sort_values(ascending=False))

# 4. Segment by instrument, within asset_class == "Equity" only: highest total value.
print("\nValue by Equity Instruments")
print(df[df['asset_class'] == 'Equity'].groupby('instrument')['value'].sum().sort_values(ascending=False))

# 5. Write one pattern, one anomaly, and one specific, checkable hypothesis as comments.
"""
Pattern: More trades have been made in USD
Anomaly: Not necessarily an anomaly, but despite more trades being made in USD, the trade value is greater in GBP
"""
print("\nValue by Advisor")
print(df.groupby('advisor')['value'].sum().sort_values(ascending=False))
"""
Checkable Hypothesis: Advisor J. Okafor seems to be generating the most value for their clients.
"""