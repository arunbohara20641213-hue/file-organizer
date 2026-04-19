"""Undo file organization by reversing recent transactions."""

import json
import shutil
from pathlib import Path
from typing import List

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


def reverse_transaction(transaction: dict) -> bool:
    """Reverse a single transaction by moving file back to source."""
    source = Path(transaction.get("source"))
    destination = Path(transaction.get("destination"))

    if not destination.exists():
        print(f"[WARN] Destination file not found: {destination}")
        return False

    try:
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(source))
        print(f"[OK] Reverted: {destination.name} -> {source}")
        return True
    except OSError as exc:
        print(f"[ERROR] Failed to revert {destination.name}: {exc}")
        return False


def undo_last(count: int = 1) -> int:
    """Revert the last N transactions. Return count of successful reversals."""
    transactions = read_transactions()

    if not transactions:
        print("[WARN] No transactions to undo.")
        return 0

    count = min(count, len(transactions))
    reversed_count = 0

    for i in range(count):
        txn = transactions[-(i + 1)]
        if reverse_transaction(txn):
            reversed_count += 1

    print(f"\n[OK] Undo complete: {reversed_count}/{count} transactions reversed.")
    return reversed_count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Undo file organization by reverting recent moves.")
    parser.add_argument("--count", type=int, default=1, help="Number of moves to revert (default: 1)")
    args = parser.parse_args()

    undo_last(args.count)
