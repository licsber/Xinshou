from flask import current_app

from xinshou import wx
from .processor import Processor


class CpDailyProcessor(Processor):
    def _process_event(self, m: wx.receive.Event) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        exist = current_app.cpdaily.check_user_added(m.from_user_name)
        if not exist:
            token = current_app.cpdaily.gen_token(m.from_user_name)
            content = f'<a href=\"https://wx.licsber.site/cpdaily/?token={token}\">' \
                      f'进公众号文章点下底部广告后戳我进入</a>'
        else:
            content = '此微信已成功绑定1个账号, 如需更多请找舍友或联系管理员.'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
