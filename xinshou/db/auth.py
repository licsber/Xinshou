from flask import current_app
from licsber import get_mongo


class Auth:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._db = db['wx_auth']
        self.all = self._get_all()

    def get_all(self):
        return self.all

    def _get_all(self):
        res = []
        for i in self._db.find():
            res.append(i)
        return res
