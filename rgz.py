from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, Blueprint
from Db import db
from Db.models import Users, Vacation
from flask_login import login_user, login_required, current_user, logout_user
import psycopg2
from datetime import date, timedelta

rgz = Blueprint("rgz", __name__)

@rgz.route("/rgz/")
def main():
    return render_template('rgz.html')

@rgz.route("/rgz/check")
def check():
    my_users = Users.query.all()
    print(my_users)
    return "resuit in console"

@rgz.route("/rgz/glavn") 
def glavn (): 
    visibleUser = "Anon"
    
    if current_user is not None and current_user.is_authenticated:
        visibleUser = current_user.username

    elif 'username' in session: 
        visibleUser = session['username'] 
    
    return render_template('glavn.html', username=visibleUser)

@rgz.route("/rgz/users")
def users():
    names = [user.username for user in Users.query.all()] 
    return render_template('users.html', names=names)


@rgz.route("/rgz/register", methods=["GET", "POST"])
def registerPage():
    errors = {}
    visibleUser = "Anon"

    if request.method == "GET":
        return render_template("register.html")

    username_form = request.form.get("username")
    login_form = request.form.get("login")
    password_form = request.form.get("password")

    def is_valid_input(text):
        pattern = r"^[a-zA-Z0-9.,!?-]+$"  
        return bool(re.match(pattern, text))

    if username_form == '' or login_form == '' or password_form == '':
        errors = "Заполните все поля"
        return render_template("register.html", errors=errors)

    if not all(is_valid_input(value) for value in (login_form, password_form)):
        errors = "Логин и пароль должны состоять только из латинских букв, цифр и знаков препинания"
        return render_template("register.html", errors=errors)

    existing_user = Users.query.filter_by(username=username_form).first()

    if existing_user is not None:
        errors = "Пользователь уже существует"
        return render_template("register.html", errors=errors)

    hashesPswd = generate_password_hash(password_form, method='pbkdf2')
    new_user = Users(username=username_form, login=login_form, password=hashesPswd)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/rgz/login")


@rgz.route("/rgz/login", methods=["GET", "POST"])
def login():
    errors = []

    visibleUser = "Anon"

    if request.method == "GET":
        return render_template("login2.html")

    username_form = request.form.get("username")
    login_form = request.form.get("login")
    password_form = request.form.get("password")

    if username_form == '' or login_form == '' or password_form == '':
        errors.append("Заполните все поля")
        return render_template("login2.html", errors=errors, username=visibleUser)

    existing_user = Users.query.filter_by(username=username_form).first()

    if existing_user is None:
        errors.append("Нет такого пользователя")
        return render_template("login2.html", errors=errors, username=visibleUser)
    else:
        if check_password_hash(existing_user.password, password_form):
            login_user(existing_user, remember=False)
            return redirect("/rgz/calendarer")
        else:
            errors.append("Неправильный пароль")
            return render_template("login2.html", errors=errors, username=visibleUser)

@rgz.route('/rgz/calendarer', methods=['GET', 'POST']) 
@login_required 
def calendarer(): 
    visibleUser = current_user.username 
    week_data = [] 
 
    if request.method == "POST": 
        start_of_week = request.form.get("start_of_week") 
        end_of_week = request.form.get("end_of_week") 
 
        if start_of_week and end_of_week: 
            new_vacation = Vacation(user_id=current_user.id, start_of_week=start_of_week, end_of_week=end_of_week) 
            db.session.add(new_vacation) 
            db.session.commit() 
            return redirect("/rgz/vacations") 
 
    today = date.today() 
    start_of_year = date(today.year, 1, 1) 
 
    for i in range(1, 49): 
        start_of_week = start_of_year + timedelta(weeks=i - 1) 
        end_of_week = start_of_year + timedelta(weeks=i) - timedelta(days=1) 
        week_data.append({"number": i, "start_of_week": start_of_week.strftime('%Y-%m-%d'), "end_of_week": end_of_week.strftime('%Y-%m-%d')}) 
 
    return render_template("calendarer.html", visibleUser=visibleUser, week_data=week_data, username=visibleUser) 

@rgz.route('/rgz/vacations') 
@login_required 
def vacations(): 
    visibleUser = current_user.username 
    selected_weeks = Vacation.query.filter_by(user_id=current_user.id).all() 
 
    return render_template("vacations.html", visibleUser=visibleUser, selected_weeks=selected_weeks) 

  
@rgz.route('/rgz/all_vacations') 
def all_vacations(): 
    names = [user.username for user in Users.query.all()] 
    selected_weeks = Vacation.query.filter_by(user_id=current_user.id).all() 
    return render_template("user_vacations.html", selected_weeks=selected_weeks, names=names) 


@rgz.route('/rgz/logout') 
@login_required 
def logout(): 
    logout_user()
    return redirect("/rgz")

@rgz.route("/rgz/delete_account", methods=["POST"]) 
@login_required  
def delete_account(): 
    if request.method == "POST": 
        user_to_delete = Users.query.filter_by(username=visibleUser).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect("/rgz/glavn") 
    




