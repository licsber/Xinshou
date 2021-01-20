from xinshou.weixin import *

WX_APP_ID = '微信id'
WX_APP_SECRET = '微信secret'
WX_TOKEN = '微信token'
WX_ENCODING_AES_KEY = '微信加密key'

MONGO_PASSWD_B64 = '数据库密码'
ADMIN_PASSWD = '管理后台密码'

SCHEDULER_API_ENABLED = True
JOBS = [
    {
        'id': 'refresh_access_token',
        'func': 'xinshou.wx.admin:refresh_access_token',
        'args': (
            API_REFRESH_ACCESS_TOKEN,
            MONGO_PASSWD_B64,
            WX_APP_ID,
            WX_APP_SECRET
        ),
        'trigger': 'interval',
        'seconds': 3000
    }
]
