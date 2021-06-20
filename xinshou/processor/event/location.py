from flask import current_app

from processor.processor import Processor
from wx import receive, reply


class LocationProcessor(Processor):
    def get_keyword(self) -> str:
        return 'location'

    def _process_event(self, m: receive.Event) -> reply.Msg:
        current_app.location.set(m)
        return reply.Msg()
