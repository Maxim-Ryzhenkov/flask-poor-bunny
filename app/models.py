from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username}'

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Complaint(db.Model):
    __tablename__ = "complaints"
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_female = db.Column(db.Boolean, default=True)
    text = db.Column(db.String(500))

    def __repr__(self):
        return f'{self.text.capitalize()}'


class Consolation(db.Model):
    __tablename__ = "consolations"
    id = db.Column(db.Integer, primary_key=True)
    is_female = db.Column(db.Boolean, default=True)
    text = db.Column(db.String(500))

    def __repr__(self):
        return f'{self.text.capitalize()}'


db.create_all()
