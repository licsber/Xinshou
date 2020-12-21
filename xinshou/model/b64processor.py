import base64

import wx
from .processor import Processor


class B64Processor(Processor):

    def _process_text(self, m: wx.receive.TextMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        content = f'Base64回音壁测试, 你刚说了: ' \
                  f'"{base64.b64encode(m.content.encode()).decode()}".'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
