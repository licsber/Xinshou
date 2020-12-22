from bson.objectid import ObjectId
from flask import current_app
from licsber import get_mongo
from licsber.utils import get_now_date

from cpdaliy import check_in
from cpdaliy import get_session


class CpDaily:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._log = db['cp_daily_log']
        self._token = db['cp_daily_token']
        self._work = db['cp_daily']

    def gen_token(self, open_id):
        r = self._token.insert_one({
            'id': open_id
        })
        return r.inserted_id

    def take_token(self, token):
        r = self._token.find_one_and_delete({
            '_id': ObjectId(token)
        })
        return r['id'] if r else None

    def add_user(self, stu_no, passwd, open_id):
        l = {
            'id': open_id,
            'no': stu_no,
            'pwd': passwd,
            'ctime': get_now_date()
        }
        self._log.insert_one(l)

        s = get_session(stu_no, passwd)
        if s:
            self._work.insert_one(l)
            check_in(stu_no, passwd, dorm=True)
        return s is not None

    def check_user(self, open_id):
        return self._work.find_one(
            {'id': open_id}
        )
