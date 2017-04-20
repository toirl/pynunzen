#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from pynunzen.helpers import utcts


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
    try:
        msg_dict = json.loads(json_msg)
        if msg_dict["mtype"] == "request":
            msg = Request(msg_dict["command"], msg_dict["data"])
        else:
            msg = Response(msg_dict["data"])
        return msg
    except:
        raise MessageParseException("Message can not be parsed")


class JSONSerializable(object):
    def __repr__(self):
        return json.dumps(self.__dict__)


class Message(JSONSerializable):

    """Docstring for Message. """

    def __init__(self, mtype, data):
        self.timestamp = utcts(datetime.datetime.utcnow())
        self.mtype = mtype
        self.data = data


class Request(Message):

    """Docstring for Request. """

    def __init__(self, command, data=None):
        """TODO: to be defined1. """
        Message.__init__(self, "request", data)
        self.command = command


class Response(Message):

    """Docstring for Response. """

    def __init__(self, data, success=True):
        """TODO: to be defined1.

        :data: TODO
        :success: TODO

        """
        Message.__init__(self, "response", data)
        self.success = success
