from xinshou import wx
from .cpdaily_processor import CpDailyProcessor
from .default_processor import DefaultProcessor
from .location_msg_processor import LocationMsgProcessor
from .location_processor import LocationProcessor
from .magic_processor import MagicProcessor
from .status_processor import StatusProcessor

msg_map = {
    '我爱你': MagicProcessor(),
    'default': DefaultProcessor(),
    'location': LocationMsgProcessor()
}

event_map = {
    'status': StatusProcessor(),
    'cpdaily': CpDailyProcessor(),
    'location': LocationProcessor()
}


def receive_msg(m: wx.receive.Msg) -> wx.reply.Msg:
    if isinstance(m, wx.receive.TextMsg) and m.content in msg_map:
        processor = msg_map[m.content]
    elif isinstance(m, wx.receive.LocationMsg):
        processor = msg_map['location']
    elif isinstance(m, wx.receive.Event) and m.event_key in event_map:
        processor = event_map[m.event_key]
    else:
        processor = msg_map['default']
    return processor.process(m)
