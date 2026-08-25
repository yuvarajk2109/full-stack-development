from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1] / "shared"
OUT = Path(__file__).resolve().parents[1] / "reports"
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])

# TODO:
# 1. Bar chart: total value by asset_class, y-axis starting at 0, specific title,
#    labelled axes -> chart_asset_class.png
asset_class_totals = trades.groupby('asset_class')['value'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(asset_class_totals.index, asset_class_totals.values, color="#368727")
ax.set_title('Total Value by Asset Class')
ax.set_xlabel('Asset Class')
ax.set_ylabel('Total Trade Value ($)')
ax.set_ylim(bottom=0)
fig.savefig(OUT / 'chart_01_asset_class.png')
plt.close(fig)
print("Chart 1 SUCCESSFULLY saved: Total Value by Asset Class")

# 2. Line chart: total value by week (reuse Module 9's resample("W") pattern),
#    specific title, labelled axes -> chart_weekly_trend.png
weekly_trends = trades.set_index('trade_date').resample('W')['value'].sum()
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(weekly_trends.index, weekly_trends.values, marker='o', color="#368727")
ax.set_title('Total Trade Value by Week')
ax.set_xlabel('End of Week Date')
ax.set_ylabel('Total Trade Value ($)')
ax.set_xticks(weekly_trends.index)
ax.set_xticklabels([date.strftime('%d-%m-%Y') for date in weekly_trends.index])
fig.savefig(OUT / 'chart_02_weekly_trend.png')
plt.close(fig)
print("Chart 2 SUCCESSFULLY saved: Total Value by Week")

# 3. Scatter plot: quantity vs value, Equity trades only, labelled axes
#    -> chart_quantity_vs_value.png
equity_trades = trades[trades['asset_class'] == 'Equity']
fix, ax = plt.subplots(figsize=(10, 10))
ax.scatter(equity_trades['quantity'], equity_trades['value'], color='#368727', alpha=0.7)
ax.set_title('Quantity vs Trade Value of Equity Trades')
ax.set_xlabel('Quantity')
ax.set_ylabel('Trade Value ($)')
fig.savefig(OUT / 'chart_03_quantity_vs_value.png')
print("Chart 3 SUCCESSFULLY saved: Scatter Plot of Quantity vs Value for Equity Trades")

# 4. One deliberately misleading chart, with a comment explaining the specific flaw
#    -> chart_misleading.png
asset_class_totals = trades.groupby('asset_class')['value'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(asset_class_totals.index, asset_class_totals.values, color="#368727")
ax.set_title('MISLEADING Total Value by Asset Class')
ax.set_xlabel('Asset Class')
ax.set_ylabel('Total Trade Value ($)')
ax.set_ylim(bottom=35000)
fig.savefig(OUT / 'chart_04_misleading.png')
plt.close(fig)
print("Chart 4 SUCCESSFULLY saved: MISLEADING Total Value by Asset Class")