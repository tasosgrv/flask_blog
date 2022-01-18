from email.policy import default
from enum import unique

from sqlalchemy import ForeignKey
from FlaskBlogApp import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)
    profile_image = db.Column(db.String(30), default="default_profile_image.jpg")
    articles = db.relasionship('Article', 'author', lazy=True)

    def __repr__(self) -> str:
        return f"{self.username} {self.email}"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_body = db.Column(db.String(250), nullable=False)
    article_image = db.Column(db.String(30), default="default_article_image.jpg")
    date_created = db.Column(db.datetime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"{self.date_created} {self.article_title}"