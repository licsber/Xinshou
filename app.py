import hashlib

from flask import Flask
from flask import request

from config import *

app = Flask(__name__)


@app.route('/')
def root():
    if len(request.args) == 0:
        return 'Hello from Licsber.'

    # noinspection SpellCheckingInspection
    echo_str = request.args['echostr']
    nonce = request.args['nonce']
    signature = request.args['signature']
    timestamp = request.args['timestamp']

    h = [WX_TOKEN, timestamp, nonce]
    h.sort()
    h = ''.join(h)
    h = hashlib.sha1(h).hexdigest()
    return echo_str if h == signature else 'Fail.'


if __name__ == '__main__':
    app.run(port=30443)
