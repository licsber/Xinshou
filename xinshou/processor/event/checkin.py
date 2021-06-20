import uuid

from flask import current_app

from processor.processor import Processor
from wx import receive, reply


class CheckinProcessor(Processor):
    def get_keyword(self) -> str:
        return 'checkin'

    def _process_event(self, m: receive.Event) -> reply.Msg:
        can_register = current_app.wisedu.check_can_register(m.from_user_name)
        if can_register:
            content = '尚未绑定账号\n请先点击「校园账号绑定」'
        else:
            token = uuid.uuid4()
            credits, uid = current_app.wisedu.get_credits(m.from_user_name)
            current_app.session.set(token, 'checkin_root', uid, unique=True)
            content = '为防止签到无人看管期间\n人身出现意外事故\n现在每隔一段时间需要获取Mana\nMana消耗完便会暂停'
            content += f'\n<a href=\"https://wx.licsber.site/u/checkin?token={token}\">点我领取Mana</a>'
            content += f"\n当前账户剩余Mana: {credits}"
        return reply.TextMsg.reply(m, content)
