# TODO:
# 1. Define InvalidTradeError(Exception).
# 2. Write trade_value(quantity: float, price: float) -> float, raising InvalidTradeError
#    if quantity or price is not positive.
# 3. Write classify_trade(value: float, threshold: float = 20000) -> str.
# 4. Write safe_trade_value(trade: dict) -> float, which calls trade_value and re-raises
#    InvalidTradeError with the trade_id folded into the message (raise ... from e).
# 5. Add docstrings, and an `if __name__ == "__main__":` block with one example call.

class InvalidTradeError(Exception):
    pass
    
def trade_value(quantity: float, price: float) -> float:
    if quantity <= 0:
        raise InvalidTradeError(f"Quantity must be positive; obtained value: {quantity}")
    if price <= 0:
        raise InvalidTradeError(f"Price must be positive; obtained value: {price}")
    return quantity * price

def classify_trade(value: float, threshold: float = 20000) -> str:
    return 'LARGE TRADE' if value > threshold else 'default'

def safe_trade_value(trade: dict) -> float:
    try:
        return trade_value(trade['quantity'], trade['price'])
    except InvalidTradeError as e:
        raise InvalidTradeError(f"{trade['trade_id']}: {e}") from e
        
if __name__ == '__main__':    
    print(classify_trade(2500))    
    safe_trade_value({'trade_id': 'TB001', 'quantity': -500, 'price': 0})