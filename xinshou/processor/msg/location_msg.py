from processor.processor import Processor
from wx import receive, reply


class LocationMsgProcessor(Processor):
    def get_keyword(self) -> str:
        return 'location'

    def _process_location(self, m: receive.LocationMsg) -> reply.Msg:
        content = f'已记录位置"{m.label}".'
        content += '\n最好不要一天内多次更改位置.'
        return reply.TextMsg.reply(m, content)
