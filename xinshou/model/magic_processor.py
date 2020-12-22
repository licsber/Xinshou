from flask import current_app

from xinshou import wx
from .processor import Processor


class MagicProcessor(Processor):

    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = current_app.admin.get_access_token()
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
