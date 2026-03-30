import os
import time
import psycopg2
from flask import Flask, request, redirect

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secret'),
        dbname=os.environ.get('DB_NAME', 'notesdb')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL
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
    <title>Notes App</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        input, textarea { padding: 8px; width: 100%; margin-bottom: 10px; }
        button { padding: 8px 16px; background: #28a745; color: white; border: none; cursor: pointer; }
        .note { padding: 15px; border: 1px solid #ddd; margin-bottom: 10px; border-radius: 4px; }
        .delete { background: red; color: white; border: none; cursor: pointer; padding: 4px 8px; float: right; }
    </style>
</head>
<body>
    <h1>📝 Notes App</h1>
    <input type="text" id="title" placeholder="Note title..." />
    <textarea id="content" rows="3" placeholder="Note content..."></textarea>
    <button onclick="addNote()">Add Note</button>
    <br><br>
    <h3>My Notes:</h3>
    {% for note in notes %}
    <div class="note">
        <form method="POST" action="/delete/{{ note[0] }}" style="display:inline">
            <button class="delete" type="submit">Delete</button>
        </form>
        <strong>{{ note[1] }}</strong>
        <p>{{ note[2] }}</p>
    </div>
    {% endfor %}
    <script>
        function addNote() {
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            fetch('/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, content})
            }).then(() => location.reload());
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    from flask import render_template_string
    return render_template_string(HTML, notes=notes)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', 
                (data['title'], data['content']))
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
