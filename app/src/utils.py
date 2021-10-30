#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import os
import hmac
import hashlib

TRUE = 0
FALSE = 1


def load_env(filename):
    with open(filename, 'r') as fr:
        for line in fr.readlines():
            key, value = line.split("=")
            if value and value[-1] == '\n':
                value = value[:-1]
            value = value.strip()
            key = key.strip()
            if value and key:
                os.environ[key] = value
                Log.info(f"{key}={value}")


def get_signature(secret, data):
    return hmac.new(bytes(secret, 'utf-8'),
                    msg=data,
                    digestmod=hashlib.sha256).hexdigest()


class LogLevel:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class Log:
    DEBUG = LogLevel("Debug", 3)
    INFO = LogLevel("Info", 2)
    WARN = LogLevel("Warn", 1)
    ERROR = LogLevel("Error", 0)
    LEVEL = DEBUG

    @staticmethod
    def set(level):
        if level.upper() == "INFO":
            Log.LEVEL = Log.INFO
        elif level.upper() == "WARN":
            Log.LEVEL = Log.WARN
        elif level.upper() == "ERROR":
            Log.LEVEL = Log.ERROR
        else:
            Log.LEVEL = Log.DEBUG

    @classmethod
    def base(cls, level, message):
        if cls.LEVEL.value >= level.value:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            print(f"{level.name} - {timestamp} | {message}")

    @classmethod
    def info(cls, message):
        cls.base(cls.INFO, message)

    @classmethod
    def warn(cls, message):
        cls.base(cls.WARN, message)

    @classmethod
    def error(cls, message):
        cls.base(cls.ERROR, message)

    @classmethod
    def debug(cls, message):
        cls.base(cls.DEBUG, message)
