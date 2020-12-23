import json
import uuid

from licsber.utils import get_now_date

from .utils import *

HOST = 'njit.campusphere.net'


def sign_all(session, stu_no):
    session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/queryDailySginTasks',
        headers=DEFAULT_HEADER, data=json.dumps({}), verify=False)
    res = session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/queryDailySginTasks',
        headers=DEFAULT_HEADER, data=json.dumps({}), verify=False)
    if len(res.json()['datas']['unSignedTasks']) < 1:
        return '当前无签到任务.'

    latest_task = res.json()['datas']['unSignedTasks'][0]
    now_date = get_now_date()
    if now_date not in latest_task['rateSignDate']:
        return '已被签到.'

    params = {
        'signInstanceWid': latest_task['signInstanceWid'],
        'signWid': latest_task['signWid']
    }
    res = session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/detailSignTaskInst',
        headers=DEFAULT_HEADER, data=json.dumps(params), verify=False)
    task = res.json()['datas']

    form = {
        'signPhotoUrl': '',
        'signInstanceWid': task['signInstanceWid'],
        'longitude': LON,
        'latitude': LAT,
        'isMalposition': task['isMalposition'],
        'abnormalReason': '在校',
        'position': ADDRESS
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
            }
        ]
        extra_field_item_values = []
        for i in range(0, len(extra_fields)):
            default = defaults[i]
            extra_field = extra_fields[i]
            if default['title'] != extra_field['title']:
                continue
            extraFieldItems = extra_field['extraFieldItems']
            for extraFieldItem in extraFieldItems:
                if extraFieldItem['content'] == default['value']:
                    extraFieldItemValue = {'extraFieldItemValue': default['value'],
                                           'extraFieldItemWid': extraFieldItem['wid']}
                    if extraFieldItem['isOtherItems'] == 1:
                        extraFieldItemValue = {'extraFieldItemValue': default['other'],
                                               'extraFieldItemWid': extraFieldItem['wid']}
                    extra_field_item_values.append(extraFieldItemValue)
        form['extraFieldItems'] = extra_field_item_values

    extension = {
        "model": "China Plus Max S",
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
    res = session.post(url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/completeSignIn',
                       headers=headers, data=json.dumps(form), verify=False)
    msg = res.json()['message']
    return msg if msg == 'SUCCESS' else ''


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
        'qrUuid': ''
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


def check_in(stu_no, passwd, dorm=False) -> bool:
    s = get_session(stu_no, passwd)
    if s:
        if dorm:
            res = sign_dorm(s, stu_no)
        else:
            res = sign_all(s, stu_no)
        if res:
            log(f'{stu_no}: {res}')
            return True
    log(f'{stu_no}: 签到失败.')
    return False
