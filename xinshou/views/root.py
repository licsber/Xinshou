import base64
import hashlib

from flask import Blueprint
from flask import current_app
from flask import request
from flask import send_from_directory

import wx

mod = Blueprint('root', __name__)


@mod.route('/', methods=['POST'])
def post():
    req = wx.receive.parse_xml(request.data)
    res = wx.reply.Msg()

    if isinstance(req, wx.receive.TextMsg):
        to_user = req.from_user_name
        from_user = req.to_user_name
        content = f'Base64回音壁测试, 你刚说了: "{base64.b64encode(req.content).decode()}".'
        res = wx.reply.TextMsg(to_user, from_user, content)

    return res.send()


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
