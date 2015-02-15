import json
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, logout_user, current_user
from website.models import User, SignupCourses, CompletedExams
from website.forms import LoginForm
from website.scripts import login_required, record_scores, rand_password

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
    check = len([user for user in users if json.loads(user.answer_page)])
    signup = SignupCourses.query.all()
    old = [exam.username for exam in CompletedExams.query.all()]
    return render_template('user/index.html', check=check, signup=signup, old=old)

@mod.route('/addexaminee', methods=['POST'])
@login_required(role='admin')
def addexaminee():
    name = next(request.form.items())[-1]
    password = rand_password()
    return '<label>Name: {} Password: {}</label>'.format(name, password)

@mod.route('/examscore', methods=['POST'])
@login_required(role='admin')
def examscore():
    name = next(request.form.items())[-1]
    exams = CompletedExams.query.filter_by(username=name).all()
    scores = [exam.exam_score for exam in exams]
    print(scores)
    return render_template('user/showscore.html', name=name, scores=scores)

@mod.route('/editpage')
@login_required(role='admin')
def editpage():
    pass

@mod.route('/examwriting', methods=['GET', 'POST'])
@login_required(role='admin')
def examwriting():
    if request.method == 'POST':
        for userdata in request.form.items():
            user = User.query.filter_by(username=userdata[0]).first()
            if user:
                writing = float(userdata[1] or 0)
                writing = writing if writing <= 6 else 0
                record_scores(user, writing)
    users = User.query.all()
    check = [check_writing(username) for username in users if json.loads(username.answer_page)]
    return render_template('user/examwriting.html', check=check)

def check_writing(user):
    answers = json.loads(user.answer_page)
    writing = answers.get('writing')
    return (user.username, writing)
