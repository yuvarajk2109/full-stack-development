from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. LinearRegression predicting value from quantity and price.
# 2. train_test_split(test_size=0.3, random_state=42).

X = df[['quantity', 'price']]
y = df['value']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)

model = LinearRegression().fit(X_train, y_train)
preds = model.predict(X_test)

# 3. Evaluate with MAE (Mean Absolute Error) and RMSE (Root Mean Squared Error)
#    on the test set.
mae = mean_absolute_error(y_test, preds)
mse = mean_squared_error(y_test, preds) ** 0.5
print(f"Logistic Regression Statistics\nMean Absolute Error: {mae}\nMean Squared Error: {mse}")

# 4. DummyRegressor(strategy="mean") baseline, evaluated the same way, and compared.
baseline = DummyRegressor(strategy='mean').fit(X_train, y_train)
base_preds = baseline.predict(X_test)
base_mae = mean_absolute_error(y_test, preds)
base_mse = mean_squared_error(y_test, preds) ** 0.5
print(f"\nBaseline Statistics\nMean Absolute Error: {base_mae}\nMean Squared Error: {base_mse}")

# 5. Investigate: compute quantity * price per row, compare to actual value, 
# find the asset_class where they disagree.
df['calc_value'] = df['quantity'] * df['price']
df['disagrees'] = (df['calc_value'] - df['value']).abs() > 0.01
print("\nRows where quantity * price != value:")
print(df.loc[df["disagrees"], ["trade_id", "asset_class", "quantity", "price", "value", "calc_value"]])

# 6. Comment: what's actually different about how value is calculated for that class?
"""
The value is computed as (quantity * price) / 100, 
which is different from how is it computed for the rest of the data. 
"""

# 7. Comment: plain-English explanation of the MAE, why the model underperformed, and
#    what feature engineering would fix it.
"""
Mean Absolute Error essentially compares the actual value and the predicted value, 
finding the difference between them. This computation is done for each prediction.
Just computing the difference would mean the error computation 
would have positive and negative values, making the error a useless measure.
When taking the absolute value, we get positive values 
and it gives a good measure of the error.

The models - both the logistic regression and baseline - 
are just poor and basically provide the same error. This is because
the value computation differs for different equity types 
(like bond having a different computation). 

So we need to consider the equity feature/column as well and engineer the
model based on the additional aforemntioned features.
"""