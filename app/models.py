from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    avatar_url = db.Column(db.String(1024))

    picks = db.relationship('Pick', backref='author', lazy='dynamic')
    casts_hosting = db.relationship('Cast', backref='host', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Cast(db.Model):
    __tablename__ = 'casts'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))
    date = db.Column(db.String(80))
    cast_number = db.Column(db.Integer, unique=True)
    description = db.Column(db.Text)
    picture_url = db.Column(db.String(1024))

    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    picks = db.relationship('Pick', backref='cast', lazy='dynamic')

class Pick(db.Model):
    __tablename__ = 'picks'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(255), index=True)
    album = db.Column(db.String(255), index=True)
    song = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    picture_url = db.Column(db.String(1024))
    waffles_link = db.Column(db.String(1024))
    what_link = db.Column(db.String(1024))
    other_link = db.Column(db.String(1024))
    last_edited = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cast_id = db.Column(db.Integer, db.ForeignKey('casts.id'))