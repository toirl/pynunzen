#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_message
----------------------------------

Tests for `message` module.
"""


import pytest
from pynunzen.node.message import (
    MessageParseException,
    Request, Response,
    encode_message, decode_message
)


@pytest.fixture
def request():
    return Request("ping")


@pytest.fixture
def response():
    return Response("Foooo")


def test_decode_broken_json():
    with pytest.raises(MessageParseException):
        decode_message('{"key": "isbroken}')


def test_decode_message_no_json():
    with pytest.raises(MessageParseException):
        decode_message("Foo")


def test_decode_message_missing_mtype():
    with pytest.raises(MessageParseException):
        decode_message('{"command": "Foo", "data": "Bar"}')


def test_decode_message_missing_command():
    with pytest.raises(MessageParseException):
        decode_message('{"mtype": "request", "data": "Bar"}')


def test_decode_message():
    msg = decode_message('{"command": "Foo", "data": "Bar", "mtype": "request"}')
    assert msg.mtype == "request"
    assert msg.command == "Foo"
    assert msg.data == "Bar"


def test_encode_decode_request(request):
    json_message = encode_message(request)
    msg = decode_message(json_message)
    assert msg.mtype == "request"
    assert msg.command == "ping"


def test_encode_non_message():
    with pytest.raises(ValueError):
        encode_message({"key": "value"})


def test_encode_message_with_nonserializabale_date(request):
    import datetime
    request.fail = datetime.datetime.now()
    with pytest.raises(MessageParseException):
        encode_message(request)


def test_encode_decode_response(response):
    json_message = encode_message(response)
    msg = decode_message(json_message)
    assert msg.mtype == "response"
    assert msg.data == "Foooo"
    assert msg.success is True
