import json
from itertools import groupby
from flask import Blueprint, render_template, redirect, flash, url_for
from flask.ext.login import current_user, login_user, logout_user
from website import db
from website.models import User, Questions
from website.forms import LoginForm
from website.scripts import login_required

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.route('/')
def index():
    """Check user is authenticated."""
    if current_user and current_user.is_authenticated():
        return render_template('user/index.html')
    return redirect(url_for('user.login'))

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

@mod.route('/editpage')
@login_required(role='admin')
def editpage():
    pass

@mod.route('/examcheck')
@login_required(role='admin')
def examcheck():
    users = User.query.all()
    check = [user for user in users if json.loads(user.answer_page)]
    return render_template('user/examcheck.html', check=check)

def get_score(exam_id, username):
    """Return a list of answers that are correct."""
    user = User.query.filter_by(username=username).first()
    answers = json.loads(user.answer_page)
    data = Questions.query.filter_by(exam_id=exam_id).all()
    dicts = [ans for quest in data for ans in quest.question_page.get('correct', {})]
    correct = [key for d in dicts for key, val in d.items() if val == answers.get(key)]
    return correct

def calc_score(ans_list):
    correct = sorted(ans_list)
    groups = []
    for k, g in groupby(correct, key=lambda x: x.split('_', 1)):
        groups.append(list(g))
    return groups

def clear_answers(username):
    user = User.query.filter_by(username=username).first()
    user.answer_page = json.dumps({})
    db.session.commit()
