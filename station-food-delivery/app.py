from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3, os, uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "food_delivery.db")
app = Flask(__name__)
app.secret_key = "station-food-delivery-demo-secret"

STATIONS = [
    ("VISAKHAPATNAM", "Visakhapatnam", "AP"), ("VIZIANAGARAM", "Vizianagaram", "AP"),
    ("SRIKAKULAM", "Srikakulam Road", "AP"), ("TUNI", "Tuni", "AP"),
    ("ANAKAPALLE", "Anakapalle", "AP"), ("RAJAHMUNDRY", "Rajahmundry", "AP"),
    ("VIJAYAWADA", "Vijayawada", "AP"), ("GUNTUR", "Guntur", "AP"),
    ("ONGOLE", "Ongole", "AP"), ("NELLORE", "Nellore", "AP")
]
FOODS = [
    ("veg-meals", "Veg Meals", 120), ("biryani", "Chicken Biryani", 180),
    ("idli", "Idli & Vada", 80), ("dosa", "Masala Dosa", 90),
    ("fried-rice", "Veg Fried Rice", 130), ("snacks", "Snacks Combo", 70),
    ("water", "Water Bottle", 20)
]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_code TEXT UNIQUE NOT NULL,
        customer_name TEXT NOT NULL, contact TEXT NOT NULL,
        source_station TEXT NOT NULL, destination_station TEXT NOT NULL,
        coach_seat TEXT NOT NULL, food_name TEXT NOT NULL, quantity INTEGER NOT NULL,
        amount REAL NOT NULL, payment_mode TEXT NOT NULL, status TEXT NOT NULL,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def food_price(food_id):
    return next((price for fid, name, price in FOODS if fid == food_id), 0)

def food_name(food_id):
    return next((name for fid, name, price in FOODS if fid == food_id), food_id)

@app.route("/")
def index():
    return render_template("index.html", stations=STATIONS, foods=FOODS)

@app.post("/order")
def create_order():
    customer_name = request.form.get("customer_name", "").strip()
    contact = request.form.get("contact", "").strip()
    source = request.form.get("source_station", "")
    destination = request.form.get("destination_station", "")
    coach_seat = request.form.get("coach_seat", "").strip()
    food = request.form.get("food", "")
    quantity = int(request.form.get("quantity", 1))

    if not all([customer_name, contact, source, destination, coach_seat, food]):
        flash("Please fill all required fields.", "error")
        return redirect(url_for("index"))
    if source == destination:
        flash("Source and destination stations must be different.", "error")
        return redirect(url_for("index"))
    if quantity < 1 or quantity > 10:
        flash("Quantity must be between 1 and 10.", "error")
        return redirect(url_for("index"))

    amount = food_price(food) * quantity
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = "SFD-" + uuid.uuid4().hex[:8].upper()
    conn = db()
    conn.execute("""INSERT INTO orders
        (order_code, customer_name, contact, source_station, destination_station,
         coach_seat, food_name, quantity, amount, payment_mode, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (code, customer_name, contact, source, destination, coach_seat,
         food_name(food), quantity, amount, request.form.get("payment_mode", "Cash on Delivery"),
         "Order Confirmed", now, now))
    conn.commit()
    conn.close()
    return redirect(url_for("track", order_code=code))

@app.route("/track/<order_code>")
def track(order_code):
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,)).fetchone()
    conn.close()
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("index"))
    return render_template("track.html", order=order)

@app.route("/admin")
def admin():
    conn = db()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", orders=orders)

@app.post("/admin/update/<int:order_id>")
def update_order(order_id):
    status = request.form.get("status", "Order Confirmed")
    allowed = ["Order Confirmed", "Preparing Food", "At Source Station",
               "In Transit", "Reached Destination Station", "Delivered"]
    if status not in allowed:
        flash("Invalid status.", "error")
        return redirect(url_for("admin"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = db()
    conn.execute("UPDATE orders SET status=?, updated_at=? WHERE id=?", (status, now, order_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

@app.get("/api/stations")
def api_stations():
    return jsonify([{"code": c, "name": n, "state": s} for c, n, s in STATIONS])

@app.get("/api/orders/<order_code>")
def api_order(order_code):
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE order_code=?", (order_code,)).fetchone()
    conn.close()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(dict(order))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
