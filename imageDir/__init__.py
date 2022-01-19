from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siteDatabase.db'
# app.config['STORAGE'] = 'static/images'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)

from imageDir import routes