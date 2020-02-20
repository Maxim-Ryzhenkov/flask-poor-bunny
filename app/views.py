import random
from flask import render_template, url_for, request, redirect, flash, session
from app import app, db
from app.forms import LoginForm, ComplainForm
from app.models import User, Complaint, Consolation
from flask_login import current_user, login_user, logout_user, login_required, user_logged_in
from werkzeug.urls import url_parse


@app.route('/', methods=['POST', 'GET'])
def main():
    form = ComplainForm()
    if request.method == 'GET':
        form.sex.data = 'female'

    if form.validate_on_submit():
        rand = random.randrange(0, db.session.query(Consolation).count())
        consolation = Consolation.query.get(int(rand))
        return render_template('consolation.html', consolation=consolation)

    return render_template('main.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
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
            next_page = url_for('main')
        return redirect(next_page)

    return render_template('auth.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    session['cart'] = []
    return redirect(url_for('main'))
