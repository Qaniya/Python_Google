from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .tracker import Expense, ExpenseTracker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Expense tracker CLI")
    parser.add_argument("--data-file", default="data/expenses.json", help="JSON data file")

    sub = parser.add_subparsers(dest="command", required=True)

    add_cmd = sub.add_parser("add", help="Add an expense")
    add_cmd.add_argument("amount", type=float)
    add_cmd.add_argument("category")
    add_cmd.add_argument("note")
    add_cmd.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")

    sub.add_parser("summary", help="Show totals and category breakdown")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    tracker = ExpenseTracker(Path(args.data_file))
    tracker.load()

    if args.command == "add":
        tracker.add(
            Expense(
                amount=args.amount,
                category=args.category,
                note=args.note,
                spent_on=date.fromisoformat(args.date),
            )
        )
        tracker.save()
        print("Expense added")
        return

    print(f"Total: ${tracker.total():.2f}")
    breakdown = tracker.by_category()
    if not breakdown:
        print("No expenses yet")
        return
    for category, total in sorted(breakdown.items()):
        print(f"- {category}: ${total:.2f}")


if __name__ == "__main__":
    main()
