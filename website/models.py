from passlib.context import CryptContext
from website import db
from sqlalchemy.dialects.postgresql import JSON


pwd_ctx = CryptContext(schemes=['sha512_crypt', 'pbkdf2_sha512'],
        default='pbkdf2_sha512')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(192))
    role = db.Column(db.String(32))
    fullname = db.Column(db.String(32))
    exam_id = db.Column(db.String(32))
    answer_page = db.Column(JSON)

    def __init__(self, username, password, role, fullname='', exam_id='', answer_page='{}'):
        self.username = username
        self.hash_password(password)
        self.role = role
        self.fullname = fullname
        self.exam_id = exam_id
        self.answer_page = answer_page

    def hash_password(self, password):
        self.password_hash = pwd_ctx.encrypt(password)

    def check_password(self, password):
        return pwd_ctx.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_role(self):
        return self.role

    def __repr__(self):
        return '<User {}>'.format(self.username)

class SignupCourses(db.Model):
    __tablename__ = 'signupcourses'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    coursename = db.Column(db.String(32))

    def __init__(self, username, email, phone, coursename):
        self.username = username
        self.email = email
        self.phone = phone
        self.coursename = coursename

    def __repr__(self):
        return '<User {}>'.format(self.username, self.coursename)

class CompletedExams(db.Model):
    __tablename__ = 'oldexams'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    taken_date = db.Column(db.Date)
    answer_page = db.Column(JSON)
    exam_score = db.Column(JSON)

    def __init__(self, username, taken_date, answer_page, exam_score):
        self.username = username
        self.taken_date = taken_date
        self.answer_page = answer_page
        self.exam_score = exam_score

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.String())
    content = db.Column(JSON)

    def __init__(self, content_id, content):
        self.content_id = content_id
        self.content = content

    def __repr__(self):
        return '<Content {}>'.format(self.content_id)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String())
    pages = db.Column(JSON)
    correct = db.Column(JSON)

    def __init__(self, exam_id, pages, correct):
        self.exam_id = exam_id
        self.pages = pages
        self.correct = correct

    def __repr__(self):
        return '<Exam {}>'.format(self.exam_id)
