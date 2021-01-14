from bson.objectid import ObjectId
from flask import current_app
from licsber import get_mongo
from licsber.auth import get_wisedu_session
from licsber.utils import get_now_date
from licsber.utils import get_timestamp

from xinshou import wx
from xinshou.cpdaily import check_now


class CpDaily:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._log = db['cp_daily_log']
        self._token = db['cp_daily_token']
        self._work = db['cp_daily']
        self._loc = db['cp_daily_location']

    def gen_token(self, open_id):
        self._token.delete_many({
            'id': open_id
        })
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
            'cdate': get_now_date(),
            'ctime': get_timestamp(),
            'retry': 0
        }
        self._log.insert_one(l)

        url = 'http://authserver.njit.edu.cn/authserver/login?service=https%3A%2F%2Fnjit.campusphere.net%2Fportal%2Flogin'
        s = get_wisedu_session(url, stu_no, passwd)
        if s:
            l = check_now(l)
            self._work.insert_one(l)
        return s is not None

    def check_user_added(self, open_id):
        return self._work.find_one(
            {'id': open_id}
        )

    def get_user_status(self, open_id):
        res = '您尚未成功认证/登录, 请认证后重试.'
        l = self._work.find_one({
            'id': open_id
        })
        if l:
            res = '尚未发生第一次签到活动.'
            if 'mdate' in l:
                res = f"最近一次{l['mdate']}, 尚未发生签到."
            if 'last' in l:
                res = f"最近一次{l['mdate']}, 类型{l['last']}."
        return res

    def remember_location(self, event: wx.receive.LocationEvent):
        l = {
            'id': event.from_user_name,
            'ctime': get_timestamp(),
            'cdate': get_now_date(),
            'longitude': event.longitude,
            'latitude': event.latitude,
            'scale': event.scale,
            'label': event.label,
            'poi': event.poi
        }
        self._loc.insert_one(l)
