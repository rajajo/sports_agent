import json
import os
from datetime import datetime
from flask import Flask, render_template

OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output.json")
EXPENSE_FILE = os.getenv("EXPENSE_FILE", "expenses.json")

app = Flask(__name__)


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


@app.route("/")
def index():
    output = _load_json(OUTPUT_FILE)
    expenses = _load_json(EXPENSE_FILE)

    generated_at = output.get("generated_at", "")
    if generated_at:
        try:
            dt = datetime.fromisoformat(generated_at)
            generated_at = dt.strftime("%d %b %Y, %H:%M UTC")
        except ValueError:
            pass

    summary = output.get("summary", "No data yet. Run daily_assistant.py first.")

    monthly_totals = expenses.get("monthly_totals", {})
    month = expenses.get("month", "")
    all_entries = expenses.get("expenses", [])
    grand_total = round(sum(monthly_totals.values()), 2)

    # Most recent entries first
    all_entries = sorted(all_entries, key=lambda e: e.get("date", ""), reverse=True)

    return render_template(
        "index.html",
        generated_at=generated_at,
        summary=summary,
        monthly_totals=monthly_totals,
        month=month,
        all_entries=all_entries,
        grand_total=grand_total,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
