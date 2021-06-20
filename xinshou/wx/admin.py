import sys

from flask import current_app
from licsber import get_mongo
from licsber.utils import get_timestamp


class Admin:
    def __init__(self):
        self.db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self.admin = self.db['wx_admin']
        refresh_access_token(
            url=current_app.config['API_REFRESH_ACCESS_TOKEN'],
            passwd=current_app.config['MONGO_PASSWD_B64'],
            app_id=current_app.config['WX_APP_ID'],
            secret=current_app.config['WX_APP_SECRET']
        )
        self.token = self._get_type('access_token')

    def get_access_token(self) -> str:
        res = self.token
        if self.token['expire'] < get_timestamp() + 3630:
            res = self.token = self._get_type('access_token')
        return res['token']

    def _get_type(self, type):
        return self.admin.find_one({
            'type': {'$eq': type}
        })


def refresh_access_token(url, passwd, app_id, secret):
    admin = get_mongo(passwd)['wx_admin']
    access_token = admin.find_one({
        'type': {'$eq': 'access_token'}
    })

    if sys.platform == 'darwin':
        return

    if access_token and access_token['expire'] > get_timestamp() + 3600:
        print(f"当前token仍有效, {access_token['token']}.")
        return

    import requests
    import json

    param = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': secret
    }
    res = requests.get(url, params=param)

    if res.status_code == 200:
        res = res.content
        res = json.loads(res)
        if 'errcode' in res:
            print(f"token更新失败, {res['errmsg']}")
            return
        access_token = {
            'type': 'access_token',
            'token': res['access_token'],
            'expire': get_timestamp() + res['expires_in']
        }
        admin.replace_one(
            {'type': {'$eq': 'access_token'}},
            access_token,
            upsert=True
        )
        print(f"token更新成功, {access_token['token']}.")
