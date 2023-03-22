# Übernommen aus den Beispielen
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

# Übernommen aus den Beispielen
class LoginForm(FlaskForm):
    scoutname = StringField('Pfadiname', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Einloggen')

# Übernommen aus den Beispielen
class RegistrationForm(FlaskForm):
    scoutname = StringField('Pfadiname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Rolle', choices=[('1', 'Leiter'), ('2', 'Materialchef')], validators=[DataRequired()])
    submit = SubmitField('Registrieren')

    # Übernommen aus den Beispielen
    def validate_scoutname(self, scoutname):
        user = User.query.filter_by(scoutname=scoutname.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden einen anderen Pfadinamen!')
            
    # Übernommen aus den Beispielen
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden eine andere Email Adresse!')

# Eigenentwicklung
class BestellungForm(FlaskForm):
    activityDate = DateField("",validators=[DataRequired()], format='%Y-%m-%d')
    article = StringField("",validators=[DataRequired()])
    amount = StringField("",validators=[DataRequired()])
    description = StringField("")
    submit = SubmitField('Bestellen')



