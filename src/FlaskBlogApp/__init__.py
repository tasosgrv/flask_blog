from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = 'fa41efa0758221558203292e6df640971d56'
app.config["WTF_CSRF_SECRET_KEY"] = '6680d2e8b86b1be39f3f1fd422a7cc075ea1'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask_course_database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

from FlaskBlogApp import routes