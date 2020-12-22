import wx
from .cpdaily_processor import CpDailyProcessor
from .default_processor import DefaultProcessor
from .magic_processor import MagicProcessor
from .status_processor import StatusProcessor

msg_map = {
    '我爱你': MagicProcessor(),
    'default': DefaultProcessor()
}

event_map = {
    'status': StatusProcessor(),
    'cpdaily': CpDailyProcessor()
}


def receive_msg(m: wx.receive.Msg) -> wx.reply.Msg:
    if isinstance(m, wx.receive.TextMsg) and m.content in msg_map:
        processor = msg_map[m.content]
    elif isinstance(m, wx.receive.Event) and m.event_key in event_map:
        processor = event_map[m.event_key]
    else:
        processor = msg_map['default']
    return processor.process(m)
