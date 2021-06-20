API_ROOT = 'https://api.weixin.qq.com'

API_REFRESH_ACCESS_TOKEN = API_ROOT + '/cgi-bin/token'

API_MENU_DELETE = API_ROOT + '/cgi-bin/menu/delete'
API_MENU_INFO = API_ROOT + '/cgi-bin/get_current_selfmenu_info'
API_MENU_CREATE = API_ROOT + '/cgi-bin/menu/create'

API_USER_INFO = API_ROOT + '/cgi-bin/user/info'

DEFAULT_MENU = '''
{
    "button": [
        {
            "name": "功能设置",
            "sub_button": [
                {
                    "name": "校园账号绑定",
                    "type": "click",
                    "key": "register"
                },
                {
                    "name": "位置信息选择",
                    "type": "location_select",
                    "key": "location"
                },
                {
                    "name": "领取每日Mana",
                    "type": "click",
                    "key": "checkin"
                }
            ]
        },
        {
            "name": "信息获取",
            "type": "click",
            "key": "status"
        },
        {
            "name": "服务支持",
            "sub_button": [
                {
                    "name": "加入我们",
                    "type": "view",
                    "url": "https://www.yuque.com/njit"
                },
                {
                    "name": "个人博客",
                    "type": "view",
                    "url": "https://www.cnblogs.com/licsber/"
                },
                {
                    "name": "开源地址",
                    "type": "view",
                    "url": "https://github.com/licsber"
                }
            ]
        }
    ]
}
'''
