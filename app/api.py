from flask import jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from app import app, db
from app.models import User, Bestellung
import jwt
import datetime

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(scoutname=username).first()
    if user and user.check_password(password):
        return user
    return None

# In diesem Array müssen alle endpoints angegeben werden, welche über die token verifizierung verifiziert werden sollen
auth_endpoints = ['api_getUser', 'api_bestellungen']

@app.before_request
def verify_token():
    if request.endpoint in auth_endpoints:
        # Überprüfe, ob ein JWT-Token im Request-Header enthalten ist
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization header is missing or invalid'}), 401

        # Extrahiere den JWT-Token aus dem Authorization-Header
        token = auth_header.replace('Bearer ', '')

        # Überprüfe, ob der JWT-Token gültig ist
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    return

# Token generieren
@app.route('/api/token')
@auth.login_required
def generate_token():
    user = User.query.filter_by(scoutname=auth.username()).first()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({'user_id': user.id, 'exp': expiration}, 'secret_key')
    # user.token = token
    # db.session.commit()
    return jsonify({'token': token})

# Alle Benutzer abfragen
@app.route('/api/users')
def api_getUser():
    users = User.query.all()
    results = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['scoutname'] = user.scoutname
        user_data['email'] = user.email
        results.append(user_data)    
    return jsonify(results)

@app.route('/api/bestellungen/<userid>')
@app.route('/api/bestellungen')
def api_bestellungen(userid=None):
    results = []
    if userid:
        bestellungen = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.user_id==userid).order_by(Bestellung.id.desc()).all()
    else:
        bestellungen = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).order_by(Bestellung.id.desc()).all()
    x = 0
    for bestellung,user in bestellungen:
        bestellung_data = {}
        bestellung_data['id'] = bestellung.id
        bestellung_data['user'] = user.scoutname
        bestellung_data['activityDate'] = bestellung.activityDate
        # das "enumerat" ist eine Funktion welche einem array einen Index generiert
        art_data = {}
        for x, art in enumerate(bestellung.articles):
            art_data[x] = {
                'article': art.article,
                'amount': art.amount,
                'description': art.description
            }
        bestellung_data['articles'] = art_data
        results.append(bestellung_data)
    return jsonify(results)