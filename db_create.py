import os
import json
from website import db
from website.models import User, Questions, Content

db.reflect()
db.drop_all()
db.create_all()

def add_users(namelist):
    for name in namelist:
        db.session.add(User(name[0], name[1]))
    db.session.commit()

def add_questions(dirname):
    for path in os.listdir(dirname):
        if path.endswith('json'):
            section_id = path.rstrip('.json')
            with open(os.path.join(dirname, path)) as f:
                question_page = json.load(f)
            db.session.add(Questions(dirname, section_id, question_page))
    db.session.commit()

os.chdir('data')
with open('teachers.json') as f:
    content = json.load(f)
db.session.add(Content('teachers', content))
db.session.commit()

add_users([['user1', 'user1'], ['user2', 'user2'], ['user3', 'user3']])
add_questions('silly1')
