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

from time import time
from table import Table


class Tip(Table):
    TABLE = 'TIPS'
    PK = 'id'
    UNIKEYS = ['norder', 'category_id']
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS {}(
    {} INTEGER PRIMARY KEY AUTOINCREMENT,
    norder INTEGER TYPE UNIQUE,
    category_id INTEGER,
    text STRING,
    published INTEGER
    )
    """.format(TABLE, PK)

    def save(self):
        if self.published is None:
            self.published = 0
        super().save()

    def publish(self):
        self.published = time()
        self.save()

    @classmethod
    def get_next_by_category(cls, category_id):
        condition = f"category_id='{category_id}' AND published = 0 ORDER BY norder ASC"
        items = cls.select(condition)
        return items[0] if len(items) > 0 else None

    @classmethod
    def get_next_norder(cls, category_id):
        sqlquery = f"SELECT MAX(norder) FROM {cls.TABLE} WHERE category_id='{category_id}'"
        item = cls.query(sqlquery)
        return item[0][0] + 1
