from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user, login_required
from website import db
from website.models import Questions
import random
import json

mod = Blueprint('exam', __name__, url_prefix='/exam')

@mod.after_request
def add_no_cache(response):
    """Make sure that pages are not cached."""
    if current_user.is_authenticated:
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@mod.route('/')
def index():
    """Check user is authenticated and randomly choose exam from database."""
    if current_user and current_user.is_authenticated:
        query = db.session.query(Questions.exam_id.distinct().label('exam_id'))
        exam_id = random.choice([row.exam_id for row in query.all()])
        data = Questions.query.filter_by(exam_id=exam_id, section_id='initial').first().question_page
        return render_template('exam/index.html', data=data)
    return redirect(url_for('user.login'))

@mod.route('/<exam_id>/section/<section_id>', methods=['GET', 'POST'])
@login_required
def section(section_id, exam_id):
    """Display question pages and get user's answers."""
    if request.method == 'POST':
        get_results(request.form.items(), exam_id)
        if section_id == 'finish':
            score = calc_score(get_score(exam_id))
            print(score)
            return redirect(url_for('exam.completed'))
        return redirect(url_for('exam.section', exam_id=exam_id, section_id=section_id))
    data = Questions.query.filter_by(exam_id=exam_id, section_id=section_id).first().question_page
    return render_template('exam/questions.html', data=data)

def get_results(items, exam_id):
    """Add the user's answers to the database."""
    results = {item[0]: item[1] for item in items}
    answers = json.loads(current_user.answer_page)
    answers.update(results)
    current_user.answer_page = json.dumps(answers)
    db.session.commit()

def get_score(exam_id):
    """Return a list of answers that are correct."""
    answers = json.loads(current_user.answer_page)
    data = Questions.query.filter_by(exam_id=exam_id).all()
    dicts = [ans for quest in data for ans in quest.question_page.get('correct', {})]
    correct = [key for d in dicts for key, val in d.items() if val == answers.get(key)]
    return correct

def calc_score(ans_list):
    return len(ans_list)

@mod.route('/completed')
def completed():
    return render_template('exam/completed.html')
