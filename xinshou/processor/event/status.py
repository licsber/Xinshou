from flask import current_app

from processor.processor import Processor
from wx import receive, reply


class StatusProcessor(Processor):
    def get_keyword(self) -> str:
        return 'status'

    def _process_event(self, m: receive.Event) -> reply.Msg:
        oid = m.from_user_name
        content = ''

        credits, uid = current_app.wisedu.get_credits(oid)
        if credits:
            content += f"UID: {uid}"
            content += f"\nMana: {credits}"
            date, type_ = current_app.wisedu.get_checkin_info(oid)
            if date:
                content += f"\n最近: {date} {type_}"
            else:
                content += '\n最近: 未发生签到'
        else:
            content += 'UID: 尚未绑定或密码错误\nMana: 0'

        if loc := current_app.location.get(oid):
            content += f"\n位置: 「{loc}」"
        else:
            content += '\n位置: 「默认」'

        return reply.TextMsg.reply(m, content)
