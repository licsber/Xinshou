from xml.etree import ElementTree


class Msg(object):
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text

    def to_dict(self):
        return {
            'to': self.to_user_name,
            'from': self.from_user_name,
            'ctime': self.create_time,
            'type': self.msg_type
        }

    def __str__(self):
        return str(self.to_dict())


class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content = xml_data.find('Content').text
        self.msg_id = xml_data.find('MsgId').text

    def to_dict(self):
        d = super(TextMsg, self).to_dict()
        d['content'] = self.content
        d['id'] = self.msg_id
        return d

    def to_db(self, db):
        pass


class ImageMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text
        self.msg_id = xml_data.find('MsgId').text

    def to_dict(self):
        d = super(ImageMsg, self).to_dict()
        d['pic_url'] = self.pic_url
        d['media_id'] = self.media_id
        d['id'] = self.msg_id
        return d


class VoiceMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.media_id = xml_data.find('MediaId').text
        self.format = xml_data.find('Format').text
        self.recognition = xml_data.find('Recognition').text
        self.msg_id = xml_data.find('MsgId').text

    def to_dict(self):
        d = super(VoiceMsg, self).to_dict()
        d['format'] = self.format
        d['media_id'] = self.media_id
        d['recognition'] = self.recognition
        d['id'] = self.msg_id
        return d


class LocationMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.longitude = xml_data.find('Location_Y').text
        self.latitude = xml_data.find('Location_X').text
        self.scale = xml_data.find('Scale').text
        self.label = xml_data.find('Label').text

    def to_dict(self):
        d = super().to_dict()
        d['longitude'] = self.longitude
        d['latitude'] = self.latitude
        d['scale'] = self.scale
        d['label'] = self.label
        return d


class Event(Msg):
    def __init__(self, xml_data):
        super(Event, self).__init__(xml_data)
        self.event_key = xml_data.find('EventKey').text
        self.event = xml_data.find('Event').text

    def to_dict(self):
        d = super(Event, self).to_dict()
        d['key'] = self.event_key
        d['event'] = self.event
        return d


class ClickEvent(Event):
    def __init__(self, xml_data):
        super(ClickEvent, self).__init__(xml_data)


class ScanWaitEvent(Event):
    def __init__(self, xml_data):
        super(ScanWaitEvent, self).__init__(xml_data)
        self.scan_type = xml_data.find('ScanCodeInfo').find('ScanType').text
        self.scan_result = xml_data.find('ScanCodeInfo').find('ScanResult').text

    def to_dict(self):
        d = super().to_dict()
        d['scan_type'] = self.scan_type
        d['scan_result'] = self.scan_result
        return d


class LocationEvent(Event):
    def __init__(self, xml_data):
        super(LocationEvent, self).__init__(xml_data)
        self.longitude = xml_data.find('SendLocationInfo').find('Location_Y').text
        self.latitude = xml_data.find('SendLocationInfo').find('Location_X').text
        self.scale = xml_data.find('SendLocationInfo').find('Scale').text
        self.label = xml_data.find('SendLocationInfo').find('Label').text
        self.poi = xml_data.find('SendLocationInfo').find('Poiname').text

    def to_dict(self):
        d = super().to_dict()
        d['longitude'] = self.longitude
        d['latitude'] = self.latitude
        d['scale'] = self.scale
        d['label'] = self.label
        d['poi'] = self.poi
        return d


event_map = {
    'CLICK': ClickEvent,
    'scancode_waitmsg': ScanWaitEvent,
    'location_select': LocationEvent
}


def parse_event(xml_data):
    event = xml_data.find('Event').text
    res = Event
    if event in event_map:
        res = event_map[event]
    return res(xml_data)


xml_map = {
    'text': TextMsg,
    'image': ImageMsg,
    'voice': VoiceMsg,
    'location': LocationMsg,
    'event': parse_event
}


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xml_data = ElementTree.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    res = Msg
    if msg_type in xml_map:
        res = xml_map[msg_type]
    return res(xml_data)
