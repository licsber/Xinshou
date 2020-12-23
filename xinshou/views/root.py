import hashlib

from flask import Blueprint
from flask import current_app
from flask import request
from flask import send_from_directory

from xinshou.model import receive_msg
from xinshou.wx import parse_xml

mod = Blueprint('root', __name__)


@mod.route('/', methods=['POST'])
def post():
    if current_app.debug:
        print(request.data)
    req = parse_xml(request.data)
    current_app.msg_logger.log(req)
    return receive_msg(req)


@mod.route('/', methods=['GET'])
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
