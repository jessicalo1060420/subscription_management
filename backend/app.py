from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app,origins=["http://localhost:5174", "http://127.0.0.1:5174"])

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Subscription backend is running"

# 查詢所有訂閱
@app.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            s.subscription_id,
            s.service_name,
            s.plan_name,
            s.status,
            s.start_date,
            c.category_name,
            p.price,
            p.billing_cycle,
            p.payment_day
        FROM subscriptions s
        LEFT JOIN categories c ON s.category_id = c.category_id
        LEFT JOIN payments p ON s.subscription_id = p.subscription_id
        ORDER BY s.subscription_id;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "subscription_id": row[0],
            "service_name": row[1],
            "plan_name": row[2],
            "status": row[3],
            "start_date": str(row[4]),
            "category_name": row[5],
            "price": row[6],
            "billing_cycle": row[7],
            "payment_day": row[8]
        })

    return jsonify(data)

# 新增訂閱
@app.route("/subscriptions", methods=["POST"])
def add_subscription():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()
    if start_date == "":
            start_date = None
    cur.execute("""
        INSERT INTO subscriptions 
        (user_id, category_id, service_name, plan_name, status, start_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING subscription_id;
    """, (
        data.get("user_id"),
        data.get("category_id"),
        data.get("service_name"),
        data.get("plan_name"),
        data.get("status"),
        data.get("start_date")
    )
    )
    subscription_id = cur.fetchone()[0]
    

    cur.execute("""
        INSERT INTO payments
        (subscription_id, price, billing_cycle, payment_day)
        VALUES (%s, %s, %s, %s);
    """, (
        subscription_id,
        data.get("price"),
        data.get("billing_cycle"),
        data.get("payment_day")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "新增成功", "subscription_id": subscription_id})

# 修改訂閱
@app.route("/subscriptions/<int:subscription_id>", methods=["PUT"])
def update_subscription(subscription_id):
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE subscriptions
        SET service_name=%s,
            plan_name=%s,
            status=%s,
            start_date=%s,
            category_id=%s
        WHERE subscription_id=%s;
    """, (
        data.get("service_name"),
        data.get("plan_name"),
        data.get("status"),
        data.get("start_date"),
        data.get("category_id"),
        subscription_id
    ))

    cur.execute("""
        UPDATE payments
        SET price=%s,
            billing_cycle=%s,
            payment_day=%s
        WHERE subscription_id=%s;
    """, (
        data.get("price"),
        data.get("billing_cycle"),
        data.get("payment_day"),
        subscription_id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "修改成功"})

# 刪除訂閱
@app.route("/subscriptions/<int:subscription_id>", methods=["DELETE"])
def delete_subscription(subscription_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM payments WHERE subscription_id=%s;", (subscription_id,))
    cur.execute("DELETE FROM subscriptions WHERE subscription_id=%s;", (subscription_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "刪除成功"})

if __name__ == "__main__":
    app.run(debug=True)