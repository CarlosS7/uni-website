import json
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, current_user
from website import db
from website.models import User, Questions
from website.forms import SigninForm
from website.scripts import login_required

mod = Blueprint('exam', __name__, url_prefix='/exam')

@mod.after_request
def add_no_cache(response):
    """Make sure that pages are not cached."""
    if current_user.is_authenticated():
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@mod.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(code=form.code.data).first()
        if not user or user.role != 'examinee' or not user.check_password(form.password.data):
            flash('Invalid credentials.')
            return redirect(url_for('exam.signin'))
        login_user(user)
        return redirect(url_for('exam.index'))
    return render_template('exam/signin.html', form=form)

@mod.route('/')
@login_required(role='examinee')
def index():
    """Set exam for the user."""
    exam_id = current_user.exam_id
    data = Questions.query.filter_by(exam_id=exam_id).first().pages
    return render_template('exam/index.html', welcome=data['pages'][0], pages=data['pages'][1:])

@mod.route('/update_results', methods=['POST'])
@login_required(role='examinee')
def update_results():
    """Get user's answers."""
    get_results(request.get_json())
    return json.dumps({'status': 'ok'})

@mod.route('/finish', methods=['POST'])
@login_required(role='examinee')
def finish():
    """Get user's answers and logout user."""
    get_results(request.form.items())
    return redirect(url_for('user.logout'))

def get_results(items):
    """Add the user's answers to the database."""
    if isinstance(items, dict):
        results = items
    else:
        results = {item[0]: item[1] for item in items if item[0] != 'csrf_token'}
    print(results)
    answers = json.loads(current_user.answer_page)
    answers.update(results)
    current_user.answer_page = json.dumps(answers)
    db.session.commit()
