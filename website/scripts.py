import json
import random
from datetime import datetime
from flask.ext.login import current_user
from functools import wraps
from website import login_man, db
from website.models import Questions, CompletedExams

def login_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_man.unauthorized()
            if current_user.role != role:
                return login_man.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def get_score(user):
    """Return a list of answers that are correct."""
    answers = json.loads(user.answer_page)
    exam_id = user.exam_id
    data = Questions.query.filter_by(exam_id=exam_id).first().correct
    score = [key for key, val in data.items() if val == answers.get(key)]
    return score

def calc_score(ans_list):
    listening = structure = reading = 0
    for ans in ans_list:
        if ans.split('_')[1] == 'list':
            listening += 1
        elif ans.split('_')[1] == 'struct':
            structure += 1
        else:
            reading += 1
    return listening, structure, reading

def update_db(user, exam_score):
    answer_page = json.loads(user.answer_page)
    taken_date = datetime.utcnow()
    db.session.add(CompletedExams(user.username, taken_date, answer_page, exam_score))
    db.session.delete(user)
    db.session.commit()

def record_scores(user, writing):
    exams = {'pyueng5': 'PYU Entrance Exam 5', 'pyueng8': 'PYU Entrance Exam 8'}
    exam_id = exams.get(user.exam_id)
    listening, structure, reading = calc_score(get_score(user))
    total = round(((listening + structure + reading + 55) * 11.6/3) - 23.5 + (writing * 7.83))
    exam_score = {'exam_id': exam_id, 'listening': listening, 'structure': structure,
            'reading': reading, 'writing': writing, 'total': total}
    update_db(user, exam_score)

def rand_password():
    alphabet = '23456789;:!@#$%^&*()abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'
    myrg = random.SystemRandom()
    length = 10
    return ''.join(myrg.choice(alphabet) for i in range(length))
