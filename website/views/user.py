import json
from itertools import groupby
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, logout_user
from website import db
from website.models import User, Questions
from website.forms import LoginForm
from website.scripts import login_required

mod = Blueprint('user', __name__, url_prefix='/user')

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
    flash('You have been logged out')
    return redirect(url_for('home.index'))

@mod.route('/')
@login_required(role='admin')
def index():
    users = User.query.all()
    check = [check_writing(user) for user in users if json.loads(user.answer_page)]
    return render_template('user/index.html', check=check) # also add signups to this page

@mod.route('/editpage')
@login_required(role='admin')
def editpage():
    pass

@mod.route('/examscores', methods=['POST'])
@login_required(role='admin')
def examscores():
    for user in request.form.items():
        if user[0] != 'csrf_token':
            username, writing = user[0], int(user[1])
            groups = calc_score(get_score(username))
            listening, structure, reading = len(groups[0]), len(groups[1]), len(groups[2])
            user = User.query.filter_by(username=username).first()
            user.exam_score = listening + structure + reading + writing
            db.session.commit()
            clear_answers(username)
    return redirect(url_for('user.index'))

def check_writing(user):
    answers = json.loads(user.answer_page)
    writing = answers.get('writing')
    return (user.username, writing)

def get_score(username):
    """Return a list of answers that are correct."""
    user = User.query.filter_by(username=username).first()
    answers = json.loads(user.answer_page)
    exam_id = user.username.split('_')[0]
    data = Questions.query.filter_by(exam_id=exam_id).all()
    dicts = [ans for quest in data for ans in quest.question_page.get('correct', {})]
    correct = [key for d in dicts for key, val in d.items() if val == answers.get(key)]
    return correct

def calc_score(ans_list):
    correct = sorted(ans_list)
    groups = []
    for k, g in groupby(correct, key=lambda x: x.split('_')[1]): # need to work on this
        groups.append(list(g))
    return groups

def clear_answers(username):
    user = User.query.filter_by(username=username).first()
    user.answer_page = json.dumps({})
    db.session.commit()
