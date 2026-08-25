import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / 'data.csv'

df = pd.read_csv(DATA_PATH, usecols=['sot'])['sot']
print("Before Sampling\n")
print(df.describe())
df = df.sample(n=100000, replace=True, random_state=42, ignore_index=True)

print("Shape of Data", df.shape)

print("First 10 Rows\n")
print(df.head(10))

print("\nDescription\n", df.describe())