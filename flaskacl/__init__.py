from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#create database instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#connects app to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mydbsecret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from flaskacl import routes