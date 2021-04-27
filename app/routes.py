from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, ProblemForm, RegistrationForm
from app.math_text_converter import MathTextConverter
from app.models import User, Problem
from app import db
from app.token_calc import TokenCalculator


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    posts = Problem.query.all()
    if request.method == 'POST':
        res = request.form

        if res['solve'] == '':
            return render_template("index.html", posts=posts, posts_len=len(posts))
        pr = Problem.query.filter_by(id=res['id']).first()
        pr.solve = res['solve']
        current_user.tokens += pr.value // 2
        db.session.add(pr)
        db.session.commit()

    return render_template("index.html", posts=posts, posts_len=len(posts))


@app.route('/problem', methods=['GET', 'POST'])
@login_required
def problem():
    form = ProblemForm()
    if form.validate_on_submit():
        if int(form.class_level.data) > 11:
            flash("Выберите коректный класс")
            return render_template('problem.html', form=form)
        image = MathTextConverter.getImage(form.expression.data)
        current_problem = Problem(body=form.body.data, expression=form.expression.data,
                                  class_level=form.class_level.data, image=image, author=current_user)
        current_problem.value = TokenCalculator().calculate_task_value(current_problem)
        current_problem.section = form.sections.data
        print(current_user.tokens, current_problem.value)
        if current_user.tokens >= current_problem.value:
            current_user.tokens -= current_problem.value
            db.session.add(current_problem)
            db.session.commit()
            flash(
                f"Задача успешно создана! Она оценина в {current_problem.value} токенов \nУ вас осталось {current_user.tokens}")
        else:
            flash(f"Стоимость задачи {current_problem.value}")
            flash(f"У вас не хватает токенов")
            flash(f"Ваш текущий баланс {current_user.tokens} токенов")

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
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_start_tokens_kit()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/save')
def save():

    return redirect('index')
