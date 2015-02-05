import os
import json
from website import db
from website.models import User, Questions, Content

db.reflect()
db.drop_all()
db.create_all()

def add_users(namelist):
    for name in namelist:
        db.session.add(User(*name))
    db.session.commit()

def add_questions(exams):
    for exam_id in exams:
        with open(os.path.join('exams', '{}.json'.format(exam_id))) as questions:
            pages = json.load(questions)
        with open(os.path.join('exams', '{}_answers.json'.format(exam_id))) as answers:
            correct = json.load(answers)
        db.session.add(Questions(exam_id, pages, correct))
    db.session.commit()

os.chdir('tests/testdata')
with open('teachers.json') as f:
    content = json.load(f)
db.session.add(Content('teachers', content))
db.session.commit()

add_users([['admin', 'default', 'admin'], ['humpty', 'dumpty', 'examinee', 'silly1']])
add_questions(['silly1'])
db.session.commit()
