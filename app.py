import sqlite3
import os
from flask import Flask, render_template, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
from log_reader import LogReader

app = Flask(__name__)
log_reader = LogReader()
os.makedirs('data', exist_ok=True)

# =====================
# DATABASE
# =====================
def init_db():
    conn = sqlite3.connect('data/logs.db')
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check if 'source' column exists
        cursor.execute("PRAGMA table_info(logs)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'source' not in columns:
            print("⚠️  Old database schema detected. Recreating...")
            conn.close()
            os.remove('data/logs.db')
            conn = sqlite3.connect('data/logs.db')
            cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            hostname TEXT,
            service TEXT,
            message TEXT,
            suspicion_score INTEGER DEFAULT 0,
            source TEXT DEFAULT 'unknown',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized")
# =====================
# LOG MANAGEMENT
# =====================
def save_logs_to_db(logs):
    conn = sqlite3.connect('data/logs.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM logs')
    
    for log in logs:
        cursor.execute('''
            INSERT INTO logs (timestamp, hostname, service, message, suspicion_score, source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            log['timestamp'], log['hostname'], log['service'], 
            log['message'], 0, log.get('source', 'unknown')
        ))
    
    conn.commit()
    conn.close()

# =====================
# ML DETECTION
# =====================
def detect_anomalies():
    conn = sqlite3.connect('data/logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, message FROM logs')
    rows = cursor.fetchall()
    
    if len(rows) < 5:
        conn.close()
        return {'status': 'error', 'message': 'Not enough logs'}
    
    ids = [row[0] for row in rows]
    messages = [row[1] for row in rows]
    
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(messages)
    
    clf = IsolationForest(contamination=0.1, random_state=42)
    predictions = clf.fit_predict(X)
    
    anomaly_count = 0
    for i, pred in enumerate(predictions):
        score = 1 if pred == -1 else 0
        if score == 1:
            anomaly_count += 1
        cursor.execute('UPDATE logs SET suspicion_score = ? WHERE id = ?', (score, ids[i]))
    
    conn.commit()
    conn.close()
    return {'status': 'success', 'analyzed': len(messages), 'anomalies': anomaly_count}

# =====================
# ROUTES
# =====================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/logs')
def get_logs():
    conn = sqlite3.connect('data/logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': row[0], 'timestamp': row[1], 'hostname': row[2],
        'service': row[3], 'message': row[4], 'suspicion_score': row[5],
        'source': row[6]
    } for row in rows])

@app.route('/api/analyze', methods=['POST'])
def analyze_logs():
    return jsonify(detect_anomalies())

@app.route('/api/refresh', methods=['POST'])
def refresh_logs():
    logs = log_reader.read_logs(max_logs=100)
    save_logs_to_db(logs)
    return jsonify({'status': 'refreshed', **detect_anomalies()})

@app.route('/api/system-info')
def system_info():
    return jsonify({
        'os': log_reader.system,
        'computer_name': os.environ.get('COMPUTERNAME', 'Unknown'),
        'log_source': 'real' if log_reader.system == 'Windows' else 'sample'
    })

# =====================
# MAIN
# =====================
if __name__ == '__main__':
    print("🛡️  LogSentinel Starting...")
    print("=" * 50)
    init_db()
    logs = log_reader.read_logs(max_logs=100)
    save_logs_to_db(logs)
    detect_anomalies()
    print("=" * 50)
    print("✅ Ready! Open http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)