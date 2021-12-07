from flask import Flask, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from flask_talisman import Talisman

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
pagedown = PageDown()

CSP = {
    'default-src': [
        '\'self\'',
        "*.fontawesome.com"
    ],
    'script-src': ["\'self\'", "\'unsafe-inline\'", "kit.fontawesome.com", "cdn.jsdelivr.net", "ajax.googleapis.com", "cdnjs.cloudflare.com"],
    'style-src': ["\'self\'", "\'unsafe-inline\'", "cdn.jsdelivr.net", "*.fontawesome.com"],
    'img-src': ["\'self\'", "data:"]
}


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
    Talisman(app, content_security_policy=CSP, force_https=False)

    app.register_blueprint(users, url_prefix="/user")
    app.register_blueprint(gifts)

    login_manager.login_view = "users.login"

    return app

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("users.login") + "?next=" + request.path)
