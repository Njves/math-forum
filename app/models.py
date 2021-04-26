from datetime import datetime

from flask_login import UserMixin

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Problem', backref='author', lazy='dynamic')
    tokens = db.Column(db.Integer, default=100)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_start_tokens_kit(self):
        self.tokens = 150

    def set_tokens(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        return 'user: {}, {}, {}'.format(self.username, self.email, self.tokens)


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    expression = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_level = db.Column(db.Integer, default=1)
    image = db.Column(db.String(128))
    section = db.Column(db.String(128), default='Арифметика')
    value = db.Column(db.Integer, default=100)

    def __repr__(self):
        return f'Problem:id: {self.id}, body:{self.body}, expression: {self.expression}, class_level={self.class_level}, image: {self.image}'
