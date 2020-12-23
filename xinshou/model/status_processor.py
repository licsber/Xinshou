from flask import current_app

from xinshou import wx
from .processor import Processor


class StatusProcessor(Processor):
    def _process_event(self, m: wx.receive.Event) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = current_app.cpdaily.get_user_status(m.from_user_name)
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
