import os
import json
from website import db
from website.models import User, Questions, Content

db.drop_all()
db.create_all()

pink = User('pink', 'theboss')
db.session.add(pink)
db.session.commit()

os.chdir('data/')
with open('teachers.json') as f:
    content = json.load(f)
    db.session.add(Content('teachers', content))

with open('initial.json') as f:
    question_page = json.load(f)
    db.session.add(Questions('silly1', 'initial', question_page))

with open('silly01.json') as f:
    question_page = json.load(f)
    db.session.add(Questions('silly1', 'silly01', question_page))

db.session.commit()
