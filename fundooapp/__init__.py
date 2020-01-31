from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@12345@localhost:5432/fundoonotes'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

