import hashlib

from flask import Blueprint
from flask import current_app
from flask import request
from flask import send_from_directory

from model.msg_receiver import receive_msg
from wx.receive import parse_xml

mod = Blueprint('root', __name__)


@mod.route('/', methods=['POST'])
def post():
    if current_app.debug:
        print(f"debug: {request.data}")

    req = parse_xml(request.data)
    current_app.msg_logger.log(req)
    if req.to_user_name == current_app.config['WX_USER_NAME']:
        return receive_msg(req)
    else:
        return None


def check_valid(request):
    # noinspection SpellCheckingInspection
    nonce = request.args['nonce']
    signature = request.args['signature']
    timestamp = request.args['timestamp']

    h = [current_app.config['WX_TOKEN'], timestamp, nonce]
    h.sort()
    h = ''.join(h).encode()
    h = hashlib.sha1(h).hexdigest()
    return h == signature


@mod.route('/', methods=['GET'])
def root():
    if not request.args:
        return 'Hello from Licsber.'

    echo_str = request.args['echostr']
    return echo_str if check_valid(request) else 'Fail.'


@mod.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
