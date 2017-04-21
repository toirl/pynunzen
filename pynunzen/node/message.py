#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
from pynunzen.helpers import utcts

"""Communication between nodes is done by sending and receiving JSON
strings. As long as the message is handled by the server the message is
represented as a :class:Message instance."""


class MessageParseException(ValueError):
    pass


def encode_message(msg):
    """Will encode a :class:Message into a JSON string

    :msg: :class:Message
    :returns: JSON string

    """
    if not isinstance(msg, Message):
        raise ValueError("Message must be of type {}".format(type(Message)))
    try:
        return repr(msg)
    except:
        raise MessageParseException("Message can not be parsed")


def decode_message(json_msg):
    """Will decode a JSON string and return a :class:Message instance.
    Depending on the `mtype` attribute the method return eithe a
    :class:Request or :class:Response instance.

    :msg: JSON string
    :returns: :class:Message
    """
    try:
        msg_dict = json.loads(json_msg)
    except:
        raise MessageParseException("Message can not be parsed")

    data = msg_dict.get("data")
    mtype = msg_dict.get("mtype")
    if not mtype:
        raise MessageParseException("Missing 'mtype' in message")

    if mtype == "request":
        command = msg_dict.get("command")
        if not command:
            raise MessageParseException("Request is missing a command")
        msg = Request(command, data)
    else:
        msg = Response(data)
    return msg


class JSONSerializable(object):
    def __repr__(self):
        return json.dumps(self.__dict__)


class Message(JSONSerializable):

    def __init__(self, mtype, data):
        self.timestamp = utcts(datetime.datetime.utcnow())
        """Timestamp with """
        self.mtype = mtype
        """Type of the message. Can be either be `request` or
        `response`. This string is used while decoding the a JSON string
        into a :class:Message."""
        self.data = data
        """Payload of the message"""


class Request(Message):

    def __init__(self, command, data=None):
        Message.__init__(self, "request", data)
        self.command = command
        """Name of the command in the request"""


class Response(Message):

    def __init__(self, data, success=True):
        Message.__init__(self, "response", data)
        self.success = success
        """Flag to indicate that the node which sends the response has
        an error"""
