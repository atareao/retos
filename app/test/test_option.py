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

import unittest
import sys
import os
sys.path.append(os.path.join("../src"))
from category import Category
from reto import Reto
from option import Option
from table import Table

Table.DATABASE = 'test.db'


class TestCategory(unittest.TestCase):
    def setUp(self):
        if os.path.exists(Table.DATABASE):
            os.remove(Table.DATABASE)
        Category.inicializate()
        Reto.inicializate()
        Option.inicializate()

    def tearDown(self):
        if os.path.exists(Table.DATABASE):
            os.remove(Table.DATABASE)

    def test_create(self):
        print("=== test_create ===")
        acategory = Category.from_dict({"name": "Category 1",
                                        "webhook": "Webhook 1"})
        acategory.save()
        areto = Reto.from_dict({
            "norder": 1,
            "category_id": acategory.id,
            "question": "pregunta",
            "answer": "respuesta"
            })
        areto.save()
        anoption = Option.from_dict({"reto_id": areto.id,
                                     "norder": 1,
                                     "texto": "texto",
                                     "isok": 1})
        anoption.save()
        anoption_f_db = anoption.get_by_id(anoption.id)
        self.assertEqual(anoption.texto, anoption_f_db.texto)


if __name__ == '__main__':
    unittest.main()
