import random
from flask import render_template, url_for, request, redirect, flash, session
from app import app, db
from app.forms import LoginForm, ComplainForm
from app.models import User, Complaint, Consolation
from flask_login import current_user, login_user, logout_user, login_required, user_logged_in
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/main/')
def choose_gender():
    session.clear()
    return render_template('choose_gender.html')


@app.route('/male/')
def male():
    session['gender'] = 'мужчина'
    return redirect(url_for('complain'))


@app.route('/female/')
def female():
    session['gender'] = 'женщина'
    return redirect(url_for('complain'))


@app.route('/unknown/')
def unknown():
    session['gender'] = 'неизвестно'
    return redirect(url_for('complain'))


@app.route('/complain/', methods=['GET', 'POST'])
def complain():
    form = ComplainForm()

    if form.validate_on_submit():
        return redirect(url_for('consolation'))
    return render_template('complain.html', form=form)


@app.route('/consolation/')
def consolation():
    gender = session.get('gender')
    rand = random.randrange(1, db.session.query(Consolation).count())
    consolation = Consolation.query.get(int(rand))
    return render_template('consolation.html', consolation=consolation)


@app.route('/account/<username>/')
def account(username):
    return render_template('account.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('choose_gender'))
    form = LoginForm()

    if form.validate_on_submit():
        user_query = db.session.query(User).filter(
            db.or_(User.username == form.username.data, User.email == form.username.data))
        user = user_query.first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя или пароль.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('choose_gender')
        return redirect(next_page)

    return render_template('auth.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('choose_gender'))
