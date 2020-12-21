import hashlib

from flask import Blueprint
from flask import current_app
from flask import request
from flask import send_from_directory

mod = Blueprint('root', __name__)


@mod.route('/')
def root():
    if len(request.args) == 0:
        return 'Hello from Licsber.'

    # noinspection SpellCheckingInspection
    echo_str = request.args['echostr']
    nonce = request.args['nonce']
    signature = request.args['signature']
    timestamp = request.args['timestamp']

    h = [current_app.config['WX_TOKEN'], timestamp, nonce]
    h.sort()
    h = ''.join(h).encode()
    h = hashlib.sha1(h).hexdigest()
    return echo_str if h == signature else 'Fail.'


@mod.route('/favicon.ico')
def favicon():
    return send_from_directory('static', filename='favicon.ico')
