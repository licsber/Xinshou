from flask import Flask
from flask_apscheduler import APScheduler

from .db.auth import Auth
from .db.cpdaily import CpDaily
from .db.msg_log import MsgLogger
from .views import *
from .wx.admin import Admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(root.mod, url_prefix='/')
    app.register_blueprint(cpdaily.mod, url_prefix='/cpdaily')
    app.register_blueprint(admin.mod, url_prefix='/wechat-admin')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        app.admin = Admin()
        app.msg_logger = MsgLogger()
        app.cpdaily = CpDaily()
        app.auth = Auth()

    return app
