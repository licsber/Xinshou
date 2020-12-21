from flask import Flask
from flask_apscheduler import APScheduler

from views import licsber
from views import root
from wx.admin import Admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.register_blueprint(root.mod, url_prefix='/')
    app.register_blueprint(licsber.mod, url_prefix='/licsber')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        app.admin = Admin()

    return app
