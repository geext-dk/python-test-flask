from app.models import User, Role
from app.users import users
from flask import redirect, render_template, session, request, g
import json

# Страница списка пользователей
@users.route("/users", methods=["GET"])
def users_page():
    if g.user is None:
        return redirect("/login")

    users = g.db.query(User).all()
    return render_template("users.html", users=users)

# Методы получения пользователей и сохранения пользователей
# Внимание: метод получения пользователей по факту не используется.
# P. S.: В больших приложениях было бы лучше отделить логику от view, например, создав дополнительные классы для 
# бизнес-логики (сервисы), но в таком маленьком, думаю, простительно
@users.route("/api/users", methods=["GET", "POST"])
def api_users():
    # Анонимные пользователи не могут использовать этот метод
    if g.user is None:
        return "Unauthorized", 401

    if request.method == "GET":
        users = g.db.query(User).all()
        return json.dumps(users)

    elif request.method == "POST":
        # если не админ, возвращаем 403
        if g.user.role != Role.ADMIN:
            return "Forbidden", 403
        
        json_data = json.loads(request.data.decode("utf-8"))
        if "login" not in json_data or "password" not in json_data or "role" not in json_data:
            return "Invalid JSON payload", 400
        
        login = json_data["login"]
        password = json_data["password"]
        role_str = json_data["role"]
        if not role_str.isdigit():
            return "A role must be a positive integer number", 400

        role = int(role_str)

        # Сохраняем пользователя в БД
        user = User(login=login, password=password, role=role)
        g.db.add(user)
        g.db.commit()
        return "", 204

# Методы удаления и изменения пользователей
@users.route("/api/users/<user_id>", methods=["DELETE", "PUT"])
def user_actions(user_id):
    # Анонимные пользователи не могут использовать этот метод
    if g.user is None:
        return "Unauthorized", 401

    # если не админ, возвращаем 403
    if g.user.role != Role.ADMIN:
        return "Forbidden", 403

    user = g.db.query(User).filter_by(id=user_id).first()
    if user is None:
        return "User not found", 404

    if request.method == "DELETE":
        g.db.delete(user)
        g.db.commit()
        return "", 204
    else:
        json_data = json.loads(request.data.decode("utf-8"))
        user.lgoin = json_data["login"]
        user.password = json_data["password"]
        user.role = int(json_data["role"])

        g.db.commit()

        return "", 204