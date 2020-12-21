import requests

def refresh_access_token(appid, secret) -> str:
    requests.get()
    pass


if __name__ == '__main__':
    from config import *

    refresh_access_token(WX_APP_ID, WX_APP_SECRET)
