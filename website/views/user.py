from flask import Blueprint, render_template, redirect, flash, url_for
from flask.ext.login import current_user, login_user, logout_user
from website.models import User
from website.forms import LoginForm

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.route('/')
def index():
    if current_user and current_user.is_authenticated:
        return render_template('exam/index.html')
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
        return redirect(url_for('exam.index'))
    return render_template('user/login.html', form=form)

@mod.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home.index'))
