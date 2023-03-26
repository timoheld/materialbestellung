# Übernommen aus den Beispielen
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_httpauth import HTTPBasicAuth

# Übernommen aus den Beispielen
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, api
