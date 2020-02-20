from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email


class MailForm(FlaskForm):
    """ Форма отправки сообщения """
    subject = StringField('Тема сообщения',
                          validators=[DataRequired(message="Невежливо игнорировать тему сообщения"),
                                      Length(min=2, max=50,
                                             message="Тема должна быть не короче 2 и не длиннее 50 символов")])
    email = StringField('Почта',
                        validators=[Email(message='Введите правильный адрес почты'),
                                    DataRequired()])
    body = TextAreaField('Сообщение',
                         validators=[DataRequired(),
                                     Length(min=4, message='Ваше сообщение слишком короткое')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    """ Форма входа в аккаунт """
    username = StringField('Имя или почта',
                           validators=[DataRequired(), ])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message='Пожалуйста, введите пароль')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class ComplainForm(FlaskForm):
    """ Форма жалобы для бедного зайки """

    sex = RadioField('Вы', choices=[('female', 'женщина'), ('male', 'мужчина')])
    complain_text = TextAreaField('Опишите вашу проблему',
                          validators=[DataRequired(),
                                      Length(min=2, message='Пожалуйста, не молчи, даже от простого "Ох" или "ой" тебе полегчает, точно точно!')])
    submit = SubmitField('Пожаловаться')
