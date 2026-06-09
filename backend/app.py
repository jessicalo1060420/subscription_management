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
@app.route("/subscriptions/<int:user_id>", methods=["GET"])
def get_subscriptions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            s.subscription_id,
            s.service_name,
            s.plan_name,
            c.category_name,
            p.price,
            p.billing_cycle,
            p.payment_day
        FROM subscriptions s
        LEFT JOIN categories c ON s.category_id = c.category_id
        LEFT JOIN payments p ON s.subscription_id = p.subscription_id
        WHERE s.user_id = %s
        ORDER BY s.subscription_id;
    """,(user_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "subscription_id": row[0],
            "service_name": row[1],
            "plan_name": row[2],
            "category_name": row[3],
            "price": row[4],
            "billing_cycle": row[5],
            "payment_day": row[6]       
        })

    return jsonify(data)

# 新增訂閱
@app.route("/subscriptions", methods=["POST"])
def add_subscription():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()
    start_date = data.get("start_date")
    if start_date == "":
            start_date = None
    cur.execute("""
        INSERT INTO subscriptions 
        (user_id, category_id, service_name, plan_name)
        VALUES (%s, %s, %s, %s)
        RETURNING subscription_id;
    """, (
        data.get("user_id"),
        data.get("category_id"),
        data.get("service_name"),
        data.get("plan_name"),
        
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
            category_id=%s
        WHERE subscription_id=%s;
    """, (
        data.get("service_name"),
        data.get("plan_name"),
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
#註冊
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (user_name, user_email, user_password)
        VALUES (%s, %s, %s)
        RETURNING user_id;
    """, (
        data.get("user_name"),
        data.get("user_email"),
        data.get("user_password")
    ))

    user_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "註冊成功",
        "user_id": user_id
    }), 201

#登入
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, user_name, user_email
        FROM users
        WHERE user_name = %s AND user_password = %s;
    """, (
        data.get("user_name"),
        data.get("user_password")
    ))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({
            "message": "登入成功",
            "user_id": user[0],
            "user_name": user[1],
            "user_email": user[2]
        })

    return jsonify({
        "message": "帳號或密碼錯誤"
    }), 401

if __name__ == "__main__":
    app.run(debug=True)