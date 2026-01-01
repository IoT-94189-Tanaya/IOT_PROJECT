from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_env"
)

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT temperature, humidity, gas, created_at
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    cursor.close()

    return render_template("index.html", row=row)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)