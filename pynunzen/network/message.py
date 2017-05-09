#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
from pynunzen.helpers import utcts, double_sha256

"""Messages are a containers for messages set in the Pynunzen network.
When sending a message it is encdoded into a JSON string.
"""


class MessageParseException(ValueError):
    pass


class MessageIntegrityException(ValueError):
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
        checksum = msg_dict["checksum"]
        data = msg_dict["data"]
    except:
        raise MessageParseException("Message can not be parsed")

    if double_sha256(data) != checksum:
        raise MessageIntegrityException("Data does not match checksum!")

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
    """A Message is a container for messages sent within the P2P network."""

    def __init__(self, mtype, data):
        self.timestamp = utcts(datetime.datetime.utcnow())
        """Timestamp with """
        self.mtype = mtype
        """Type of the message. Can be either be `request` or
        `response`. This string is used while decoding the a JSON string
        into a :class:Message."""
        self.data = data
        """Payload of the message"""
        self.checksum = double_sha256(data)


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
