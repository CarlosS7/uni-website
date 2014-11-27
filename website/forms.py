from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms import validators as valid

class LoginForm(Form):
    username = TextField('Username', [valid.Required('Please enter your name')])
    password = PasswordField('Password', [valid.Required('Please enter your password')])

class SignupForm(Form):
    username = TextField('Name', [
        valid.Required('Please enter your name'),
        valid.Length(max=35, message='The name should be less than 35 characters long'),
        valid.Regexp('[a-zA-Z]+', message=('Name can only contain letters.'))])
    email = TextField('Email', [valid.Email()])
    phone = TextField('Phone number', [
        valid.Required('Please enter your phone number'),
        valid.Length(max=15, message='The name should be less than 15 numbers long'),
        valid.Regexp('[0-9]+', message=('Phone number can only contain numbers.'))])
    coursename = SelectField('Course', choices=[('IEP', 'Intensive English Program'), ('IELTS', 'IELTS Preparation'),
        ('TOEFL', 'TOEFL Preparation'), ('GE', 'General English'), ('TESOL', 'TESOL Certificate')])
