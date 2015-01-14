import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user
from website import db
from website.models import Questions
from website.scripts import login_required

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
    """Check user is authenticated and set exam."""
    exam_id = current_user.exam_id
    data = Questions.query.filter_by(exam_id=exam_id, section_id='initial').first().question_page
    return render_template('exam/index.html', data=data)

@mod.route('/<exam_id>/section/<section_id>', methods=['GET', 'POST'])
@login_required(role='examinee')
def section(exam_id, section_id):
    """Display question pages and get user's answers."""
    if request.method == 'POST':
        get_results(request.form.items(), exam_id)
        if section_id == 'finish':
            return redirect(url_for('user.logout'))
        return redirect(url_for('exam.section', exam_id=exam_id, section_id=section_id))
    data = Questions.query.filter_by(exam_id=exam_id, section_id=section_id).first().question_page
    return render_template('exam/questions.html', data=data)

def get_results(items, exam_id):
    """Add the user's answers to the database."""
    results = {item[0]: item[1] for item in items if item[1]}
    answers = json.loads(current_user.answer_page)
    answers.update(results)
    current_user.answer_page = json.dumps(answers)
    db.session.commit()
