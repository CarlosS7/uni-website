import json
from drat import app
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, logout_user, current_user
from website import db
from website.models import User, Questions, SignupCourses, CompletedExams
from website.forms import LoginForm
from website.admin import login_required, record_scores, add_examinees

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.after_request
def add_no_cache(response):
    """Make sure that pages are not cached."""
    if current_user.is_authenticated():
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid credentials.')
            return redirect(url_for('user.login'))
        login_user(user)
        if user.role == 'admin':
            return redirect(url_for('user.index'))
        else:
            return redirect(url_for('exam.index'))
    return render_template('user/login.html', form=form)

@mod.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home.index'))

@mod.route('/')
@login_required(role='admin')
def index():
    users = User.query.all()
    check = [check_writing(username) for username in users if json.loads(username.answer_page)]
    signup = SignupCourses.query.all()
    exams = [q.exam_id for q in Questions.query.all()]
    old = list(set([exam.taken_date for exam in CompletedExams.query.all()]))
    return render_template('user/index.html', check=check, signup=signup, exams=exams, old=old)

@mod.route('/delsignup', methods=['POST'])
@login_required(role='admin')
def delsignup():
    for user in SignupCourses.query.all():
        db.session.delete(user)
        db.session.commit()
    return '<p>No students to contact.</p>'

@mod.route('/addexaminee', methods=['POST'])
@login_required(role='admin')
def addexaminee():
    items = dict(request.get_json())
    [name, password, fullname, exam_id] = add_examinees([items.get('name'),
        items.get('fullname'), items.get('exam_id')])
    button = items.get('button', False)
    return render_template('partials/shownamepass.html',
            fullname=fullname, name=name, password=password, button=button)

@mod.route('/examscore', methods=['POST'])
@login_required(role='admin')
def examscore():
    items = dict(request.get_json())
    date = items.get('getscore')
    exams = CompletedExams.query.filter_by(taken_date=date).all()
    scores = [(exam.username, exam.exam_score) for exam in exams]
    return render_template('partials/showscore.html', scores=scores)

@mod.route('/examwriting', methods=['POST'])
@login_required(role='admin')
def examwriting():
    items = dict(request.get_json())
    for data in items:
        user = User.query.filter_by(username=data).first()
        if user:
            writing = float(items.get(data) or 0)
            writing = writing if writing <= 6 else 0
            record_scores(user, writing)
    return str(datetime.now().date())

def check_writing(user):
    answers = json.loads(user.answer_page)
    writing = answers.get('writing')
    return (user.username, user.fullname, writing)

@mod.route('/textanalysis', methods=['POST'])
@login_required(role='admin')
def textanalysis():
    data = dict(request.get_json()).get('text')
    message = app.raw_check(data)
    return render_template('partials/dratreport.html', message=message.splitlines())
