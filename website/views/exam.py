import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user
from website import db
from website.models import Exams
from website.admin import login_required

mod = Blueprint('exam', __name__, url_prefix='/exam')

@mod.after_request
def add_no_cache(response):
    """Make sure that pages are not cached."""
    if current_user.is_authenticated():
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@mod.route('/')
@login_required(role='examinee')
def index():
    """Set exam for the user."""
    exam_id = current_user.exam_id
    answers = json.loads(current_user.answer_page)
    data = Exams.query.filter_by(exam_id=exam_id).first().pages
    return render_template('exam/index.html',
            welcome=data['pages'][0],
            pages=data['pages'][1:],
            answers=answers)

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
    answers = json.loads(current_user.answer_page)
    answers.update(results)
    current_user.answer_page = json.dumps(answers)
    db.session.commit()
