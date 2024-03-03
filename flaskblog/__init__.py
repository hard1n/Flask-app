from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
# config values of the app
app.config['SECRET_KEY'] = 'cf6c0c0039ad00a386c898d6c6e773c2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import routes