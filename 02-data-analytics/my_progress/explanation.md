# Stakeholder Explanation

## Why We Read the Data This Way

- The dashboard reads the trade data from a local CSV file using the `extract()` function.
- The dataset is small, containing only around twenty trades.
- The data is expected to be refreshed once per day rather than changing continuously throughout the day.
- For this use case, reading one local file is simpler and more reliable than making an API request every time the dashboard runs.
- A local file also avoids unnecessary network dependency, API authentication, rate limits, and connection failures.
- The ETL structure keeps the data-access step separate from the rest of the dashboard.
- If the business later moves to a live API or another data source, only the `extract()` function needs to change.
- The `transform()`, `load()`, analysis, and charting logic can continue to work with the same cleaned dataset.

## Why We Are Confident the Data Is Trustworthy

- The original data is not assumed to be perfect simply because it came from the source file.
- The `transform()` step acts as a data-quality checkpoint before analysis.
- Missing and inconsistent values are identified and handled before calculations are performed.
- A trade with no quantity is removed because its trade value cannot be reliably calculated.
- Missing trade values are recalculated using the available quantity and price.
- Missing client names are recovered using the client's other records where possible.
- Dates are explicitly parsed so that ambiguous date formats do not produce incorrect time-based analysis.
- Asset-class labels are standardised so that values such as `equity`, `Equity`, and `EQUITY` are treated consistently.
- `ETF` is handled explicitly so that its abbreviation is not incorrectly transformed into another label.
- Exact duplicate records are removed to prevent the same trade from being counted twice.
- The cleaned dataset is saved separately, providing a reproducible output that can be inspected independently of the dashboard.
- Analysis is performed on the cleaned dataset rather than directly on the raw input.
- This means the reported insights are based on a controlled and documented transformation process.

## Transformations We Performed

- Removed records with missing quantity

  - Trades without a quantity cannot provide a reliable trade value.
  - These records are removed before analysis.

- Converted quantity to numeric format

  - Quantity values are converted to floating-point numbers.
  - This ensures mathematical calculations work consistently.

- Recalculated missing trade values

  - Where `value` is missing, it is calculated as:
  - `quantity × price`

- Backfilled missing client names

  - Records are grouped by `client_id`.
  - When another record for the same client contains a name, that name is used to fill the missing value.

- Parsed trade dates

  - Trade dates are converted into a proper datetime format.
  - Ambiguous dates are interpreted using the expected day-first format.
  - This allows reliable weekly analysis and time-series charting.

- Standardised asset-class names

  - Asset-class values are converted to lowercase before mapping.
  - Standard labels are then applied:
  - `equity → Equity`
  - `bond → Bond`
  - `etf → ETF`
  - `crypto → Crypto`

- Removed exact duplicate records

  - Completely identical rows are removed.
  - This prevents duplicate trades from artificially increasing totals.

- Saved the cleaned dataset

  - The transformed data is written to a separate CSV file.
  - This provides a persistent version of the dataset used by the dashboard.

- Performed analysis after cleaning

  - Asset-class trade shares are calculated from the cleaned data.
  - Advisor performance is calculated from the cleaned data.
  - Weekly trade values are calculated from the cleaned dates and values.

- Generated charts from cleaned data

  - Asset-class totals use cleaned trade values.
  - Equity quantity-versus-value analysis uses cleaned Equity trades.
  - Weekly trends use the cleaned trade dates and values.