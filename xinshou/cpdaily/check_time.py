import datetime
import time


def check_time() -> str:
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=-8)
    now = time.gmtime(now.timestamp())
    if 7 <= now.tm_hour <= 11:
        return '上午'
    elif 14 <= now.tm_hour <= 18:
        return '下午'
    # elif 21 <= now.tm_hour <= 23:
    #     return '查寝'
    return ''


if __name__ == '__main__':
    print(check_time())
