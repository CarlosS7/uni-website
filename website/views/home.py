from flask import Blueprint, render_template

mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    return render_template('home/index.html')

@mod.route('/about')
def about():
    return render_template('home/about.html')
