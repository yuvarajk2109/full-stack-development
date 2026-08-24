import argparse
import csv

from starter_02A_math import InvalidTradeError, trade_value

def read_trades(path) -> tuple[list, int]:
    """Read a trades CSV, returning (trades, skipped_count).

    TODO: skip any row where quantity or value can't be converted to a
    number, printing a warning naming the trade_id, and continue with the
    rest of the file rather than crashing.
    """
    
    trades = []
    valid = False
    skipped_count = 0
    counter = 0
    
    with open(path) as f:
        reader = csv.DictReader(f)
        for trade in reader:             
            try:
                value = trade_value(int(trade['quantity']), float(trade['price']))
            except (TypeError, ValueError) as e:
                print(f"Invalid data type for {trade['trade_id']}, {e}")
                valid = False
                continue
            except InvalidTradeError as e:
                print(f"Invalid trade values for {trade['trade_id']}: {e}")
                valid = False
            else:
                trades.append(trade)
                valid = True
                trades[counter]['value'] = value
                counter += 1
            finally:                
                print(f"Processed trade {trade['trade_id']}")
                if not valid:
                    skipped_count += 1
    
    return (trades, skipped_count)

def check_large(trade: float, threshold: float) -> bool:
    """TODO: return True if trade['value'] > threshold."""
    return trade['value'] > threshold


def check_high_volume(trade, threshold):
    """TODO: return True if this is an Equity BUY with quantity > threshold.
    Do not apply this rule to Bond or Crypto trades."""
    return trade['asset_class'] == 'Equity' and trade['side'] == 'BUY' and int(trade['quantity']) > threshold


def count_by_client(trades):
    """TODO: return a dict of client_name -> trade count."""
    clients = dict()
    for trade in trades:
        client_name = trade['client_name']
        clients[client_name] = clients.get(client_name, 0) + 1
    return clients

def build_flags(trades, large_threshold, high_volume_threshold):
    """TODO: return a dict of trade_id -> list of flags (e.g. ["LARGE"])
    for every trade that triggers at least one rule."""
    flagged_trades = dict()
    for trade in trades:
        flagged_trades[trade['trade_id']] = list()
        if check_large(trade, large_threshold):
            flagged_trades[trade['trade_id']].append('LARGE')
        if check_high_volume(trade, high_volume_threshold):
            flagged_trades[trade['trade_id']].append('HIGH_VOLUME')
    return flagged_trades


def find_frequent_clients(trades, frequency_threshold):
    """TODO: return a dict of client_name -> count, for clients whose trade
    count is >= frequency_threshold."""
    clients = dict()
    for trade in trades:
        client_name = trade['client_name']
        clients[client_name] = clients.get(client_name, 0) + 1
    return {
        client_name: count
        for client_name, count in clients.items()
        if count >= frequency_threshold
    }
        
def write_report(path, trades, skipped_count, flags_by_trade, frequent_clients):
    """TODO: write the report described in the lab README to `path`, and
    print the same content to the console."""
    with open(path, "w") as f:
        """
            Displaying trades first, nicely formatted in a table
            The same data is also displayed to the console, 
            so each print/write is captured in a variable and then printed/written
        """
        line = f"{'Trade ID':<12}{'Side':<12}{'Quantity':>8}{'Price':>12}{'Value':>12}{'Flags':>20}"
        print("\n\n" + line)
        f.write(line + "\n")
        """
            Cycling through each trade and displaying the information
        """
        for trade in trades:
            flags = ", ".join(flags_by_trade[trade['trade_id']])
            line = f"{trade['trade_id']:<12}{trade['side']:<12}{trade['quantity']:>8}{float(trade['price']):>12,.2f}{trade['value']:>12,.2f}{flags:>20}"
            print(line)
            f.write(line + "\n")
        f.write("\n")
        print()
        
        """
        Other KPIs -> Skipped Records, Frequent Clients Info
        """
        line = f"No. of Invalid Records Skipped: {skipped_count}"
        print(line)
        f.write(line + "\n")
        freq_clients = ", ".join(frequent_clients.keys())
        line = f"Frequent Clients (with 3 or more trades): {freq_clients}"
        print(line)
        f.write(line + "\n")

def main():
    parser = argparse.ArgumentParser(description="Trade Compliance Checker")
    parser.add_argument("--input", default="../shared/trades.csv")
    parser.add_argument("--report", default="../reports/trade_report.txt")
    parser.add_argument("--large-threshold", type=float, default=20000)
    parser.add_argument("--high-volume-threshold", type=float, default=150)
    parser.add_argument("--frequency-threshold", type=int, default=3)
    args = parser.parse_args()

    trades, skipped_count = read_trades(args.input)
    flags_by_trade = build_flags(trades, args.large_threshold, args.high_volume_threshold)
    frequent_clients = find_frequent_clients(trades, args.frequency_threshold)
    write_report(args.report, trades, skipped_count, flags_by_trade, frequent_clients)


if __name__ == "__main__":
    main()