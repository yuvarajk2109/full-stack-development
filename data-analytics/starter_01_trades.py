# Starter: plain Python trade records. No libraries.
# TODO: iterate over `trades`, flag large trades (value > 20000), and print a summary.

trades = [
    {"trade_id": "T0001", "side": "BUY", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "side": "BUY", "quantity": 60, "price": 402.11},
    {"trade_id": "T0003", "side": "SELL", "quantity": 5000, "price": 98.75},
    {"trade_id": "T0004", "side": "SELL", "quantity": 40, "price": 186.10},
    {"trade_id": "T0005", "side": "BUY", "quantity": 25, "price": 141.87},
    {"trade_id": "T0006", "side": "BUY", "quantity": 300, "price": 84.22},
    {"trade_id": "T0007", "side": "SELL", "quantity": 20, "price": 404.55},
    {"trade_id": "T0008", "side": "BUY", "quantity": 0.5, "price": 42000.00},
]

# Your code here

no_of_trades = 0
total_value = 0
no_of_buy = 0
no_of_sell = 0

print("-"*80)
print(f"{'Trade ID':<12}{'Side':<12}{'Quantity':>8}{'Price':>12}{'Value':>12}{'Type':>20}")
print("-"*80)
for trade in trades:
    value = trade['quantity'] * trade['price']
    large = "LARGE TRADE" if value > 20000 else "default"
    print(f"{trade['trade_id']:<12}{trade['side']:<12}{trade['quantity']:>8}{trade['price']:>12,.2f}{value:>12,.2f}{large:>20}")
    
    no_of_trades += 1
    total_value += value
    if trade['side'] == 'BUY':
        no_of_buy += 1
    elif trade['side'] == 'SELL':
        no_of_sell += 1
print("-"*80)
print()
    
print("Total Number of Trades:", no_of_trades)
print("Total Value:", total_value)
print("Count of BUY Trades:", no_of_buy)
print("Count of SELL Trades:", no_of_sell)