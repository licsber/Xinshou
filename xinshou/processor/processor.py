import abc

from wx import receive, reply


class Processor:
    @abc.abstractmethod
    def get_keyword(self) -> str:
        pass

    def process(self, m: receive.Msg) -> reply.Msg:
        res = reply.Msg()
        if isinstance(m, receive.TextMsg):
            res = self._process_text(m)
        elif isinstance(m, receive.ImageMsg):
            res = self._process_img(m)
        elif isinstance(m, receive.VoiceMsg):
            res = self._process_voice(m)
        elif isinstance(m, receive.LocationMsg):
            res = self._process_location(m)
        elif isinstance(m, receive.Event):
            res = self._process_event(m)
        return res.send()

    def _process_text(self, m: receive.TextMsg) -> reply.Msg:
        return reply.Msg()

    def _process_img(self, m: receive.ImageMsg) -> reply.Msg:
        return reply.Msg()

    def _process_voice(self, m: receive.VoiceMsg) -> reply.Msg:
        return reply.Msg()

    def _process_location(self, m: receive.LocationMsg) -> reply.Msg:
        return reply.Msg()

    def _process_event(self, m: receive.Event) -> reply.Msg:
        return reply.Msg()
