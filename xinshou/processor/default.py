import base64

from wx import receive, reply
from .processor import Processor


class DefaultProcessor(Processor):
    def _process_img(self, m: receive.ImageMsg) -> reply.Msg:
        return super()._process_img(m)

    def _process_text(self, m: receive.TextMsg) -> reply.Msg:
        content = f'Base64回音壁测试, 你刚说了: ' \
                  f'"{base64.b64encode(m.content.encode()).decode()}".'
        return reply.TextMsg.reply(m, content)

    def _process_voice(self, m: receive.VoiceMsg) -> reply.Msg:
        content = f'语音解析结果: {m.recognition}.'
        return reply.TextMsg.reply(m, content)
