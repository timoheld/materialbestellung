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
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Einloggen')


class RegistrationForm(FlaskForm):
    scoutname = StringField('Pfadiname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_scoutname(self, scoutname):
        user = User.query.filter_by(scoutname=scoutname.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden einen anderen Pfadinamen!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden eine andere Email Adresse!')

class BestellungForm(FlaskForm):
    activityDate = DateField("",validators=[DataRequired()], format='%Y-%m-%d')
    article = StringField("",validators=[DataRequired()])
    amount = StringField("",validators=[DataRequired()])
    description = StringField("")
    submit = SubmitField('Bestellen')



