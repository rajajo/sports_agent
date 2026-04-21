import asyncio
import json
import os
import threading
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, jsonify

OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output.json")
EXPENSE_FILE = os.getenv("EXPENSE_FILE", "expenses.json")

app = Flask(__name__)

# Track whether the agent is currently running
_agent_running = False


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def _run_agent_background():
    global _agent_running
    try:
        from daily_assistant import main
        asyncio.run(main())
    except Exception as e:
        print(f"Agent run failed: {e}")
    finally:
        _agent_running = False


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

    summary = output.get("summary", "No data yet. Click 'Run Report' to start.")

    monthly_totals = expenses.get("monthly_totals", {})
    month = expenses.get("month", "")
    all_entries = expenses.get("expenses", [])
    grand_total = round(sum(monthly_totals.values()), 2)

    all_entries = sorted(all_entries, key=lambda e: e.get("date", ""), reverse=True)

    return render_template(
        "index.html",
        generated_at=generated_at,
        summary=summary,
        monthly_totals=monthly_totals,
        month=month,
        all_entries=all_entries,
        grand_total=grand_total,
        agent_running=_agent_running,
    )


@app.route("/run", methods=["POST"])
def run_report():
    global _agent_running
    if not _agent_running:
        _agent_running = True
        thread = threading.Thread(target=_run_agent_background, daemon=True)
        thread.start()
    return redirect(url_for("index"))


@app.route("/status")
def status():
    """Polled by the UI to know when the agent finishes."""
    return jsonify({"running": _agent_running})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
