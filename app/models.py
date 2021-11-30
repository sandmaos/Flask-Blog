import datetime
from app import db
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
import hashlib
from datetime import datetime


# class Log(db.Model):
#     __tablename__ = 'logs'
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(150))
#     time = db.Column(db.DateTime)
#     ip = db.Column(db.String(100))


class Post(db.Model):
    __tablename__ = 'posts'
    author = db.Column(db.String(30), default='hi',)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    comment = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    authors_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    posts = db.relationship('Post', backref='authors', lazy='dynamic')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, index=True)
    name = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about = db.Column(db.Text())
    birth = db.Column(db.Date)

    # member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


    @property
    def password(self):
        raise AttributeError('The password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    # timestamp = db.Column(db.DateTime, default=datetime.utcnow)