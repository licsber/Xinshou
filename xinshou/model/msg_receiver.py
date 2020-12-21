import wx

from .b64processor import B64Processor
from .magic_processor import MagicProcessor

text_map = {
    '我爱你': MagicProcessor(),
    'default': B64Processor()
}


def receive_msg(m: wx.receive.Msg) -> wx.reply.Msg:
    if isinstance(m, wx.receive.TextMsg) and m.content in text_map:
        processor = text_map[m.content]
    else:
        processor = text_map['default']
    return processor.process(m)
