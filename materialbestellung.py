#from flask import Flask
#from flask import render_template
#app = Flask(__name__, template_folder='templates')

#import os

#@app.route("/")
#def index():
#    title='Materialbestellung Pfadi Angenstein'
#    return render_template('index.html', title=title)

#@app.route("/infos")
#def infos():
#    return __name__

#Applikation Starten
#app.run(debug=True,host='0.0.0.0',port=5000)

from app import app
