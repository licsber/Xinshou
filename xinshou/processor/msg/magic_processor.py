from wx import receive, reply

from xinshou.processor.processor import Processor


class MagicProcessor(Processor):
    def get_keyword(self) -> str:
        return '我爱你'

    def _process_text(self, m: receive.TextMsg) -> reply.Msg:
        return reply.TextMsg.reply(m, '宝贝, 我也爱你.')
