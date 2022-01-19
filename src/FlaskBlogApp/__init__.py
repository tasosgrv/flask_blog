from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)

app.config["SECRET_KEY"] = 'fa41efa0758221558203292e6df640971d56'
app.config["WTF_CSRF_SECRET_KEY"] = '6680d2e8b86b1be39f3f1fd422a7cc075ea1'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask_course_database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=10)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='danger'
login_manager.login_message="Κάντε <a href='/login/'>σύνδεση</a> η <a href='/signup/'>εγγραφή</a> για να δειτε αυτή τη σελίδα"

from FlaskBlogApp import routes, models