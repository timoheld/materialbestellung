# from app import db
# from flask_login import UserMixin

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scoutname = db.Column(db.String(50), index=True, unique=True)
#     surname = db.Column(db.String(50), index=True)
#     lastname = db.Column(db.String(50), index=True)
#     password_hash = db.Column(db.String(80))

#     def __repr__(self):
#         return '<User {}>'.format(self.scoutname)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

############### older
# from app import db, login
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scoutname = db.Column(db.String(50), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')

#     def __repr__(self):
#         return '<User {}>'.format(self.scoutname)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scoutname = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.scoutname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Bestellung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scoutname = db.Column(db.Integer, db.ForeignKey('user.id'))
    orderDate = db.Column(db.DateTime)
    activityDate = db.Column(db.DateTime)
    pickUpDate = db.Column(db.DateTime)
    returnDate = db.Column(db.DateTime)
    # articles = db.Column(db.String(500))
    # amount = db.Column(db.Integer)
    # description = db.Column(db.String(500))

    def __repr__(self):
        return '<Bestellung {}>'.format(self.body)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bestellung_id = db.Column(db.Integer, db.ForeignKey('bestellung.id'))
    article = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(500))