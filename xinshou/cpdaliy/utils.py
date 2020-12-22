import base64
import sys
from datetime import datetime, timedelta, timezone

import requests
import urllib3
from pyDes import des, CBC, PAD_PKCS5

urllib3.disable_warnings()

ADDRESS = '江苏省南京市江宁区学海路天印湖'
LON = '118.882366'
LAT = '31.928000'


def get_time_str():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")


def log(content):
    print(get_time_str() + ' ' + str(content))
    sys.stdout.flush()
    return get_time_str() + ' ' + str(content)


def des_encrypt(s, key='ST83=@XV'):
    key = key
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(s)
    return base64.b64encode(encrypt_str).decode()


def get_session(stu_no, passwd):
    params = {
        'login_url': 'http://authserver.njit.edu.cn/authserver/login?service=https%3A%2F%2Fnjit.campusphere.net%2Fportal%2Flogin',
        'needcaptcha_url': '',
        'captcha_url': '',
        'username': stu_no,
        'password': passwd
    }

    cookies = {}
    res = requests.post('http://shh.licsber.site:48090/wisedu-unified-login-api-v1.0/api/login', params, verify=False)
    cookieStr = str(res.json()['cookies'])
    if cookieStr == 'None':
        log(res.json())
        return None

    for line in cookieStr.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookies)
    return session


def fill_form(task):
    print(task)
    form = {}
    if task['isPhoto'] != 1:
        form['signPhotoUrl'] = ''
    if task['isNeedExtra'] == 1:
        extraFields = task['extraField']
        defaults = [
            {
                'title': '上午体温报告',
                'value': '36.1℃ - 36.5℃'
            },
            {
                'title': '下午体温报告',
                'value': '36.1℃ - 36.5℃'
            }
        ]
        extra_field_item_values = []
        for i in range(0, len(extraFields)):
            default = defaults[i]
            extraField = extraFields[i]
            if default['title'] != extraField['title']:
                return None
            extraFieldItems = extraField['extraFieldItems']
            for extraFieldItem in extraFieldItems:
                if extraFieldItem['content'] == default['value']:
                    extraFieldItemValue = {'extraFieldItemValue': default['value'],
                                           'extraFieldItemWid': extraFieldItem['wid']}
                    if extraFieldItem['isOtherItems'] == 1:
                        extraFieldItemValue = {'extraFieldItemValue': default['other'],
                                               'extraFieldItemWid': extraFieldItem['wid']}
                    extra_field_item_values.append(extraFieldItemValue)
        form['extraFieldItems'] = extra_field_item_values
    form['signInstanceWid'] = task['signInstanceWid']
    form['longitude'] = LON
    form['latitude'] = LAT
    form['isMalposition'] = task['isMalposition']
    form['abnormalReason'] = '在校'
    form['position'] = ADDRESS
    return form
