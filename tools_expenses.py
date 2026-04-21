import json
import os
import shutil
from datetime import datetime

EXPENSE_FILE = os.getenv("EXPENSE_FILE", "expenses.json")

CATEGORIES = ["Food", "Transport", "Software", "Shopping", "Entertainment", "Other"]


def _current_month() -> str:
    return datetime.utcnow().strftime("%Y-%m")


def _empty_store() -> dict:
    return {
        "month": _current_month(),
        "expenses": [],
        "monthly_totals": {c: 0.0 for c in CATEGORIES},
    }


def _recompute_totals(store: dict) -> dict:
    totals = {c: 0.0 for c in CATEGORIES}
    for entry in store["expenses"]:
        cat = entry.get("category", "Other")
        if cat not in totals:
            cat = "Other"
        totals[cat] = round(totals[cat] + entry.get("amount", 0.0), 2)
    store["monthly_totals"] = totals
    return store


def _rollover_if_needed(store: dict) -> dict:
    current = _current_month()
    if store.get("month") == current:
        return store
    old_month = store.get("month", "unknown")
    archive_path = EXPENSE_FILE.replace(".json", f"_{old_month}.json")
    with open(archive_path, "w") as f:
        json.dump(store, f, indent=2)
    print(f"Archived {old_month} expenses to {archive_path}")
    return _empty_store()


def _load() -> dict:
    if not os.path.exists(EXPENSE_FILE):
        return _empty_store()
    with open(EXPENSE_FILE) as f:
        store = json.load(f)
    return _rollover_if_needed(store)


def _save(store: dict) -> None:
    store = _recompute_totals(store)
    with open(EXPENSE_FILE, "w") as f:
        json.dump(store, f, indent=2)


def get_expense_categories() -> list:
    """Return the list of valid expense categories to use when classifying expenses."""
    return CATEGORIES


def add_expense(
    msg_id: str,
    date: str,
    amount: float,
    currency: str,
    vendor: str,
    category: str,
    description: str,
    email_subject: str,
) -> str:
    """
    Save a single expense entry identified from an email.
    Skips duplicates (same msg_id). Returns a confirmation string.
    """
    store = _load()
    existing_ids = {e["id"] for e in store["expenses"]}
    if msg_id in existing_ids:
        return f"Skipped (already recorded): {vendor} {currency}{amount}"

    if category not in CATEGORIES:
        category = "Other"

    store["expenses"].append(
        {
            "id": msg_id,
            "date": date,
            "amount": amount,
            "currency": currency,
            "vendor": vendor,
            "category": category,
            "description": description,
            "email_subject": email_subject,
        }
    )
    _save(store)
    return f"Saved: {vendor} {currency}{amount} → {category}"


def get_monthly_summary() -> str:
    """Return a human-readable summary of this month's expense totals."""
    store = _load()
    month = store.get("month", _current_month())
    totals = store.get("monthly_totals", {})
    grand_total = round(sum(totals.values()), 2)
    lines = [f"Expense Summary — {month}"]
    for cat, amt in totals.items():
        if amt > 0:
            lines.append(f"  {cat}: ${amt:.2f}")
    lines.append(f"  TOTAL: ${grand_total:.2f}")
    lines.append(f"  Entries: {len(store['expenses'])}")
    return "\n".join(lines)
