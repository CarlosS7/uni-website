from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms import validators as valid

class LoginForm(Form):
    username = StringField('Username', [valid.Required('Please enter your name')])
    password = PasswordField('Password', [valid.Required('Please enter your password')])

class AddExaminee(Form):
    username = StringField('Username', [valid.Required('Please enter the examinee\'s name')])
    exam_id = SelectField('Exam ID', choices=[('pyueng5', 'PYU Entrance Exam 5'),
        ('pyueng8', 'PYU Entrance Exam 8')])

class GetScore(Form):
    username = StringField('Username', [valid.Required('Please enter the examinee\'s name')])

class SignupForm(Form):
    username = StringField('Name', [
        valid.Required('Please enter your name'),
        valid.Length(max=30, message='The name should be less than 30 characters long'),
        valid.Regexp('^[a-zA-Z\s]+$', message=('Name should only contain letters and spaces.'))])
    email = StringField('Email', [valid.Email()])
    phone = StringField('Phone number', [
        valid.Required('Please enter your phone number'),
        valid.Length(max=15, message='The name should be less than 15 numbers long'),
        valid.Regexp('^[0-9]+$', message=('Phone number can only contain numbers.'))])
    coursename = SelectField('Course', choices=[('IEP', 'Intensive English Program'), ('IELTS', 'IELTS Preparation'),
        ('TOEFL', 'TOEFL Preparation'), ('GE', 'General English'), ('TESOL', 'TESOL Certificate')])
