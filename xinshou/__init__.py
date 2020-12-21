from flask import Flask

from views import licsber
from views import root


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.register_blueprint(root.mod)
    app.register_blueprint(licsber.mod)
    return app
