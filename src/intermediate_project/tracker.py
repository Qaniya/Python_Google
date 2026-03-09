from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import json
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class Expense:
    """A single expense entry."""

    amount: float
    category: str
    note: str
    spent_on: date

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be greater than zero")
        self.category = self.category.strip().lower()
        if not self.category:
            raise ValueError("category cannot be empty")
        self.note = self.note.strip()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["spent_on"] = self.spent_on.isoformat()
        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> "Expense":
        return cls(
            amount=float(payload["amount"]),
            category=str(payload["category"]),
            note=str(payload.get("note", "")),
            spent_on=date.fromisoformat(payload["spent_on"]),
        )


class ExpenseTracker:
    """Tracks expenses and supports persistence and reporting."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._expenses: list[Expense] = []

    @property
    def expenses(self) -> tuple[Expense, ...]:
        return tuple(self._expenses)

    def add(self, expense: Expense) -> None:
        self._expenses.append(expense)

    def add_many(self, expenses: Iterable[Expense]) -> None:
        self._expenses.extend(expenses)

    def total(self) -> float:
        return round(sum(exp.amount for exp in self._expenses), 2)

    def by_category(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for exp in self._expenses:
            totals[exp.category] = round(totals.get(exp.category, 0.0) + exp.amount, 2)
        return totals

    def for_month(self, year: int, month: int) -> list[Expense]:
        return [e for e in self._expenses if e.spent_on.year == year and e.spent_on.month == month]

    def save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [exp.to_dict() for exp in self._expenses]
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.storage_path.exists():
            self._expenses = []
            return
        payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self._expenses = [Expense.from_dict(item) for item in payload]
