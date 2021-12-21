from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/gestion_biblotecaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = True
app.secret_key = "bibliotec"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


import biblioteca.routers