import uuid

from bson import ObjectId
from flask import current_app
from licsber import get_mongo
from licsber.auth import get_wisedu_session
from licsber.mongo import get_latest_doc

LOGIN = 'http://authserver.njit.edu.cn/authserver/login?service=https%3A%2F%2Fnjit.campusphere.net%2Fportal%2Flogin'
LOGOUT = 'http://authserver.njit.edu.cn/authserver/logout?service=http://ehall.njit.edu.cn/new/index.html'


class WiseduDB:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._db = db['credits']
        self._log = db['credits_log']
        self.init_db()

    def init_db(self):
        self._db.create_index('oid')
        self._log.create_index('no')

    def get_filter(self, oid):
        return {
            'oid': oid,
            'retry': {
                '$eq': 0
            },
            'active': True,
        }

    def parse_uid_from_id(self, _id):
        s = str(_id)
        return (s[:8] + s[-2:]).upper()

    def add_account(self, oid, no, pwd):
        suc = self.check_account(no, pwd)
        if suc:
            doc = self._db.insert_one({
                'no': no,
                'pwd': pwd,
                'token': uuid.uuid4(),
                'active': True,
                'retry': 0,
                'level': 2,
                'credits': 10,
                'invitor': ObjectId('60cd66c6f0d2e36ad4fa3192'),
                'oid': oid,
            })
            return self.parse_uid_from_id(doc.inserted_id)

    def get_checkin_info(self, oid):
        f = self.get_filter(oid)
        doc = get_latest_doc(self._db, f, ['no'])
        if doc:
            no = doc['no']
            doc = self._log.find_one({'no': no})
            return doc['date'], doc['type']
        return None, None

    def get_credits(self, oid):
        f = self.get_filter(oid)
        doc = get_latest_doc(self._db, f, ['credits'])
        if doc:
            return doc['credits'], self.parse_uid_from_id(doc['_id'])
        return None, None

    def check_can_register(self, oid):
        f = self.get_filter(oid)
        doc = get_latest_doc(self._db, f, [])
        return not doc

    def check_account(self, no, pwd):
        s = get_wisedu_session(LOGIN, no, pwd)
        suc = len(s.cookies) != 2
        if suc:
            s.get(LOGOUT)
        return suc
