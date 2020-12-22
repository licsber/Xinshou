from xinshou import wx


class Processor:
    def process(self, m: wx.receive.Msg) -> wx.reply.Msg:
        res = wx.reply.Msg()
        if isinstance(m, wx.receive.TextMsg):
            res = self._process_text(m)
        elif isinstance(m, wx.receive.ImageMsg):
            res = self._process_img(m)
        elif isinstance(m, wx.receive.VoiceMsg):
            res = self._process_voice(m)
        elif isinstance(m, wx.receive.Event):
            res = self._process_event(m)
        return res.send()

    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        return wx.reply.Msg()

    def _process_img(self, m: wx.receive.ImageMsg) -> wx.reply.Msg:
        return wx.reply.Msg()

    def _process_voice(self, m: wx.receive.VoiceMsg) -> wx.reply.Msg:
        return wx.reply.Msg()

    def _process_event(self, m: wx.receive.Event) -> wx.reply.Msg:
        return wx.reply.Msg()
