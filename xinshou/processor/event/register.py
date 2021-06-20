import uuid

from flask import current_app

from processor.processor import Processor
from wx import receive, reply


class RegisterProcessor(Processor):
    def get_keyword(self) -> str:
        return 'register'

    def _process_event(self, m: receive.Event) -> reply.Msg:
        can_register = current_app.wisedu.check_can_register(m.from_user_name)
        if can_register:
            token = uuid.uuid4()
            current_app.session.set(token, 'register_root', m.from_user_name, unique=True)
            content = '查看公众号最新文章'
            content += '\n点击页面广告后返回'
            content += f'\n<a href=\"https://wx.licsber.site/u?token={token}\">完成后戳我进入</a>'
        else:
            content = '已成功绑定 1 个账号\n如需更多请找舍友或联系管理员'
        return reply.TextMsg.reply(m, content)
