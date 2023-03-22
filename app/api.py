# Übernommen aus den Beispielen
from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from app import app, db
from app.models import User, Bestellung
import datetime

# Eigenentwicklung
# Der das JWT Modul (JSON Web Token) ermöglicht es im Python JWTs zu erstellen und zu verarbeiten
# JWT ist ein authentifizierungsberfahren welches oft für APIs verwendet wird
import jwt


auth = HTTPBasicAuth()

# Übernommen aus den Beispielen
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(scoutname=username).first()
    if user and user.check_password(password):
        return user
    return None

# In diesem Array müssen alle endpoints angegeben werden, welche über die token verifizierung verifiziert werden sollen
auth_endpoints = ['api_getUser', 'api_bestellungen']

# Eigenentwicklung
@app.before_request
def verify_token():
    if request.endpoint in auth_endpoints:
        # Überprüfung, ob ein JWT-Token im Request-Header enthalten ist
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization header is missing or invalid'}), 401

        # Extrahieren des JWT-Token aus dem Authorization-Header
        token = auth_header.replace('Bearer ', '')

        # Überprüfung, ob der JWT-Token gültig ist, fals der Token abgelaufen ist gibt es die Meldung 'Token has expired' zurück, falls er ungültig ist 'Invalid Token' 
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    return

# Eigenentwicklung
# Token generieren
@app.route('/api/token')
@auth.login_required
def generate_token():
    user = User.query.filter_by(scoutname=auth.username()).first()
    # Ablaufdatum für den Token erstellen
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    # JSON Web Token anhand der UserID, des Ablaufdatums und einem Secret Key erstellen
    token = jwt.encode({'user_id': user.id, 'exp': expiration}, 'secret_key')
    return jsonify({'token': token})

# Eigenentwicklung
# Alle Benutzer abfragen
@app.route('/api/users')
def api_getUser():
    users = User.query.all()
    results = []
    # Die Benutzerdaten in dem Array "results" speichern
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['scoutname'] = user.scoutname
        user_data['email'] = user.email
        results.append(user_data)    
    return jsonify(results)

# Eigenentwicklung
@app.route('/api/bestellungen/<userid>')
@app.route('/api/bestellungen')
def api_bestellungen(userid=None):
    results = []
    # Überprüfen ob eine UserID mitgegeben wurde
    if userid:
        # Falls die UserID mitgegeben wurde, nur die Bestellungen dieses Benutzers aus der Datenbank gelesen
        bestellungen = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).filter(Bestellung.user_id==userid).order_by(Bestellung.id.desc()).all()
    else:
        # Falls die UserID nicht mitgegeben wurde, werden alle Daten des Benutzers aus der Datenbank gelesen
        bestellungen = db.session.query(Bestellung, User).join(User, Bestellung.user_id == User.id).order_by(Bestellung.id.desc()).all()
    x = 0
    # Die aus der Datenbank geholten Bestellungen in dem Array "results" speichern
    for bestellung,user in bestellungen:
        bestellung_data = {}
        bestellung_data['id'] = bestellung.id
        bestellung_data['user'] = user.scoutname
        bestellung_data['activityDate'] = bestellung.activityDate
        # das "enumerat" ist eine Funktion welche einem array einen Index generiert, dadurch können die Artikel in einem weiteren array "art_data" hochgezählt werden und haben einen dynamischen Index
        art_data = {}
        for x, art in enumerate(bestellung.articles):
            art_data[x] = {
                'article': art.article,
                'amount': art.amount,
                'description': art.description
            }
        # Den art_data array in den bestellung_data array einfügen, sodass alle Artikel einer Bestellung in einem mehrdimensionalen Array gespeichert sind
        bestellung_data['articles'] = art_data
        results.append(bestellung_data)
    return jsonify(results)