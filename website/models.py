from passlib.hash import pbkdf2_sha512
from website import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(192))
    role = db.Column(db.String(32))
    fullname = db.Column(db.String(32))
    exam_id = db.Column(db.String(32))
    answer_page = db.Column(JSON)

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha512.encrypt(password)

    def check_password(self, password):
        return pbkdf2_sha512.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class SignupCourses(db.Model):
    __tablename__ = 'signupcourses'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    coursename = db.Column(db.String(32))

    def __repr__(self):
        return '<User {}>'.format(self.username, self.coursename)

class CompletedExams(db.Model):
    __tablename__ = 'oldexams'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    code = db.Column(db.String(32))
    taken_date = db.Column(db.Date)
    answer_page = db.Column(JSON)
    exam_score = db.Column(JSON)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.String())
    content = db.Column(JSON)

    def __repr__(self):
        return '<Content {}>'.format(self.content_id)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String())
    pages = db.Column(JSON)
    correct = db.Column(JSON)

    def __repr__(self):
        return '<Exam {}>'.format(self.exam_id)
