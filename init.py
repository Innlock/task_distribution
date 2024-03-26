from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/task_distribution'
app.config['SECRET_KEY'] = 'task_distribution'
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
