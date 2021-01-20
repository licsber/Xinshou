from flask import current_app

from xinshou import wx
from .processor import Processor


class LocationMsgProcessor(Processor):
    def _process_location(self, m: wx.receive.LocationMsg) -> wx.reply.Msg:
        to_user = m.from_user_name
        from_user = m.to_user_name
        exist = current_app.cpdaily.check_user_added(to_user)
        if exist:
            content = '已记录，将在最迟一天内生效，该功能仍在公测，请注意观察。'
            content += '\n最好不要一天内多次更改位置，程序已知会引起未知行为。'
            content += '\n最好不要一天内多次更改位置，程序已知会引起未知行为。'
            content += '\n最好不要一天内多次更改位置，程序已知会引起未知行为。'
            content += f"\n当前位置理论上是: {m.label}."
        else:
            content = '还没绑定呢，改啥位置？'
        res = wx.reply.TextMsg(to_user, from_user, content)
        return res
