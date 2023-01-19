from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fasdkjlfhe3iqruh34345'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

from fileStorage.models import User

login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from fileStorage import views
from fileStorage import admin_views