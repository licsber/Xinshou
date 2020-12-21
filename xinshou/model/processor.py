import wx


class Processor:
    def process(self, m: wx.receive.Msg) -> wx.reply.Msg:
        res = wx.reply.Msg()
        if isinstance(m, wx.receive.TextMsg):
            res = self._process_text(m)
        elif isinstance(m, wx.receive.ImageMsg):
            res = self._process_img(m)
        return res.send()

    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        return wx.reply.Msg()

    def _process_img(self, m: wx.receive.ImageMsg) -> wx.reply.Msg:
        return wx.reply.Msg()
