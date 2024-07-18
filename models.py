from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(25), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    profile_image = db.Column(db.String(255), nullable=False)

class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_no = db.Column(db.Integer,nullable=False)
    marks = db.Column(db.String(100),nullable=False)
