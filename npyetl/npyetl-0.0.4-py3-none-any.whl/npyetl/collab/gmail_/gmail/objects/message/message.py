from __future__ import annotations
from typing import (
    List,
    Dict,
    NamedTuple
)
import email
import base64
from ._base_message import BaseMessage
from .._base_object import _BaseObject


def make_message(**kwargs) -> BaseMessage:
    if 'payload' in kwargs:
        if 'body' in kwargs['payload']:
            return FullMessage(**kwargs)
        else:
            return MetadataMessage(**kwargs)
    elif 'raw' in kwargs:
        return RawMessage(**kwargs)
    else:
        return MinimalMessage(**kwargs)
    

class MessageWithHeaders(BaseMessage):
    
    def get_header(self, header: str) -> str:
        for header_data in self._payload.headers:
            if header_data['name'] == header:
                return header_data['value']
        return str()
    
    @property
    def from_(self) -> str:
        return self.get_header('From')
    
    @property
    def to(self) -> str:
        return self.get_header('To')
    
    @property
    def subject(self) -> str:
        return self.get_header('Subject')


class FullMessage(MessageWithHeaders):

    def __init__(self,
                 payload: Dict[str, object] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._payload = FullMessage.Payload(**payload)    

    @property
    def payload(self) -> FullMessage.Payload:
        return self._payload
    
    #@override(BaseMessage)
    @property
    def email_message(self) -> email.message.Message:
        """
        """
        msg_bytes = None
        #
        if 'data' in self._payload.body:
            msg_bytes = base64.urlsafe_b64decode(self._payload.body['data'].encode('utf-8'))
        elif self._payload.parts:
            part = FullMessage.get_part_by_mime_type(self._payload.parts)
            if part:
                msg_bytes = base64.urlsafe_b64decode(part['body']['data'].encode('utf-8'))
        #
        return email.message_from_bytes(msg_bytes) if msg_bytes else email.message.Message()
    
    @staticmethod
    def get_part_by_mime_type(parts: List[dict],
                              mime_type='text/plain'):
        for part in parts:
            if part['mimeType'] == mime_type:
                return part
            if part['mimeType'].startswith('multipart'):
                result = FullMessage.get_part_by_mime_type(part['parts'], mime_type)
                if result:
                    return result
        return dict()

    def to_string(self) -> str:
        for part in self.email_message.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    return part.get_payload(decode=True).decode('utf-8')
        return str()
    
    class Payload(NamedTuple):
        partId: str
        mimeType: str
        filename: str
        headers: List[Dict[str, str]]
        body: Dict[str, object] = None
        parts: List[Dict[str, object]] = None


class MetadataMessage(MessageWithHeaders):

    def __init__(self,
                 payload: Dict[str, object] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._payload = MetadataMessage.Payload(**payload)
    
    @property
    def payload(self) -> MetadataMessage.Payload:
        return self._payload
    
    class Payload(NamedTuple):
        mimeType: str
        headers: List[Dict[str, str]]


class RawMessage(BaseMessage):

    def __init__(self,
                 raw: str,
                 **kwargs):
        super().__init__(**kwargs)
        self._raw = raw

    #@override(BaseMessage)
    @property
    def email_message(self) -> email.message.Message:
        """
        """
        msg_bytes = base64.urlsafe_b64decode(self._raw.encode('utf-8'))
        return email.message_from_bytes(msg_bytes)

    def to_string(self) -> str:
        for part in self.email_message.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    return part.get_payload(decode=True).decode('utf-8')
        return str()
    
    
class MinimalMessage(BaseMessage):
    pass
