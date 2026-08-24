# TODO: import from starter_math, then refactor the loop below to:
# - catch (TypeError, ValueError) together for a wrong-type quantity/price
# - catch InvalidTradeError separately for a business-rule failure
# - use else to accumulate the running total only on success
# - use finally to print a "processed <trade_id>" line unconditionally

from starter_02A_math import InvalidTradeError, trade_value, classify_trade, safe_trade_value

trades = [
    {"trade_id": "T0001", "quantity": 120, "price": 185.32},
    {"trade_id": "T0002", "quantity": "N/A", "price": 402.11},  # wrong type
    {"trade_id": "T0003", "quantity": -5, "price": 98.75},       # fails validation
    {"trade_id": "T0004", "quantity": 300, "price": 84.22},
    {"trade_id": "T0005", "quantity": 8, "price": 241.20},
]

total_value = 0.0

for trade in trades:
    try:
        value = trade_value(trade['quantity'], trade['price'])
    except (TypeError, ValueError) as e:
        print(f"Invalid data type for {trade['trade_id']}, {e}")
        continue
    except InvalidTradeError as e:
        print(f"Invalid trade values for {trade['trade_id']}: {e}")
    else:
        total_value += value
    finally:
        print(f"Processed trade {trade['trade_id']}; total trade value: {total_value:,.2f}")

print(f"\nTotal value processed: {total_value:,.2f}")