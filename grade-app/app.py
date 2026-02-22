from flask import Flask, request

app = Flask(__name__)

# Sample data to start with
students = [
    {"name": "Ahmed", "grade": 85},
    {"name": "Sara", "grade": 92},
    {"name": "Ali", "grade": 78}
]

@app.route('/')
def home():
    result = '<h1>Student Grade Calculator</h1>'
    result += '<h2>All Students:</h2>'
    for s in students:
        result += f'<p>{s["name"]} → Grade: {s["grade"]}</p>'
    return result

@app.route('/add')
def add():
    name = request.args.get('name', 'Unknown')
    grade = int(request.args.get('grade', 0))
    students.append({"name": name, "grade": grade})
    return f'<h2>Added {name} with grade {grade}</h2>'

@app.route('/average')
def average():
    avg = sum(s['grade'] for s in students) / len(students)
    return f'<h2>Class Average: {avg:.2f}</h2>'

@app.route('/highest')
def highest():
    top = max(students, key=lambda s: s['grade'])
    return f'<h2>Highest Grade: {top["name"]} with {top["grade"]}</h2>'

@app.route('/lowest')
def lowest():
    low = min(students, key=lambda s: s['grade'])
    return f'<h2>Lowest Grade: {low["name"]} with {low["grade"]}</h2>'

@app.route('/health')
def health():
    return {'status': 'ok', 'students': len(students)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
