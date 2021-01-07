import requests
from bs4 import BeautifulSoup as bs4
from requests.compat import urljoin

from auth.utils import encrypt


def get_session(url, no, pwd):
    s = requests.session()
    res = s.get(url)
    data = {
        "lt": None,
        "dllt": None,
        "execution": None,
        "_eventId": None,
        "rmShown": None,
        'pwdDefaultEncryptSalt': None
    }

    res = bs4(res.content, 'html.parser')

    salt = res.find('input', id='pwdDefaultEncryptSalt')['value']
    login_url = res.find('form', id='casLoginForm')['action']
    login_url = urljoin(url, login_url)

    for i in res.find_all('input'):
        if 'name' in i.attrs and i['name'] in data:
            data[i['name']] = i['value']

    data['username'] = no
    data['password'] = encrypt(pwd, salt)

    s.post(login_url, data=data)
    return s
