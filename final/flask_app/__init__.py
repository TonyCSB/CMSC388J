from flask import Flask, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pagedown import PageDown
from flaskext.markdown import Markdown

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
pagedown = PageDown()


from .users.routes import users
from .gifts.routes import gifts


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    pagedown.init_app(app)
    Markdown(app)

    app.register_blueprint(users, url_prefix="/user")
    app.register_blueprint(gifts)

    login_manager.login_view = "users.login"

    return app

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("users.login") + "?next=" + request.path)
