from flask import Blueprint
from flask import current_app

from licsber import get_mongo

mod = Blueprint('licsber', __name__)


@mod.route('/')
def root():
    m = get_mongo(current_app.config['MONGO_PASSWD_B64'])
    print(m)
    return '123213'
