from flask import current_app

from xinshou import wx
from .processor import Processor


class LocationProcessor(Processor):
    def _process_event(self, m: wx.receive.Event) -> wx.reply.Msg:
        current_app.cpdaily.remember_location(m)
        return wx.reply.Msg()
