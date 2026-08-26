"""A small end-to-end dashboard, pulling together every module of Sprint 4:
Module 12's ETL structure, Module 6's cleaning, Module 7/9's analysis patterns,
and Module 10's honest charting principles.

Data-access note for a non-technical stakeholder: this dashboard reads from a local
file (extract()), not a live API. For a book this size (twenty trades, refreshed once
a day), a daily file is simpler and more reliable than querying an API on every run --
an API only earns its complexity when data changes intraday or only a filtered subset
is needed. If the source ever changes to a live feed, only extract() needs to change;
transform(), load(), and everything downstream stay the same.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1] / "shared"
OUT = Path(__file__).resolve().parents[1] / "reports"

ASSET_CLASSES = {
    "equity": "Equity",
    "bond": "Bond",
    "etf": "ETF",
    "crypto": "Crypto"
}

def extract():
    """TODO: read shared/trade.csv and return it unchanged."""
    return pd.read_csv(BASE / 'trades.csv')

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

def compute_insights(df):
    """
    Question 1
    Which asset contributes to most of the trade value?
    """
    asset_share = (df.groupby("asset_class")["value"].sum() / df["value"].sum() * 100).round(1)
    top_asset_class = asset_share.idxmax()

    """
    Question 2:
    Who is the best advisor?
    Who is the worst advisor?
    By how much do they differ? 
    """
    mean_by_advisor = df.groupby("advisor")["value"].mean().round(2)
    top_advisor = mean_by_advisor.idxmax()
    bottom_advisor = mean_by_advisor.idxmin()
    ratio = round(mean_by_advisor[top_advisor] / mean_by_advisor[bottom_advisor], 1)
    
    """
    Question 3
    What is the total weekly value?
    """

    weekly = df.set_index("trade_date")["value"].resample("W").sum()
    
    """
    Question 4
    Which advisor generated the highest total trade value?
    """
    total_by_advisor = df.groupby("advisor")["value"].sum().round(2)
    highest_total_advisor = total_by_advisor.idxmax()

    """
    Question 5
    Which asset class had the highest average trade value per transaction?
    """
    avg_by_asset_class = df.groupby("asset_class")["value"].mean().round(2)
    highest_avg_asset_class = avg_by_asset_class.idxmax()

    return {
        "asset_share": asset_share,
        "top_asset_class": top_asset_class,
        "mean_by_advisor": mean_by_advisor,
        "top_advisor": top_advisor,
        "bottom_advisor": bottom_advisor,
        "advisor_ratio": ratio,
        "weekly": weekly,
        "total_by_advisor": total_by_advisor,
        "highest_total_advisor": highest_total_advisor,
        "avg_by_asset_class": avg_by_asset_class,
        "highest_avg_asset_class": highest_avg_asset_class,
        "equity_trade_percentage": equity_trade_percentage,
    }


def build_charts(df):
    # TODO:
    # 1. Bar chart: total value by asset_class, y-axis starting at 0, specific title,
    #    labelled axes -> chart_asset_class.png
    asset_class_totals = df.groupby('asset_class')['value'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(asset_class_totals.index, asset_class_totals.values, color="#368727")
    ax.set_title('Total Value by Asset Class')
    ax.set_xlabel('Asset Class')
    ax.set_ylabel('Total Trade Value ($)')
    ax.set_ylim(bottom=0)
    fig.savefig(OUT / 'chart_final_01_asset_class.png')
    plt.close(fig)
    print("Chart 1 SUCCESSFULLY saved: Total Value by Asset Class")
    
    equity_trades = df[df['asset_class'] == 'Equity']
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(equity_trades['quantity'], equity_trades['value'], color='#368727', alpha=0.7)
    ax.set_title('Quantity vs Trade Value of Equity Trades')
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Trade Value ($)')
    fig.savefig(OUT / 'chart_final_02_quantity_vs_value.png')
    plt.close(fig)
    print("Chart 2 SUCCESSFULLY saved: Scatter Plot of Quantity vs Value for Equity Trades")
    
    weekly_trends = df.set_index('trade_date').resample('W')['value'].sum()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(weekly_trends.index, weekly_trends.values, marker='o', color="#368727")
    ax.set_title('Total Trade Value by Week')
    ax.set_xlabel('End of Week Date')
    ax.set_ylabel('Total Trade Value ($)')
    ax.set_xticks(weekly_trends.index)
    ax.set_xticklabels([date.strftime('%d-%m-%Y') for date in weekly_trends.index])
    fig.savefig(OUT / 'chart_final_03_weekly_trend.png')
    plt.close(fig)
    print("Chart 3 SUCCESSFULLY saved: Total Value by Week")

def print_dashboard(insights):
    print("\nAnalytics Dashboard\n")

    print(f"1. {insights['top_asset_class']} accounts for "
          f"{insights['asset_share'][insights['top_asset_class']]}% of total trade value.")

    print(f"2. {insights['top_advisor']}'s average trade "
          f"(${insights['mean_by_advisor'][insights['top_advisor']]:,.2f}) is "
          f"{insights['advisor_ratio']}x {insights['bottom_advisor']}'s "
          f"(${insights['mean_by_advisor'][insights['bottom_advisor']]:,.2f}).")

    week1 = insights["weekly"].iloc[0]
    print(f"3. The total trading value of the week was (${week1:,.2f}).")

    print(f"4. {insights['highest_total_advisor']} generated the highest "
          f"total trade value of "
          f"${insights['total_by_advisor'][insights['highest_total_advisor']]:,.2f}.")

    print(f"5. {insights['highest_avg_asset_class']} had the highest "
          f"average trade value per transaction of "
          f"${insights['avg_by_asset_class'][insights['highest_avg_asset_class']]:,.2f}.")

if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean, OUT / "dashboard_data_loaded.csv")
    insights = compute_insights(clean)
    build_charts(clean)
    print_dashboard(insights)