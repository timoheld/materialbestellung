from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, BestellungForm
from app.models import User, Bestellung, Material
import itertools

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

# @app.route('/bestellung', methods=['GET', 'POST'])
# @login_required
# def bestellung():
#     form = BestellungForm()
#     if form.validate_on_submit():
#         bestellung = Bestellung(scoutname=current_user.id, activityDate=form.activityDate.data, article=form.article.getlist, amount=form.amount.data, description=form.description.data)
#         db.session.add(bestellung)
#         db.session.commit()
#         flash('Bestellung wurde versendet!')
#     return render_template('bestellung.html', title='Bestellung', form=form)

@app.route('/bestellung', methods=['GET', 'POST'])
@login_required
def bestellung():
    if request.method == 'POST':
        best_id = get_next_id("bestellung")
        bestellung = Bestellung(id=best_id, scoutname=current_user.id, activityDate=request.form['datum'])
        db.session.add(bestellung)
        articles = request.form.getlist('articles[]')
        amounts = request.form.getlist('amounts[]')
        descriptions = request.form.getlist('descriptions[]')
        # x = []
        for art, amt, des in zip(articles, amounts, descriptions):
            material = Material(bestellung_id=best_id, article=art, amount=amt, description=des)
            db.session.add(material)
            # x.append([art, amt, des])
        # bestellung = Bestellung(scoutname=current_user.id, activityDate=request.form['datum'], articles=str(x))
        db.session.add(bestellung)
        db.session.commit()
        flash('Bestellung wurde versendet!')
    return render_template('bestellung.html', title='Bestellung')


# @app.route('/showOrders' emthods['GET'])
# @login_required
# def showBestellungen():
#     articles = Bestellung.query.all()
#     return render_template('showOrders.html', articles=articles)





    # form  = BestellungForm()
    # if request.method == 'POST' and form.validate():
    #     # entries = []
    #     for article_form in form.articles:
    #         article = ArticlesForm(article=article_form.article.data, amount=article_form.amount.data, description=article_form.description.data)
    #         db.session.add(article)
    #         db.session.flush()
    #         bestellung = Bestellung() 
    #         db.session.add()
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form)

    # if form.validate_on_submit():
    #     response = "Form Contents <pre>%s</pre>" % "<br/>\n".join(["%s:%s" % item for item in form.items()] )
    #     # return render_template('testsubmit.html', activityDate=form.activityDate.data, article=form.article.getlist)
    #     return response
    # return render_template('test.html', form=form)
