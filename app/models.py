from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scoutname = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    bestellungen = db.relationship('Bestellung', backref='user', lazy=True)
    token = db.Column(db.String(150), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.scoutname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # # Token erzeugen (Übernommen aus den Beispielen)
    # def get_token(self, expires_in=3600):
    #     now = datetime.utcnow()
    #     if self.token and self.token_expiration > now + timedelta(seconds=60):
    #         return self.token
    #     self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    #     self.token_expiration = now + timedelta(seconds=expires_in)
    #     db.session.add(self)
    # # Token zerstören (Übernommen aus den Beispielen)
    # def revoke_token(self):
    #     self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    # Token überprüfen (Übernommen aus den Beispielen)
    # @staticmethod
    # def check_token(token):
    #     user = User-query.filter_by(token=token).first()
    #     if user is None or user.token_expiration < datetime.utcnow():
    #         return None
    #     return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Bestellung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    orderDate = db.Column(db.DateTime)
    activityDate = db.Column(db.DateTime)
    pickUpDate = db.Column(db.DateTime)
    returnDate = db.Column(db.DateTime)
    articles = db.relationship('Material', backref='bestellung', lazy=True)
    orderStatus = db.Column(db.Integer)

    def __repr__(self):
        return '<Bestellung {}>'.format(self.body)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bestellung_id = db.Column(db.Integer, db.ForeignKey('bestellung.id'))
    article = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(500))

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))
    role_description = db.Column(db.String(100))
    users = db.relationship('User', backref='roles', lazy=True)
