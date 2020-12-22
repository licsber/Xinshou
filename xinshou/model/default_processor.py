import base64

from xinshou import wx
from .processor import Processor


class DefaultProcessor(Processor):

    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = f'Base64回音壁测试, 你刚说了: ' \
                  f'"{base64.b64encode(m.content.encode()).decode()}".'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res

    def _process_voice(self, m: wx.receive.VoiceMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = f'语音解析结果: {m.recognition}.'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
