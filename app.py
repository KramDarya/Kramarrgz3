from flask import Flask, redirect, session, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from rgz import rgz
from Db import db
from Db.models import Users, Vacation
from flask_login import LoginManager
from datetime import datetime, timedelta


app = Flask(__name__)

app.secret_key = "123"
user_db = "darya_knowledge_base"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "knowledge_base_4"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()

login_manager.login_view = "rgz.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return Users.query.get(int(user_id))

app.register_blueprint(rgz)

@app.route("/")
def main():
    return render_template('rgz.html')