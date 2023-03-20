# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired
# from app.models import User

# class LoginForm(FlaskForm):
#     scoutname = StringField('Pfadiname', validators=[DataRequired()])
#     password = PasswordField('Passwort', validators=[DataRequired()])
#     submit = SubmitField('Login')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    scoutname = StringField('Pfadiname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    scoutname = StringField('Pfadiname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_scoutname(self, scoutname):
        user = User.query.filter_by(scoutname=scoutname.data).first()
        if user is not None:
            raise ValidationError('Please use a different scoutname.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# class ArticlesForm(FlaskForm):
#     article = StringField("Artikel")
#     amount = StringField("Anzahl")
#     description = StringField("Beschreibung")


class BestellungForm(FlaskForm):
    activityDate = DateField("",validators=[DataRequired()], format='%Y-%m-%d')
    article = StringField("",validators=[DataRequired()])
    amount = StringField("",validators=[DataRequired()])
    description = StringField("")
    # articles = FieldList(FormField(ArticlesForm))
    submit = SubmitField('Bestellen')



