from licsber import get_mongo
from licsber.utils import get_timestamp

from config import *


def gen_access_token() -> (str, int):
    return '123', 7200

def get_access_token() -> str:

    return


if __name__ == '__main__':
    db = get_mongo(MONGO_PASSWD_B64)
    c = db['wx_admin']
    c.create_index('type')
    access_token = c.find_one({
        'type': {'$eq': 'access_token'}
    })
    if not access_token:
        token, expire = gen_access_token()
        now = get_timestamp()
        c.insert_one({
            'type': 'access_token',
            'token': token,
            'expire': expire + get_timestamp()
        })
    if access_token['expire'] > get_timestamp():
        print(access_token)
