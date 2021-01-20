from xinshou import wx
from .processor import Processor


class MagicProcessor(Processor):
    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = '我也爱你'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
