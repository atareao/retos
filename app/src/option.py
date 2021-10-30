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


from table import Table


class Option(Table):
    TABLE = 'OPTIONS'
    PK = 'id'
    UNIKEYS = ['norder', 'reto_id']
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS {}(
    {} INTEGER PRIMARY KEY AUTOINCREMENT,
    reto_id INTEGER,
    norder INTEGER,
    texto STRING,
    isok INTEGER
    )
    """.format(TABLE, PK)

    @classmethod
    def get_options(cls, reto_id):
        condition = f"reto_id='{reto_id}' ORDER BY norder"
        items = cls.select(condition)
        return items

    @classmethod
    def get_ok_options(cls, reto_id):
        condition = f"reto_id='{reto_id}' AND isok=1 ORDER BY norder"
        items = cls.select(condition)
        return items
