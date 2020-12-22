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
                    "name": "首次人脸认证",
                    "type": "pic_sysphoto",
                    "key": "bind"
                },
                {
                    "name": "扫码报名内测",
                    "type": "scancode_waitmsg",
                    "key": "scan"
                },
                {
                    "name": "今日校园签到",
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
                    "name": "联系管理",
                    "type": "view",
                    "url": "https://github.com/licsber"
                }
            ]
        }
    ]
}
'''
