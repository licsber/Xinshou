import datetime

from flask import current_app
from licsber import get_mongo


class SessionDB:
    def __init__(self, timeout=30 * 60):
        self.timeout = timeout
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._db = db['xinshou_session']
        self.init_db()

    def init_db(self):
        self._db.create_index('id')
        self._db.create_index('key')
        self._db.create_index('ctime', expireAfterSeconds=self.timeout)

    def set(self, idd: str, key: str, value, unique=False):
        if unique:
            self._db.delete_many({
                'id': idd,
                'key': key,
            })

        self._db.insert_one({
            'id': idd,
            'ctime': datetime.datetime.utcnow(),
            'key': key,
            'value': value,
        })

    def get(self, idd: str, key: str):
        doc = self._db.find_one_and_delete({
            'id': idd,
            'key': key,
        }, projection=['value'])
        if doc:
            return doc['value']
