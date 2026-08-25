import pytest
from starter_12A_etl_pipeline import extract, transform

"""
To run this file:
python -m pytest starter_12B_test_trades.py    
"""

VALID_ASSET_CLASSES = {"Equity", "Bond", "ETF", "Crypto"}

@pytest.fixture
def clean_trades():
    return transform(extract())

# TODO: write tests for
# 1. no missing trade_id values
def test_no_missing_trade_ids(clean_trades):
    assert clean_trades['trade_id'].notna().all()

# 2. quantity is always positive
def test_quantity_is_positive(clean_trades):
    assert (clean_trades['quantity'] > 0).all()

# 3. value is never negative
def test_value_is_non_negative(clean_trades):
    assert (clean_trades['value'] >= 0).all()

# 4. asset_class only contains VALID_ASSET_CLASSES
def test_asset_class_is_valid(clean_trades):
    assert clean_trades['asset_class'].isin(VALID_ASSET_CLASSES).all()

# 5. no duplicate trade_id values
def test_no_duplicate_trade_ids(clean_trades):
    assert clean_trades['trade_id'].is_unique

# TODO: add test_asset_class_valid_no_all
# Deliberately broken: missing .all() on a boolean Series
# Running this gives a "truth value of a Series is ambiguous" error
def test_asset_class_is_valid_no_all(clean_trades):
    assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES)
    # CORRECTED
    # assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES).all()