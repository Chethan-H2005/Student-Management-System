from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                    (name, age, course))
        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add.html')

# View Students
@app.route('/view')
def view():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()

    return render_template('view.html', students=data)

# Delete Student
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/view')

# Update Student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        cur.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                    (name, age, course, id))
        conn.commit()
        conn.close()

        return redirect('/view')

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()

    return render_template('update.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)