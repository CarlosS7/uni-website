import os
import json
from website import db
from website.models import User, Content
from website.admin import add_admin, add_exam

db.reflect()
db.drop_all()
db.create_all()

os.chdir('tests/testdata')
with open('teachers.json') as f:
    content = json.load(f)
db.session.add(Content(content_id='teachers', content=content))
db.session.commit()

add_exam('silly1', os.path.join('exams', 'silly1.json'),
        os.path.join('exams', 'silly1_answers.json'))
add_admin('admin', 'pass', 'Admin')

user1 = User(username='1', role='examinee', fullname='Thomas Hardy', exam_id='silly1', answer_page='{}')
user1.hash_password('pass')
db.session.add(user1)
user2 = User(username='2', role='examinee', fullname='Franz Kafka', exam_id='silly1', answer_page='{}')
user2.hash_password('pass')
db.session.add(user2)
db.session.commit()
