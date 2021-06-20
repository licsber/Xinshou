from flask import Flask
from flask_apscheduler import APScheduler

from db.location import LocationDB
from db.msg_log import MsgLogger
from db.session import SessionDB
from db.wisedu import WiseduDB
from views import root, admin, u
from wx.admin import Admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(root.mod, url_prefix='/')
    app.register_blueprint(admin.mod, url_prefix='/wechat-admin')
    app.register_blueprint(u.mod, url_prefix='/u')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        app.admin = Admin()
        app.msg_logger = MsgLogger()
        app.location = LocationDB()
        app.session = SessionDB()
        app.wisedu = WiseduDB()

    return app
