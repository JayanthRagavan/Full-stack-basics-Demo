from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create database and table if not exist
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# POST route to store name and return all users
@app.route('/submit', methods=['POST'])
def submit():
    name = request.json.get('name')

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()

    # Get all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return jsonify({
        'message': f'Hello, {name}!',
        'users': [{'id': u[0], 'name': u[1]} for u in users]
    })

# Optional: separate API to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify([{'id': u[0], 'name': u[1]} for u in users])

if __name__ == '__main__':
    app.run(debug=True)
