import json
import uuid
from json import JSONDecodeError

from licsber.auth import get_wisedu_session
from licsber.utils import get_now_date

from .utils import *

HOST = 'njit.campusphere.net'

OLD_URLS = {
    'one_day': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/queryDailySginTasks',
    'detail': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/detailSignTaskInst',
    'submit': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/completeSignIn'
}

NEW_URLS = {
    'one_day': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay',
    'detail': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/detailSignInstance',
    'submit': f'https://{HOST}/wec-counselor-sign-apps/stu/sign/submitSign'
}

URLS = NEW_URLS


def sign_all(session, stu_no, loc=None, debug=False):
    session.post(
        url=URLS['one_day'],
        headers=DEFAULT_HEADER, data=json.dumps({}), verify=False)
    res = session.post(
        url=URLS['one_day'],
        headers=DEFAULT_HEADER, data=json.dumps({}), verify=False)
    try:
        all_task = res.json()['datas']['unSignedTasks']
    except JSONDecodeError:
        log(f"{stu_no}: 需要验证码")
        return ''

    if len(all_task) < 1:
        return '当前无签到任务.'

    if debug:
        print(all_task)

    latest_task = all_task[0]
    for i in all_task:
        if '体温' in i['taskName'] or '健康' in i['taskName']:
            latest_task = i
            break

    now_date = get_now_date()
    if now_date not in latest_task['rateSignDate']:
        return '已被签到.'

    params = {
        'signInstanceWid': latest_task['signInstanceWid'],
        'signWid': latest_task['signWid']
    }
    res = session.post(
        url=URLS['detail'],
        headers=DEFAULT_HEADER, data=json.dumps(params), verify=False)
    task = res.json()['datas']
    if debug:
        print(task)

    if loc:
        ADDRESS = loc['label']
        if not ADDRESS:
            ADDRESS = loc['poi']
            if not ADDRESS:
                ADDRESS = random_address()
        LON, LAT = random_position(longitude=float(loc['longitude']), latitude=float(loc['latitude']))
    else:
        ADDRESS = random_address()
        LON, LAT = random_position()

    form = {
        'signPhotoUrl': '',
        'signInstanceWid': task['signInstanceWid'],
        'longitude': LON,
        'latitude': LAT,
        'isMalposition': task['isMalposition'],
        'abnormalReason': '假期',
        'position': ADDRESS,
        'uaIsCpadaily': True
    }

    if task['isNeedExtra'] == 1:
        extra_fields = task['extraField']
        defaults = [
            {
                'title': '上午体温报告',
                'value': '36.1℃ - 36.5℃'
            },
            {
                'title': '下午体温报告',
                'value': '36.1℃ - 36.5℃'
            },
            {
                'title': '上午体温报告',
                'value': '36.1摄氏度～36.5摄氏度'
            },
            {
                'title': '同住人员是否有发热、咳嗽、干咳和腹泻等症状',
                'value': '无'
            },
            {
                'title': '你的当地健康码颜色是（请谨慎如实填写）（必填）',
                'value': '绿色'
            },
            {
                'title': '你的当地健康码颜色是（请谨慎如实填写）',
                'value': '绿色'
            },
            {
                'title': '你或你的同住人目前是否被医学隔离（必填）',
                'value': '否'
            },
            {
                'title': '近14天你或你的同住人是否有疫情中、高风险区域行程史 （必填）',
                'value': '否'
            },
            {
                'title': '你的健康状况（必填）',
                'value': '健康'
            },
            {
                'title': '你的体温情况（必填）',
                'value': '37.2℃及以下'
            },
        ]
        extra_field_item_values = []
        for i in extra_fields:
            for j in defaults:
                if j['title'] != i['title']:
                    continue
                for k in i['extraFieldItems']:
                    if k['content'] == j['value']:
                        extra_field_item_values.append({
                            'extraFieldItemValue': j['value'],
                            'extraFieldItemWid': k['wid']
                        })
        form['extraFieldItems'] = extra_field_item_values

    extension = {
        "model": "OnePlus 20+",
        "appVersion": "8.1.14",
        "systemVersion": "8.0",
        "userId": stu_no,
        "systemName": "android",
        "lon": LON,
        "lat": LAT,
        "deviceId": str(uuid.uuid1())
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; OPPO R11 Plus Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.12.4',
        'CpdailyStandAlone': '0',
        'extension': '1',
        'Cpdaily-Extension': des_encrypt(json.dumps(extension)),
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive'
    }
    res = session.post(url=URLS['submit'],
                       headers=headers, data=json.dumps(form), verify=False)
    msg = res.json()['message']
    if msg != 'SUCCESS':
        if msg == '任务未开始，扫码签到无效！':
            return '任务未开始'
        log(f'{stu_no}: {msg}')
        return ''
    return '正常签到.'


def sign_dorm(session, stu_no):
    session.post(
        url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/getStuAttendacesInOneDay',
        headers=DEFAULT_HEADER, data=json.dumps({}))
    res = session.post(
        url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/getStuAttendacesInOneDay',
        headers=DEFAULT_HEADER, data=json.dumps({}))
    if len(res.json()['datas']['unSignedTasks']) < 1:
        log('当前没有未签到任务')
        return True

    latest_task = res.json()['datas']['unSignedTasks'][0]
    task = {
        'signInstanceWid': latest_task['signInstanceWid'],
        'signWid': latest_task['signWid']
    }
    res = session.post(url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/detailSignInstance',
                       headers=DEFAULT_HEADER, data=json.dumps(task))
    task = res.json()['datas']

    ADDRESS = random_address()
    LON, LAT = random_position()

    extension = {
        "lon": LON,
        "model": "PCRT00",
        "appVersion": "8.0.8",
        "systemVersion": "4.4.4",
        "userId": stu_no,
        "systemName": "android",
        "lat": LAT,
        "deviceId": str(uuid.uuid1())
    }
    form = {
        'signInstanceWid': task['signInstanceWid'],
        'longitude': LON,
        'latitude': LAT,
        'isMalposition': task['isMalposition'],
        'abnormalReason': '在校',
        'signPhotoUrl': '',
        'position': ADDRESS,
        'qrUuid': '',
        'uaIsCpadaily': True
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 okhttp/3.8.1',
        'CpdailyStandAlone': '0',
        'extension': '1',
        'Cpdaily-Extension': des_encrypt(json.dumps(extension)),
        'Content-Type': 'application/json; charset=utf-8',
        'Host': HOST,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    res = session.post(
        url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/submitSign',
        headers=headers, data=json.dumps(form))
    msg = res.json()['message']
    return msg if msg == 'SUCCESS' else ''


def check_in(stu_no, passwd, dorm=False, loc=None, debug=False) -> bool:
    url = 'http://authserver.njit.edu.cn/authserver/login?service=https%3A%2F%2Fnjit.campusphere.net%2Fportal%2Flogin'
    s = get_wisedu_session(url, stu_no, passwd)
    if 'iPlanetDirectoryPro' not in s.cookies:
        try:
            s = old_get_session(stu_no, passwd)
        except Exception:
            s = None
    if s:
        if dorm:
            res = sign_dorm(s, stu_no)
        else:
            res = sign_all(s, stu_no, loc=loc, debug=debug)
        if res:
            log(f'{stu_no}: {res}')
            return True
    log(f'{stu_no}: 签到失败.')
    return False
