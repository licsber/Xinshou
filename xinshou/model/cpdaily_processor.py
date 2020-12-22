from flask import current_app

from xinshou import wx
from .processor import Processor


class CpDailyProcessor(Processor):
    def _process_event(self, m: wx.receive.Event) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        exist = current_app.cpdaily.check_user(m.from_user_name)
        print(exist)
        if not exist:
            token = current_app.cpdaily.gen_token(m.from_user_name)
            content = f'<a href=\"https://wx.licsber.site/cpdaily/?token={token}\">完成认证后点我进入</a>'
        else:
            content = '此微信今天已成功绑定1个账号, 如需更多请找舍友或联系管理员.'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
