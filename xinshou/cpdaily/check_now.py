from licsber.utils import get_now_date

from .check_in import check_in
from .check_time import check_time


def check_now(l):
    now = check_time()
    l['mdate'] = get_now_date()
    if now and 'no' in l and 'pwd' in l:
        dorm = now == '查寝'
        if check_in(l['no'], l['pwd'], dorm=dorm):
            l['last'] = now
        else:
            l['retry'] += 1
    return l
