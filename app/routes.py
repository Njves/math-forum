from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, ProblemForm
from app.math_text_converter import MathTextConverter
from app.models import User, Problem


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    print(users)
    return render_template("index.html", users=users)


@app.route('/problem', methods=['GET', 'POST'])
@login_required
def problem():
    form = ProblemForm()
    if form.validate_on_submit():
        image = MathTextConverter.getImage(form.expression.data)
        current_problem = Problem(body=form.body.data, expression=form.expression.data,
                                  class_level=form.class_level.data, image=image)
        print(current_problem)
    return render_template('problem.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

