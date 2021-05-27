from app.models import User, seed, Session, sql_engine
from app.auth import auth
from flask import render_template, g, redirect, session, request
import json

# Страница входа
@auth.route("/login", methods=["GET"])
def login_page():
    if g.user is not None:
        return redirect("/users")

    return render_template("login.html")

# API-метод входа
# Авторизация происходит путем добавление в session пользователя его логина.
# В Production, конечно, такое лучше не пихать, потому что такие сессии нельзя инвалидировать.
# Правильнее было бы хранить в куках пользователя только идентификатор сессии.
# Однако это все еще приемлемо, потому что куки дополнительно шифруются с помощью app.secret_key
@auth.route("/api/login", methods=["POST"])
def api_login():
    if g.user is not None:
        return "", 204
    json_data = json.loads(request.data.decode("utf-8"))
    login = json_data["login"]
    password = json_data["password"]
    user = g.db.query(User).filter_by(login=login, password=password).first()
    if user is None:
        return "Invalid login or password", 401
    
    session["login"] = login
    return "", 204

# API-метод логаута
@auth.route("/api/logout", methods=["POST"])
def api_logout():
    if g.user is None:
        return "", 204
    
    session.pop("login")

    return "", 204