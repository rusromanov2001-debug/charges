import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
DB_PATH = "charges.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS charges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            charge_date TEXT NOT NULL,
            token TEXT,
            number TEXT,
            refunded REAL DEFAULT 0,
            is_returned INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()
    charges = conn.execute("SELECT * FROM charges ORDER BY charge_date DESC, id DESC").fetchall()
    conn.close()
    return render_template("index.html", charges=charges)

@app.route("/add", methods=["POST"])
def add_charge():
    amount = float(request.form.get("amount", 0))
    charge_date = request.form.get("charge_date") or datetime.now().strftime("%Y-%m-%d")
    token = request.form.get("token", "").strip()
    number = request.form.get("number", "").strip()
    refunded = float(request.form.get("refunded", 0) or 0)

    conn = get_db()
    conn.execute(
        "INSERT INTO charges (amount, charge_date, token, number, refunded) VALUES (?, ?, ?, ?, ?)",
        (amount, charge_date, token, number, refunded)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:charge_id>", methods=["POST"])
def toggle_returned(charge_id):
    conn = get_db()
    charge = conn.execute("SELECT is_returned FROM charges WHERE id = ?", (charge_id,)).fetchone()
    if charge:
        new_status = 0 if charge["is_returned"] else 1
        conn.execute("UPDATE charges SET is_returned = ? WHERE id = ?", (new_status, charge_id))
        conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:charge_id>", methods=["POST"])
def delete_charge(charge_id):
    conn = get_db()
    conn.execute("DELETE FROM charges WHERE id = ?", (charge_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/update_refund/<int:charge_id>", methods=["POST"])
def update_refund(charge_id):
    refunded = float(request.form.get("refunded", 0) or 0)
    conn = get_db()
    conn.execute("UPDATE charges SET refunded = ? WHERE id = ?", (refunded, charge_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
