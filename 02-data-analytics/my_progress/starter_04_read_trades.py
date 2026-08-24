import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "shared" / "trades.csv"

# TODO:
# 1. Read DATA_PATH with csv.DictReader inside a `with` block, collect rows into a list.
# 2. Build a dict keyed by client_name, summing `value` (convert to float) per client.
# 3. Build a set of distinct advisor names.
# 4. Print each client's total, sorted alphabetically by client_name.
# 5. Write the same summary to client_summary.txt (same folder as this script), using `with`.

trades = []

with open(DATA_PATH) as f:
    reader = csv.DictReader(f)
    for row in reader:
        trades.append(row)
        
print(f"No. of Trades: {len(trades)}\n")

clients = dict()
for trade in trades:
    client_name = trade['client_name']
    if client_name in clients:
        clients[client_name] += float(trade['value'])
    else:
        clients[client_name] = float(trade['value'])

advisors = set()
for trade in trades:
    advisors.add(trade['advisor'])

sorted_clients = sorted(clients.items())
    
SUMMARY_PATH = Path(__file__).resolve().parents[1] / "reports" / "client_summary.txt"
with open(SUMMARY_PATH, "w") as f:
    line = f"{'Client Name':<20} {'Value':<20}"
    print(line)
    f.write(line + "\n")
    for client in sorted_clients:
        line = f"{client[0]:<20} {client[1]:<20,.2f}"
        print(line)
        f.write(line + "\n")
        
print(f"\nSummary written to {SUMMARY_PATH.name} under the reports folder")    