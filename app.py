from flask import Flask, render_template, flash, redirect, url_for, session, send_from_directory, make_response, request
from models import db, migrate, Student, StudentAnswer
from studentSignup import SignupForm
from studentLogin import LoginForm
from flask_session import Session
from sqlalchemy import text
from functools import wraps
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
# from config import Config
import random

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aptech123@localhost/testdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://aseef:dmABnCUras8QT6CgApZk4BtEXz1MQIGX@dpg-cqalhmggph6c73f61sc0-a:5432/asf'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'aseef_swati_parth_prakash_ninad'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Session(app)

db.init_app(app)
migrate.init_app(app, db)
Bootstrap(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'contact' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('/exam/index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/student/studentsignup', methods=['GET', 'POST'])
def contact():
    form = SignupForm()
    if form.validate_on_submit():
        contact_number = str(form.contact.data).strip()
        existing_student = Student.query.filter_by(contact=contact_number).first()
        if existing_student:
            flash('Student already exists!')
            return render_template('/student/studentsignup.html', form=form)
        
        file = form.upload.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
            
        student = Student(
            fullname=form.fullname.data,
            contact=str(form.contact.data),
            address=form.address.data,
            password=form.password.data,
            profile_image=filename
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student_login'))
    return render_template('/student/studentsignup.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/student/studentlogin', methods=['GET', 'POST'])
def student_login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        check_contact_number = str(loginForm.contact.data).strip()
        check_password = loginForm.password.data
        existing_student = Student.query.filter_by(contact=check_contact_number).first()
        # existing_password = Student.query.filter_by(password=check_password).first()
        if existing_student and existing_student.password == check_password:
            session['contact'] = existing_student.id
            session['exam_over'] = True
            return render_template('/student/studentbase.html', student=existing_student)
        else:
            flash('Invalid contact number or password. Please try again or sign up.')
            return render_template('/student/studentlogin.html', loginForm=loginForm)
    return render_template('/student/studentlogin.html', loginForm=loginForm)

@app.route('/dashboard')
@login_required
def dashboard():
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        return render_template('studentbase.html', student=user)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('student_login'))

@app.route('/student/student-dashboard')
@login_required
def student_dashboard():
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        return render_template("/student/student_dashboard.html", student=user)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('student_login'))

@app.route('/student/student-exam')
@login_required
def student_exam():
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        data = get_course()
        db.session.execute(text('TRUNCATE TABLE student_answer'))
        db.session.commit()
        return render_template("/student/student_exam.html", student=user, coursedata=data)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('student_login'))

@app.route('/student/student-marks')
@login_required
def student_marks():
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        course = get_course()
        return render_template("/student/student_marks.html", student=user, coursedata=course)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('student_login'))

@app.route("/logout")
def student_logout():
    session.pop('contact', None)
    session.pop('exam_over', None)
    resp = make_response(redirect(url_for('student_login')))
    resp.set_cookie('Marks', '', expires=0)
    resp.set_cookie('Selected Answer', '', expires=0)
    return resp

@app.route('/start_exam/<int:exam_id>')
@login_required
def start_exam(exam_id):
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        questions = get_exam_questions(exam_id)
        random.shuffle(questions)
        resp = make_response(render_template('/student/start_exam.html', questions=questions, student=user))
        return resp
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('student_login'))

@app.route('/submit_marks', methods=['POST'])
@login_required
def submit_marks():
    if not session.get('exam_over'):
        return redirect(url_for('student_login'))
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
    if request.method == 'POST':
        courseID = request.form.get('course_no')
        selected_marks_string = request.form.get('selected_marks')
        
        selected_marks_list = selected_marks_string.split(',')
        marks_entries = []
        for mark in selected_marks_list:
            if mark:
                parts = mark.split(':')
                if len(parts) == 2:
                    marks_entries.append((parts[0], parts[1]))
        for mark_entry in marks_entries:
            new_marks = StudentAnswer(course_no=courseID, marks=mark_entry[1])
            db.session.add(new_marks)
        db.session.commit()
        return render_template('/student/check_marks.html', student=user)
    else:
        return 'Method not allowed', 405

@app.route("/view_marks/<int:exam_id>", methods=["GET"])
@login_required
def view_marks(exam_id):
    if 'contact' in session:
        user = Student.query.filter_by(id=session['contact']).first()
        data = get_course()
        stmt = text('''
            SELECT t1.course_id, COUNT(*) AS match_count 
            FROM (
                SELECT course_id, CorrectAnswer, ROW_NUMBER() OVER (ORDER BY course_id) AS row_num 
                FROM exam_questions 
                WHERE course_id = :course_id
            ) t1 
            JOIN (
                SELECT course_no, marks, ROW_NUMBER() OVER (ORDER BY course_no) AS row_num 
                FROM student_answer 
                WHERE course_no = :course_no
            ) t2 
            ON t1.row_num = t2.row_num 
            AND t1.CorrectAnswer = t2.marks 
            GROUP BY t1.course_id
        ''')
       
        results = db.session.execute(stmt, {'course_id': exam_id, 'course_no': exam_id}).fetchall()
        if not results:
            flash('no attempt.', 'warning')
            return render_template("/student/warning.html", student=user)
        
        return render_template("/student/view_result.html", results=results, courses=data, student=user)
    else:
        return redirect(url_for('login'))

def get_course():
    return db.session.execute(text("SELECT * FROM courses")).fetchall()

def get_exam_questions(exam_id):
    return db.session.execute(text("SELECT * FROM exam_questions WHERE course_id = :exam_id"), {'exam_id': exam_id}).fetchall()


@app.route("/teacherclick")
def teacherclick():
    return render_template("exam/index.html")

@app.route("/aboutus")
def aboutus():
    return render_template("exam/aboutus.html")

if __name__ == "__main__":
    app.run()
# if __name__ == "__main__":
#     with app.app_context():
#             db.create_all()
#     app.run(debug=True)
