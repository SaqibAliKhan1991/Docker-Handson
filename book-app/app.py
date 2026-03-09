from flask import Flask, request, render_template_string
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secret'),
        dbname=os.environ.get('DB_NAME', 'bookdb')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    author VARCHAR(200) NOT NULL
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

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Book Library</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        input { padding: 8px; width: 45%; }
        button { padding: 8px 16px; background: #28a745; color: white; border: none; cursor: pointer; }
        ul { list-style: none; padding: 0; }
        li { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
        .delete { background: red; color: white; border: none; cursor: pointer; padding: 4px 8px; }
    </style>
</head>
<body>
    <h1>📚 Book Library</h1>
    <form method="POST" action="/add">
        <input type="text" name="title" placeholder="Book title..." required>
        <input type="text" name="author" placeholder="Author name..." required>
        <button type="submit">Add Book</button>
    </form>
    <br>
    <h3>All Books:</h3>
    <ul>
        {% for book in books %}
        <li>
            📖 {{ book[1] }} — by {{ book[2] }}
            <form method="POST" action="/delete/{{ book[0] }}" style="display:inline">
                <button class="delete">Delete</button>
            </form>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML, books=books)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (title, author))
    conn.commit()
    cur.close()
    conn.close()
    return index()

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return index()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
