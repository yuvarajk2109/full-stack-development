from pathlib import Path
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. Calculate skew of quantity and value; comment on what each tells you about shape.
print(f"Skew of Quantity: {df['quantity'].skew():.2f}")
print(f"Skew of Value: {df['value'].skew():.2f}")
print("""
Observation: both Quantity and Value are right skewed. 
Quantity is more right skewed than Value is. 
Right Skewed means that there are probably a few values 
which are much higher than values around the mean, kind of like outliers""")

# 2. Calculate pearsonr(quantity, value); comment on r and p together.
r, p = stats.pearsonr(df['quantity'], df['value'])
print(f"\nQuantity vs Value - Correlation: {r:.2f}")
print(f"Quantity vs Value - p-value (<0.05 means the correlation is significant): {p:.3f}")
print("""
Observation: there is no correlation, as the r-value is close to 0. 
This is also statistically proved via the p-value, which is 0.38 and much, much greater than the expected < 0.05 range.""")

# 3. Discuss and comment: would a strong correlation here prove causation?
"""
Not necessarily, just because 2 variables are strongly correlated doesn't mean one is actually influencing the other.
The two variables could still be independent/not completely dependent on each other.
So NO, strong correlation doesn't necessarily prove causation.  
Eg: Ice cream sales and death by drowning increase in summer, so they are correlated, but one doesn't cause the other.  
"""

# 4. ttest_ind comparing BUY vs SELL value; interpret against 0.05, with a small-sample caveat.
buy_values = df.loc[df['side'] == 'BUY', 'value']
sell_values = df.loc[df['side'] == 'SELL', 'value']

t_stat, p_value = stats.ttest_ind(buy_values, sell_values, equal_var = False)
print(f"\nBUY Mean: {buy_values.mean():.2f}")
print(f"SELL Mean: {sell_values.mean():.2f}")
print(f"t-test Results: t={t_stat:.2f}, p={p_value:.2f}")

if p_value < 0.05:
    print("p < 0.05: The NULL HYPOTHESIS is FALSE")
else:
    print("p >= 0.05: Not ENOUGH evidence against the NULL HYPOTHESIS")