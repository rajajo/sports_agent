"""Run this once to populate expenses.json and output.json with sample data."""
import json
from datetime import datetime, timezone

EXPENSE_FILE = "expenses.json"
OUTPUT_FILE = "output.json"

expenses = [
    {
        "id": "mock_001",
        "date": "2026-04-18",
        "amount": 24.50,
        "currency": "USD",
        "vendor": "Uber",
        "category": "Transport",
        "description": "Ride to downtown office",
        "email_subject": "Your Tuesday trip with Uber",
    },
    {
        "id": "mock_002",
        "date": "2026-04-18",
        "amount": 14.99,
        "currency": "USD",
        "vendor": "Spotify",
        "category": "Software",
        "description": "Monthly premium subscription",
        "email_subject": "Your Spotify receipt",
    },
    {
        "id": "mock_003",
        "date": "2026-04-19",
        "amount": 38.75,
        "currency": "USD",
        "vendor": "Deliveroo",
        "category": "Food",
        "description": "Lunch order from Wagamama",
        "email_subject": "Your Deliveroo order is confirmed",
    },
    {
        "id": "mock_004",
        "date": "2026-04-19",
        "amount": 9.99,
        "currency": "USD",
        "vendor": "AWS",
        "category": "Software",
        "description": "EC2 usage — April billing",
        "email_subject": "AWS Invoice for April 2026",
    },
    {
        "id": "mock_005",
        "date": "2026-04-20",
        "amount": 55.00,
        "currency": "USD",
        "vendor": "Marriott",
        "category": "Entertainment",
        "description": "Hotel bar tab — team dinner",
        "email_subject": "Marriott receipt — folio #8821",
    },
    {
        "id": "mock_006",
        "date": "2026-04-20",
        "amount": 12.30,
        "currency": "USD",
        "vendor": "Pret A Manger",
        "category": "Food",
        "description": "Coffee and sandwich",
        "email_subject": "Your Pret order receipt",
    },
    {
        "id": "mock_007",
        "date": "2026-04-21",
        "amount": 199.00,
        "currency": "USD",
        "vendor": "JetBlue",
        "category": "Transport",
        "description": "Flight BOS→NYC — work trip",
        "email_subject": "Your JetBlue itinerary",
    },
    {
        "id": "mock_008",
        "date": "2026-04-21",
        "amount": 29.99,
        "currency": "USD",
        "vendor": "GitHub",
        "category": "Software",
        "description": "Copilot monthly subscription",
        "email_subject": "GitHub receipt — April 2026",
    },
]

# Compute monthly totals
totals = {"Food": 0.0, "Transport": 0.0, "Software": 0.0, "Shopping": 0.0, "Entertainment": 0.0, "Other": 0.0}
for e in expenses:
    totals[e["category"]] = round(totals[e["category"]] + e["amount"], 2)

store = {
    "month": "2026-04",
    "expenses": expenses,
    "monthly_totals": totals,
}

grand_total = round(sum(totals.values()), 2)

summary = f"""Processed 8 expense emails today. Here's what was added:

New today (Apr 21):
  • JetBlue — $199.00 (Transport) — Flight BOS→NYC
  • GitHub — $29.99 (Software) — Copilot subscription

Monthly snapshot — April 2026:
  Transport is your biggest spend at ${totals['Transport']:.2f} — mainly the JetBlue flight.
  Software subscriptions are stacking up: Spotify, AWS, and GitHub total ${totals['Software']:.2f}.
  Food spend looks normal at ${totals['Food']:.2f}.

Overall total: ${grand_total:.2f} for the month so far."""

output = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "summary": summary,
    "expenses": {
        "new_today": [e for e in expenses if e["date"] == "2026-04-21"],
        "monthly_totals": totals,
        "month_total": grand_total,
        "all_entries": expenses,
    },
}

with open(EXPENSE_FILE, "w") as f:
    json.dump(store, f, indent=2)

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Mock data written to {EXPENSE_FILE} and {OUTPUT_FILE}")
print(f"   {len(expenses)} expenses — total ${grand_total}")
print("   Run: python3 ui.py  →  http://localhost:5000")
