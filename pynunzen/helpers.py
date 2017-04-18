#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar


def utcts(dt):
    """Will return a UTC timestamp of the given datetime"""
    if dt.tzinfo is not None:
        raise ValueError("Datetime must be naiv and must not contain any tzinfo")
    return calendar.timegm(dt.utctimetuple())
