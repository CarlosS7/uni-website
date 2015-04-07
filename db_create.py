import os
import json
from website import db
from website.models import User, Questions, Content

db.reflect()
db.drop_all()
db.create_all()

def add_questions(exams):
    for exam_id in exams:
        with open(os.path.join('exams', '{}.json'.format(exam_id))) as questions:
            pages = json.load(questions)
        with open(os.path.join('exams', '{}_answers.json'.format(exam_id))) as answers:
            correct = json.load(answers)
        db.session.add(Questions(exam_id=exam_id, pages=pages, correct=correct))
    db.session.commit()

os.chdir('tests/testdata')
with open('teachers.json') as f:
    content = json.load(f)
db.session.add(Content(content_id='teachers', content=content))
db.session.commit()

admin = User(username='admin', role='admin', fullname='Admin')
user1 = User(username='1', role='examinee', fullname='Thomas Hardy', exam_id='silly1', answer_page='{}')
user2 = User(username='2', role='examinee', fullname='Franz Kafka', exam_id='silly1', answer_page='{}')
user3 = User(username='3', role='examinee', fullname='Ernest Hemingway', exam_id='silly1', answer_page='{}')
for user in (admin, user1, user2, user3):
    user.hash_password('pass')
    db.session.add(user)
db.session.commit()

add_questions(['silly1'])
