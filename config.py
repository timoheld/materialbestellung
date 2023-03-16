import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Master01@materialbestellung-mysqldb-1:3306/materialbestellung" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
