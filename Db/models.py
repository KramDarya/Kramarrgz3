from . import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    login = db.Column(db.String(200))
    password = db.Column(db.String(102), nullable=False)


class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    start_of_week = db.Column(db.Date, nullable=False)
    end_of_week = db.Column(db.Date, nullable=False)
    week_data = db.Column(db.Integer, nullable=False)

