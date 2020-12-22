from flask import Flask
from flask_apscheduler import APScheduler

from db.msg_log import MsgLogger
from views import *
from wx.admin import Admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.register_blueprint(root.mod, url_prefix='/')
    app.register_blueprint(cpdaliy.mod, url_prefix='/cpdaliy')
    app.register_blueprint(admin.mod, url_prefix='/wechat-admin')
    app.register_blueprint(bind.mod, url_prefix='/bing')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        app.admin = Admin()
        app.msg_logger = MsgLogger()

    return app
