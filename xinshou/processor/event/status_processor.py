from processor.processor import Processor
from wx import receive, reply


class StatusProcessor(Processor):
    def get_keyword(self) -> str:
        return 'status'

    def _process_event(self, m: receive.Event) -> reply.Msg:
        return reply.TextMsg.reply(m, '123')
