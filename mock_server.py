from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# --- Mock Database Setup ---
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER, username TEXT, secret_info TEXT)')
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?)', [
        (1, 'admin', 'FLAG{SQL_INJECTION_MASTER}'),
        (2, 'alice', 'Personal_Data_001'),
        (3, 'bob', 'Internal_Project_X')
    ])
    conn.commit()
    return conn

db_conn = init_db()

@app.route("/api/v1/analyzer/test", methods=["GET"])
def sqli_vulnerable_endpoint():
    """
    VULNERABLE ENDPOINT: Uses string formatting for queries.
    Perfect for testing your campaign analyzer's detection logic.
    """
    user_id = request.args.get('id', '1')
    session_token = request.headers.get('X-Session-ID', 'GUEST_SESSION')
    
    # Intentional Vulnerability: f-string used in SQL query
    query = f"SELECT username, secret_info FROM users WHERE id = {user_id}"
    
    try:
        cursor = db_conn.cursor()
        # executescript allows multiple statements (for more advanced exploits)
        res = cursor.execute(query).fetchall()
        
        return jsonify({
            "status": "success",
            "executed_query": query,
            "session": session_token,
            "results": res,
            "security_level": "LOW (Vulnerable)"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "executed_query": query,
            "error_message": str(e),
            "hint": "Database error often indicates successful syntax breakage (SQLi)"
        }), 500

@app.route("/api/v1/analyzer/secure", methods=["GET"])
def sqli_secure_endpoint():
    """
    SECURE ENDPOINT: Uses parameterized queries.
    Use this to show your analyzer can distinguish between a vulnerability and a false positive.
    """
    user_id = request.args.get('id', '1')
    
    # Secure Method: Parameterized query
    query = "SELECT username, secret_info FROM users WHERE id = ?"
    
    cursor = db_conn.cursor()
    res = cursor.execute(query, (user_id,)).fetchall()
    
    return jsonify({
        "status": "success",
        "executed_query": "Protected via Parameterization",
        "results": res,
        "security_level": "HIGH (Secure)"
    }), 200

if __name__ == "__main__":
    print("SQLi Campaign Analyzer Test Server Active...")
    print("Target URL: http://127.0.0.1:5000/api/v1/analyzer/test?id=1")
    app.run(port=5000, debug=True)