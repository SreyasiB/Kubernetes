from flask import Flask, jsonify
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT content FROM messages LIMIT 1;")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": result[0]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)