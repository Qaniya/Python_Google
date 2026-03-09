from datetime import date

from intermediate_project.tracker import Expense, ExpenseTracker


def test_tracker_totals_and_categories(tmp_path):
    tracker = ExpenseTracker(tmp_path / "expenses.json")
    tracker.add_many(
        [
            Expense(amount=10.5, category="Food", note="Lunch", spent_on=date(2026, 1, 3)),
            Expense(amount=25.0, category="Transport", note="Taxi", spent_on=date(2026, 1, 4)),
            Expense(amount=9.5, category="food", note="Coffee", spent_on=date(2026, 1, 4)),
        ]
    )

    assert tracker.total() == 45.0
    assert tracker.by_category() == {"food": 20.0, "transport": 25.0}


def test_persistence_round_trip(tmp_path):
    path = tmp_path / "expenses.json"
    tracker = ExpenseTracker(path)
    tracker.add(Expense(amount=12.0, category="Books", note="Python", spent_on=date(2026, 2, 1)))
    tracker.save()

    reloaded = ExpenseTracker(path)
    reloaded.load()

    assert len(reloaded.expenses) == 1
    expense = reloaded.expenses[0]
    assert expense.amount == 12.0
    assert expense.category == "books"
    assert expense.note == "Python"
