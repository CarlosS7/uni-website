from flask import Blueprint, render_template
from website.models import Content

mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    data = Content.query.filter_by(content_id='home').first().content
    return render_template('home/index.html', home_data=data)

@mod.route('/about')
def about():
    data = Content.query.filter_by(content_id='about').first().content
    return render_template('home/about.html', about_data=data)
