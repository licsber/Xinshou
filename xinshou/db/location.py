from flask import current_app
from licsber import get_mongo
from licsber.utils import get_timestamp, get_now_date

from wx.receive import LocationEvent


class LocationDB:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._db = db['xinshou_location']
        self.clean()

    def clean(self):
        self._db.delete_many({
            'label': None
        })
        self._db.delete_many({
            'poi': None
        })
        unique = set()
        for i in self._db.find(projection=['id', 'poi', 'label']):
            u = i['id'], i['poi'], i['label']
            if u not in unique:
                unique.add(u)
            else:
                self._db.delete_one(i)

    def set(self, event: LocationEvent):
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
        self._db.insert_one(l)

    def get(self, oid):
        loc = list(self._db.find({
            'id': oid
        }).sort([
            ('_id', -1)
        ]).limit(1))
        if loc:
            loc = loc[0]
            if label := loc['label']:
                return label
            else:
                return loc['poi']
