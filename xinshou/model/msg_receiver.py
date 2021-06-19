from processor.default_processor import DefaultProcessor
from utils.mod_loader import ModLoader
from wx import receive, reply

mod_loader = ModLoader()

msg_map = mod_loader.load_mods('xinshou/processor/msg/')
event_map = mod_loader.load_mods('xinshou/processor/event/')
default = DefaultProcessor()


def receive_msg(m: receive.Msg) -> reply.Msg:
    processor = default
    if isinstance(m, receive.TextMsg) and m.content in msg_map:
        processor = msg_map[m.content]
    elif isinstance(m, receive.LocationMsg):
        processor = msg_map['location']
    elif isinstance(m, receive.Event) and m.event_key in event_map:
        processor = event_map[m.event_key]
    return processor.process(m)
