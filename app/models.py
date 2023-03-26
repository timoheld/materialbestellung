# Übernommen aus den Beispielen
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os

# Eigenentwicklung
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scoutname = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(256))
    bestellungen = db.relationship('Bestellung', backref='user', lazy=True)

    # Übernommen aus den Beispielen
    def __repr__(self):
        return '<User {}>'.format(self.scoutname)

    # Übernommen aus den Beispielen
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Übernommen aus den Beispielen
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Übernommen aus den Beispielen
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Eigenentwicklung
class Bestellung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activityDate = db.Column(db.DateTime)
    articles = db.relationship('Material', backref='bestellung', lazy=True)
    orderStatus = db.Column(db.Integer)

    def __repr__(self):
        return '<Bestellung {}>'.format(self.body)

# Eigenentwicklung
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bestellung_id = db.Column(db.Integer, db.ForeignKey('bestellung.id'))
    article = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(500))

# Eigenentwicklung
class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))
    role_description = db.Column(db.String(100))
    users = db.relationship('User', backref='roles', lazy=True)
