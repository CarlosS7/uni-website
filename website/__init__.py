from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_man = LoginManager()
login_man.init_app(app)

from website.views import home
from website.views import exam
from website.views import user
app.register_blueprint(home.mod)
app.register_blueprint(exam.mod)
app.register_blueprint(user.mod)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

from .models import User

login_man.login_view = 'user.login'

@login_man.user_loader
def load_user(id):
    return User.query.get(int(id))
