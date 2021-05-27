from flask import Flask, session, g, redirect
from config import Config
from app.models import User, sql_engine, Session, seed

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

def find_user_by_session():
    if "login" not in session:
        return None
    
    user_login = session["login"]
    return g.db.query(User).filter_by(login=user_login).first()

@app.before_first_request
def before_first_request():
    seed(sql_engine)

@app.before_request
def before_request():
    if "db" not in g:
        g.db = Session()

    if "user" not in g:
        g.user = find_user_by_session()

@app.teardown_appcontext
def teardown_app_request(_):
    db = g.pop("db", None)

    if db is not None:
        db.close()

@app.errorhandler(404)
def not_found_handler(_):
    return redirect('/login')

from .auth import auth as auth_blueprint
from .users import users as users_blueprint
from .async_sample_data import async_sample_data as async_sample_data_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(async_sample_data_blueprint)