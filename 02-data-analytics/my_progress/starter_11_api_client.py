import time
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5050/trades"
API_KEY = "leap-sprint4-key"
HEADERS = {"X-API-Key": API_KEY}

# TODO:
# 1. fetch_page(page, page_size): one authenticated GET request, return parsed JSON.
response_without_api_key = requests.get(BASE_URL)
print(f"Without API Key:\tHTTP {response_without_api_key.status_code}\t|\t{response_without_api_key.json()}")
response_with_api_key = requests.get(BASE_URL, headers=HEADERS)
print(f"With API Key:\t\tHTTP {response_with_api_key.status_code}\t|\t{response_with_api_key.json()}")

# 2. fetch_all_trades(page_size): loop fetch_page from page 1, accumulate data,
#    stop once page >= total_pages.
PAGE_SIZE = 3

def fetch_all_trades(page_size = PAGE_SIZE):
    records = []
    page = 1
    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params = {"page": page, "page_size": PAGE_SIZE})
        if response.status_code == 429:
            pass
        body = response.json()
        print(body)
        records.extend(body['data'])
        print(f"Page {page} successfully fetched")
        if page >= body['total_pages']:
            break
        page += 1
    return records

# 3. Load accumulated rows into a DataFrame; print shape and df.head().
print("\nFetching All Trades, Page by Page...")
records = fetch_all_trades()
df = pd.DataFrame(records)
print(f"\nSuccessfully loaded {len(df)} records into a dataframe")
print("Shape of Dataset: ", df.shape)
print("First 5 Rows")
print(df.head())

# 4. In fetch_all_trades, on a 429: read Retry-After, time.sleep(), retry the SAME page.
   

# 5. Comment: would you recommend an API over a nightly batch extract for this dataset? Why?