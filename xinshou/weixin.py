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
                    "name": "账号注册",
                    "type": "click",
                    "key": "register"
                },
                {
                    "name": "位置信息选择",
                    "type": "location_select",
                    "key": "location"
                },
                {
                    "name": "校园验证获取",
                    "type": "click",
                    "key": "cpdaily"
                }
            ]
        },
        {
            "name": "状态获取",
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
                    "name": "联系管理",
                    "type": "view",
                    "url": "https://github.com/licsber"
                }
            ]
        }
    ]
}
'''
