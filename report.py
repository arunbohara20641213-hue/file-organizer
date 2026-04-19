"""Generate summary reports of file organization activities."""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

from config import TRANSACTION_LOG


def read_transactions() -> List[dict]:
    """Read all transaction records from the log."""
    transactions = []
    if not TRANSACTION_LOG.exists():
        return transactions

    try:
        with open(TRANSACTION_LOG, "r") as f:
            for line in f:
                if line.strip():
                    transactions.append(json.loads(line))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Failed to read transaction log: {exc}")

    return transactions


def get_summary_stats(transactions: List[dict]) -> Dict[str, int]:
    """Calculate summary statistics from transactions."""
    stats = defaultdict(int)
    stats["total_transactions"] = len(transactions)

    for txn in transactions:
        folder = txn.get("folder", "Unknown")
        stats[f"folder_{folder}"] += 1
        stats[f"status_{txn.get('status', 'unknown')}"] += 1

    return dict(stats)


def filter_transactions_by_date(transactions: List[dict], date_str: str) -> List[dict]:
    """Filter transactions by date. Format: YYYY-MM-DD, 'today', 'yesterday', or 'week'."""
    if not transactions:
        return []

    now = datetime.now()

    if date_str.lower() == "today":
        target_date = now.date()
    elif date_str.lower() == "yesterday":
        target_date = (now - timedelta(days=1)).date()
    elif date_str.lower() == "week":
        target_date = (now - timedelta(days=7)).date()
    else:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"[ERROR] Invalid date format: {date_str}. Use YYYY-MM-DD or 'today'/'yesterday'/'week'.")
            return []

    filtered = []
    for txn in transactions:
        txn_date = datetime.fromisoformat(txn.get("timestamp", "")).date()
        if date_str.lower() in ("week",) and txn_date >= target_date:
            filtered.append(txn)
        elif date_str.lower() not in ("week",) and txn_date == target_date:
            filtered.append(txn)

    return filtered


def print_report(transactions: List[dict], date_str: str = None) -> None:
    """Print a formatted summary report."""
    if date_str:
        transactions = filter_transactions_by_date(transactions, date_str)

    stats = get_summary_stats(transactions)

    print("\n" + "=" * 60)
    print("FILE ORGANIZER SUMMARY REPORT")
    print("=" * 60)

    print(f"\nTotal Transactions: {stats.get('total_transactions', 0)}")

    print("\nBy Folder:")
    for key, count in sorted(stats.items()):
        if key.startswith("folder_"):
            folder_name = key.replace("folder_", "")
            print(f"  {folder_name}: {count}")

    print("\nBy Status:")
    for key, count in sorted(stats.items()):
        if key.startswith("status_"):
            status = key.replace("status_", "")
            print(f"  {status}: {count}")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a summary report of file organization.")
    parser.add_argument("--date", type=str, default=None, help="Filter by date (YYYY-MM-DD, 'today', 'yesterday', 'week')")
    args = parser.parse_args()

    transactions = read_transactions()
    print_report(transactions, args.date)
