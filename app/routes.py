from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from app import app
from app.models import User
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author':{'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author':{'username': 'Susan'},
            'body': 'The Avangers movie was so cool!'
        },
        {
            'author':{'username': 'Daniil'},
            'body': 'Hello! I want to become a python developer!'
        },
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect (url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

