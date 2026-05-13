from flask import Flask, render_template
from flask import request, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"

db = SQLAlchemy(app)

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    courses = db.relationship(
        "Course",
        backref="student",
        lazy=True
    )

class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id")
    )

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        student_name = request.form["student"]
        course_title = request.form["course"]

        student = Student(name=student_name)

        db.session.add(student)
        db.session.commit()

        course = Course(
            title=course_title,
            student_id=student.id
        )

        db.session.add(course)
        db.session.commit()

        return redirect("/")

    students = Student.query.all()

    return render_template(
        "index.html",
        students=students
    )

if __name__ == "__main__":
    app.run(debug=True)
