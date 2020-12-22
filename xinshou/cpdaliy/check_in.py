import json
import uuid

from .utils import *

HOST = 'njit.campusphere.net'


def get_detail_task(session, params):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    res = session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/detailSignTaskInst',
        headers=headers, data=json.dumps(params), verify=False)
    data = res.json()['datas']
    return data


def submit_form(session, form, stu_no):
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
    return res.json()['message']


def sign_all(session, stu_no):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/queryDailySginTasks',
        headers=headers, data=json.dumps({}), verify=False)
    res = session.post(
        url=f'https://{HOST}/wec-counselor-sign-apps/stu/sign/queryDailySginTasks',
        headers=headers, data=json.dumps({}), verify=False)
    if len(res.json()['datas']['unSignedTasks']) < 1:
        return True

    # log(res.json())
    status = []
    for i in range(0, len(res.json()['datas']['unSignedTasks'])):
        latest_task = res.json()['datas']['unSignedTasks'][i]
        params = {
            'signInstanceWid': latest_task['signInstanceWid'],
            'signWid': latest_task['signWid']
        }
        task = get_detail_task(session, params)
        form = fill_form(task)
        if form:
            status.append(submit_form(session, form, stu_no))
    return status


def sign_dorm(session, stu_no):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    session.post(
        url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/getStuAttendacesInOneDay',
        headers=headers, data=json.dumps({}))
    res = session.post(
        url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/getStuAttendacesInOneDay',
        headers=headers, data=json.dumps({}))
    if len(res.json()['datas']['unSignedTasks']) < 1:
        log('当前没有未签到任务')
        return True

    latestTask = res.json()['datas']['unSignedTasks'][0]
    task = {
        'signInstanceWid': latestTask['signInstanceWid'],
        'signWid': latestTask['signWid']
    }
    res = session.post(url=f'https://{HOST}/wec-counselor-attendance-apps/student/attendance/detailSignInstance',
                       headers=headers, data=json.dumps(task))
    task = res.json()['datas']

    form = {}
    form['signInstanceWid'] = task['signInstanceWid']
    form['longitude'] = LON
    form['latitude'] = LAT
    form['isMalposition'] = task['isMalposition']
    form['abnormalReason'] = '在校'
    form['signPhotoUrl'] = ''
    form['position'] = ADDRESS
    form['qrUuid'] = ''
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
    message = res.json()['message']
    return message


def check_in(stu_no, passwd, dorm=False) -> bool:
    s = get_session(stu_no, passwd)
    if s:
        if dorm:
            res = sign_dorm(s, stu_no)
        else:
            res = sign_all(s, stu_no)
        log(res)
        return True
    return False
