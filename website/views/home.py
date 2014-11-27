from flask import Blueprint, render_template
from website.models import Content

mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    return render_template('home/index.html')

@mod.route('/about')
def about():
    data = Content.query.filter_by(content_id='teachers').first().content
    return render_template('home/about.html', data=data)

@mod.route('/courses')
def courses():
    return render_template('home/courses.html')
