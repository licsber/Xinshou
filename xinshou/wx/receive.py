from xml.etree import ElementTree


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xml_data = ElementTree.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'image':
        return ImageMsg(xml_data)
    else:
        return None


class Msg(object):
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text

    def to_dict(self):
        return {
            'to': self.to_user_name,
            'from': self.from_user_name,
            'ctime': self.create_time,
            'type': self.msg_type,
            'id': self.msg_id
        }

    def __str__(self):
        return str(self.to_dict())


class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content = xml_data.find('Content').text.encode("utf-8")

    def to_dict(self):
        d = super(TextMsg, self).to_dict()
        d['content'] = self.content.decode()
        return d

    def to_db(self, db):
        pass


class ImageMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text

    def to_dict(self):
        d = super(ImageMsg, self).to_dict()
        d['pic_url'] = self.pic_url
        d['media_id'] = self.media_id
        return d
