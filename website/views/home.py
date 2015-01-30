from flask import Blueprint, render_template, request, redirect, flash, url_for
from website import db
from website.forms import SignupForm
from website.models import Content, SignupCourses

mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    return render_template('home/index.html')

@mod.route('/about')
def about():
    data = Content.query.filter_by(content_id='teachers').first().content
    return render_template('home/about.html', data=data)

@mod.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if SignupCourses.query.filter_by(username=form.username.data,
                    email=form.email.data, coursename=form.coursename.data).count():
                m = 'It seems like you have already signed up for the {} course. We will contact you soon.'
            else:
                db.session.add(SignupCourses(form.username.data, form.email.data, form.phone.data, form.coursename.data))
                db.session.commit()
                m = 'You have signed up for the {} course. We will contact you soon about your application.'
            flash(m.format(form.coursename.data))
            return redirect(url_for('home.index'))
        for field in form.errors:
            for error in form.errors[field]:
                flash(error)
        return redirect(url_for('home.signup'))
    return render_template('home/signup.html', form=form)
