from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, BestellungForm
from app.models import User, Bestellung, Material
# from flask_user import roles_required
import itertools
import jwt

def get_next_id(table_name):
    sequence_name = db.session.execute(f"SHOW CREATE TABLE {table_name}").fetchone()[1].split()[-1]
    next_id = db.session.execute(f"SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = '{table_name}'").fetchone()[0]
    return next_id

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


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
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(scoutname=form.scoutname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/bestellung', methods=['GET', 'POST'])
@login_required
def bestellung():
    if current_user.role != 1:
        return redirect(url_for('login'))
    if request.method == 'POST':
        best_id = get_next_id("bestellung")
        bestellung = Bestellung(id=best_id, user_id=current_user.id, activityDate=request.form['datum'], orderStatus=1)
        db.session.add(bestellung)
        articles = request.form.getlist('articles[]')
        amounts = request.form.getlist('amounts[]')
        descriptions = request.form.getlist('descriptions[]')
        for art, amt, des in zip(articles, amounts, descriptions):
            material = Material(bestellung_id=best_id, article=art, amount=amt, description=des)
            db.session.add(material)
        db.session.add(bestellung)
        db.session.commit()
        flash('Bestellung wurde versendet!')
    return render_template('bestellung.html', title='Bestellung')


@app.route('/showOrders', methods=['GET'])
@login_required
def showBestellungen():
    if current_user.role != 2:
        return redirect(url_for('login'))
    newOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.orderStatus==1).order_by(Bestellung.id.desc()).all()
    oldOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.orderStatus==2).order_by(Bestellung.id.desc()).all()
    return render_template('showOrders.html', newOrders=newOrders, oldOrders=oldOrders)

@app.route('/acceptOrder/<int:id>', methods=['GET', 'POST'])
def acceptOrder(id):
    order = Bestellung.query.get(id)
    if request.method == 'POST':
        order.orderStatus = 2
        flash('Bestellung wurde Akzeptiert!')
        db.session.commit()
    return "accept"

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    # myOrders = Bestellung.query.filter_by(user_id=current_user.id)
    myOrders = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.user_id==current_user.id).order_by(Bestellung.id.desc()).all()
    return render_template('profile.html', myOrders=myOrders)

# API

@app.route("/api")
def index_view():
    return jsonify(msg="This is the API for the 'Materialbestellungs-Tool' form Pfadi Anngenstein!")