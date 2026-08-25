from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1] / "shared"
OUT = Path(__file__).resolve().parents[1] / "reports"

ASSET_CLASSES = {
    "equity": "Equity",
    "bond": "Bond",
    "etf": "ETF",
    "crypto": "Crypto"
}

def extract():
    """TODO: read shared/messy-trades-raw.csv and return it unchanged."""
    return pd.read_csv(BASE / 'messy-trades-raw.csv')

def transform(df):
    """TODO: apply Module 6's cleaning steps: drop the row with missing quantity,
    recompute the missing value, backfill the missing client_name, parse the
    ambiguous date, normalise asset_class casing (without breaking ETF), and drop
    the exact duplicate row."""
    
    # Dropping the row with missing quantity
    df.dropna(inplace=True, subset=['quantity'])
    
    # Recomputing missing 'values'
    df['quantity'] = df['quantity'].astype(float)
    missing_value = df['value'].isna()
    df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]
    
    # Backfilling missing client names
    df['client_name'] = df.groupby('client_id')['client_name'].transform('first')
    
    # Parsing ambiguous dates
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='mixed', dayfirst=True)
    
    # Normalising ASSET_CLASSES
    df['asset_class'] = df['asset_class'].str.lower().map(ASSET_CLASSES)
    
    # Dropping exact duplicates
    df.drop_duplicates(inplace=True)
    
    return df

def load(df, out_path = OUT / 'clean_trades_loaded.csv'):
    """TODO: write df to out_path as a CSV, and return out_path."""
    df.to_csv(out_path, index=False)
    return out_path

if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean)
    print(f"Extracted {len(raw)} raw rows, transformed to {len(clean)} clean rows")