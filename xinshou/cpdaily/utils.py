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
DEFAULT_HEADER = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Content-Type': 'application/json;charset=UTF-8'
}


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
