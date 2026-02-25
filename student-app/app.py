from flask import Flask, request, redirect
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres-db'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secret'),
        database=os.environ.get('DB_NAME', 'mydb')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    grade INT
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database ready!")
            return
        except Exception as e:
            print(f"Database not ready yet, retrying... ({e})")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to database after 5 retries")

@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students ORDER BY id DESC')
    students = cur.fetchall()
    cur.close()
    conn.close()
    html = '''
    <h1>Student Registration</h1>
    <form action="/register" method="POST">
        <p>Name: <input type="text" name="name" required></p>
        <p>Grade: <input type="number" name="grade" required></p>
        <p><input type="submit" value="Register Student"></p>
    </form>
    <h2>Registered Students:</h2>
    '''
    for s in students:
        html += f'<p>ID: {s[0]} | Name: {s[1]} | Grade: {s[2]}</p>'
    return html

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    grade = request.form['grade']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO students (name, grade) VALUES (%s, %s)', (name, grade))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Practice 1 by Saqib!'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
