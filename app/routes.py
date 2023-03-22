# Übernommen aus den Beispielen
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, BestellungForm
from app.models import User, Bestellung, Material

# Eigenentwicklung -> Das Modul wird in api.py erklärt
import jwt

# Eigenentwicklung
# Diese Funktion holt aus der Datenbank aus den Tabellen informationen die nächste ID für die angegebene tabelle
# Dies wird verwendet, damit Bestellungen und die dazugehörigen Artikel im gleichen DB Commit eingefügt werden können. Da die Articel die ID der Bestellung brauchen weil dies der Foreign Key ist
def get_next_id(table_name):
    sequence_name = db.session.execute(f"SHOW CREATE TABLE {table_name}").fetchone()[1].split()[-1]
    next_id = db.session.execute(f"SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = '{table_name}'").fetchone()[0]
    return next_id

# Eigenentwicklung
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

# Übernommen aus den Beispielen
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(scoutname=form.scoutname.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid scoutname or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)

# Übernommen aus den Beispielen
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Übernommen aus den Beispielen
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(scoutname=form.scoutname.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Eigenentwicklung
@app.route('/bestellung', methods=['GET', 'POST'])
@login_required
def bestellung():
    # Es wird überprüft ob der Benutzer die Rolle 1 (Leiter) hat ansonsten kann der Benutzer diese Funktion nicht ausführen
    if current_user.role != 1:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Die nächste id wird aus der DB geholt
        best_id = get_next_id("bestellung")
        bestellung = Bestellung(id=best_id, user_id=current_user.id, activityDate=request.form['datum'], orderStatus=1)
        db.session.add(bestellung)
        # Die Getlist funktion kann daten aus einem Form Array holen
        articles = request.form.getlist('articles[]')
        amounts = request.form.getlist('amounts[]')
        descriptions = request.form.getlist('descriptions[]')
        # Durch die "zip" funktion können drei arrays in der selben for-schleife eingelesen werden
        # Dies wird gebraucht da mehrere Artikel mit den dazugegörigen Anzahl und Beschreibung bestellt werden können
        for art, amt, des in zip(articles, amounts, descriptions):
            material = Material(bestellung_id=best_id, article=art, amount=amt, description=des)
            db.session.add(material)
        db.session.add(bestellung)
        db.session.commit()
        flash('Bestellung wurde versendet!')
    return render_template('bestellung.html', title='Bestellung')

# Eigenentwicklung
@app.route('/showOrders', methods=['GET'])
@login_required
def showBestellungen():
    # Es wird überprüft ob der Benutzer die Rolle 2 (Materialchef) hat ansonsten kann der Benutzer diese Funktion nicht ausführen
    if current_user.role != 2:
        return redirect(url_for('login'))
    # Durch die Join funktion können zwei tabellen über den Foreign Key eingelesen werden
    newOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.orderStatus==1).order_by(Bestellung.id.desc()).all()
    oldOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.orderStatus==2).order_by(Bestellung.id.desc()).all()
    return render_template('showOrders.html', newOrders=newOrders, oldOrders=oldOrders)

# Eigenentwicklung
@app.route('/acceptOrder/<int:id>', methods=['GET', 'POST'])
def acceptOrder(id):
    order = Bestellung.query.get(id)
    if request.method == 'POST':
        order.orderStatus = 2
        flash('Bestellung wurde Akzeptiert!')
        db.session.commit()
    return "accept"

# Eigenentwicklung
@app.route('/profile', methods=['GET'])
@login_required
def profile():
     # Durch die Join funktion können zwei tabellen über den Foreign Key eingelesen werden
    myOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.user_id==current_user.id).order_by(Bestellung.id.desc()).all()
    return render_template('profile.html', myOrders=myOrders)