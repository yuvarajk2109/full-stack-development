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
PAGE_SIZE = 5

def fetch_all_trades(page_size = PAGE_SIZE):
    records = []
    page = 1
    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params = {"page": page, "page_size": PAGE_SIZE})
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry After', 1))
            print(f"\tRate limit reached, please wait {retry_after}s before retrying page {page}")
            time.sleep(retry_after)
            continue
        body = response.json()
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
print("\nShape of Dataset: ", df.shape)
print("\nFirst 5 Rows")
print(df.head())

# 4. In fetch_all_trades, on a 429: read Retry-After, time.sleep(), retry the SAME page.
print("\nManually hitting the rate limit by calling the API multiple times")
for i in range(11):
    response = requests.get(BASE_URL, headers=HEADERS, params = {"page": 1, "page_size": 1})
    print(f"\trequest {i+1}:\t HTTP {response.status_code}")
    if response.status_code == 429:
        print(f"\tRate limit reached, please wait {int(response.headers.get('Retry After', 1))}s before retrying page 1")
        break

# 5. Comment: would you recommend an API over a nightly batch extract for this dataset? Why?
"""
It depends on when and where the data is used. If the data is used on an application 
and we need to fetch it for multiple users concurrently, rate limiting the API is a necessity.
However, if large amounts of trade data is sent over to a data analytics warehouse for later processing,
concurrency isn't a priority and the nightly batch extract would work.
So it depends not just on the dataset but also on the situation.
"""