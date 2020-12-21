from licsber.utils import get_timestamp


class Msg(object):
    def __init__(self):
        self.d = {}

    def send(self):
        return "success"

    def __str__(self):
        return str(self.d)


class TextMsg(Msg):
    def __init__(self, to_user_name, from_user_name, content):
        super().__init__()
        self.d.update({
            'ToUserName': to_user_name,
            'FromUserName': from_user_name,
            'CreateTime': get_timestamp(),
            'Content': content
        })

    def send(self):
        xml_form = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return xml_form.format(**self.d)


class ImageMsg(Msg):
    def __init__(self, to_user_name, from_user_name, media_id):
        super().__init__()
        self.d.update({
            'ToUserName': to_user_name,
            'FromUserName': from_user_name,
            'CreateTime': get_timestamp(),
            'MediaId': media_id
        })

    def send(self):
        xml_form = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        return xml_form.format(**self.d)
