

from flask import Flask, request, render_template,flash,redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "student_management"

# Database initialization
conn = sqlite3.connect('students.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students
             (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT, 
              age INTEGER,
              course TEXT)''')
conn.commit()
@app.route("/")
def home():
    c.execute("SELECT COUNT(*) FROM students")
    total_students = c.fetchone()[0]
    c.execute("SELECT * FROM students LIMIT 5")
    recent_students = c.fetchall()
    c.execute("SELECT COUNT(DISTINCT course) FROM students")
    total_count = c.fetchone()[0]
    c.execute("SELECT AVG(age) FROM students")
    avg_age = c.fetchone()[0]
    return render_template("index.html", total_students=total_students, recent_students=recent_students,total_count=total_count,avg_age=avg_age)
@app.route("/add_student")
def add_student():
    return render_template("add_student.html")
@app.route("/add_student", methods=["POST"])
def add_student_post():
    name = request.form.get("name")
    age = request.form.get("age")
    course = request.form.get("course")  
    c.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
    conn.commit()
    flash("Student Added Successfully!")
    return redirect("/")
@app.route("/view_students")
def view_students():
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    return render_template(
        "view_student.html",
        students=students
    )
@app.route("/search_student")
def search_student():
    return render_template("search_student.html")
@app.route("/search_student",methods=["POST"])
def search_student_post():
    name = request.form.get("name")
    c.execute("SELECT * FROM students WHERE name=?", (name,))
    students = c.fetchall()
    return render_template("student_results.html", students=students)
@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    flash("Student Deleted Successfully!")
    return redirect("/view_students")
    

@app.route("/edit_student/<int:student_id>")
def edit_student(student_id):
    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = c.fetchone()
    return render_template("edit_student.html", student=student)
@app.route("/update_student/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form.get("name")
    age = request.form.get("age")
    course = request.form.get("course")
    c.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?", (name, age, course, student_id))
    conn.commit()
    flash("Student Updated Successfully!")
    return redirect("/view_students")
    
app.run(debug=True)  

