#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import hashlib


def utcts(dt):
    """Will return a UTC timestamp of the given datetime"""
    if dt.tzinfo is not None:
        raise ValueError("Datetime must be naiv and must not contain any tzinfo")
    return calendar.timegm(dt.utctimetuple())


def double_sha256(value):
    """Return a doubled sha256 hash of the given value.

    :returns: sha256 hash.

    """
    # Ensure value value is a string
    if value is None:
        value = ""
    elif not isinstance(value, str):
        value = str(value)

    h1 = hashlib.sha256()
    h2 = hashlib.sha256()
    h1.update(value.encode("utf-8"))
    h2.update(h1.hexdigest().encode("utf-8"))
    return h2.hexdigest()
