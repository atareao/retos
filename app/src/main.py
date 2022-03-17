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

import os
import requests
from flask import Flask, jsonify, make_response, request
from table import Table
from category import Category
from reto import Reto
from tip import Tip
from option import Option
from jsonencoders import TableJSONEncoder
from utils import Log, get_signature

if os.environ['ENVIRONMENT'] == 'TEST':
    Table.DATABASE = '/app/database/retos.db'
else:
    Table.DATABASE = '/app/database/retos.db'
Log.set(os.environ['DEBUG'])

NUMBERS = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:",
           ":six:", ":seven:", ":eight:", ":nine:"]

app = Flask(__name__)
app.json_encoder = TableJSONEncoder


@app.route('/status', methods=['GET'])
def get_status():
    return make_response(jsonify({'status': 'Up and running'}), 200)


@app.route('/api/v1/test', methods=['POST'])
def test():
    for header in request.headers:
        Log.info(header)
    Log.info(request.data)
    Log.info(get_signature('secreto', request.data))
    Log.info(get_signature('secreto', '{"key1":"value1"}'.encode('utf-8')))
    return make_response(jsonify({'status': 'Up and running'}), 200)


@app.route('/api/v1/category', methods=['GET'])
@app.route('/api/v1/category/<int:id>', methods=['GET'])
def index_category(id=None):
    if id:
        return make_response(jsonify(Category.get_by_id(id)))
    return make_response(jsonify(Category.get_all()))


@app.route('/api/v1/reto', methods=['GET'])
@app.route('/api/v1/reto/<int:id>', methods=['GET'])
def index_reto(id=None):
    if id:
        return make_response(jsonify(Reto.get_by_id(id)))
    return make_response(jsonify(Reto.get_all()))


@app.route('/api/v1/reto/next/<int:id>', methods=['GET'])
def next_reto(id=None):
    category = Category.get_by_id(id)
    if category:
        reto = Reto.get_first_answer_not_published_by_category(id)
        if reto:
            ok_options = Option.get_ok_options(reto.id)
            p = []
            message = f"Para el reto **{reto.norder}**: *{reto.question}*, "
            if len(ok_options) == 0:
                message += "Todas las respuestas eran **incorrectas**"
            elif len(ok_options) == 1:
                message += "La respuesta **correcta** era:\n"
                message += "\n" + f"{NUMBERS[ok_options[0].norder]} " \
                           f"{ok_options[0].texto}"
            elif len(ok_options) > 1:
                message += "Las respuestas **correctas** eran:\n"
                o = [f"{NUMBERS[anoption.norder]} {anoption.texto}"
                     for anoption in ok_options]
                message += "\n".join(o)
            else:
                return not_found(404)
            requests.post(category.reto_webhook, {"content": message})
            reto.publish_answer()
            return make_response("OK", 200)
        else:
            reto = Reto.get_first_question_not_published_by_category(id)
            if reto:
                options = Option.get_options(reto.id)
                p = []
                p.append(f"Reto **{reto.norder}**: **{reto.question}**")
                o = []
                for anoption in options:
                    p.append(f"{NUMBERS[anoption.norder]} {anoption.texto}")
                    o.append(NUMBERS[anoption.norder])
                p.append(f"@everyone, responde a este reto de la categoría \
        **{category.name}**")
                opciones = ", ".join(o)
                p.append(f"Elige tu opción **reaccionando** con {opciones}")
                message = "\n".join(p)
                requests.post(category.reto_webhook, {"content": message})
                reto.publish_question()
                return make_response(jsonify({'status': 'OK',
                                              'msg': 'Published'}), 200)
            else:
                return not_found(404)


@app.route('/api/v1/tip/next/<int:id>', methods=['GET'])
def next_tip(id=None):
    category = Category.get_by_id(id)
    if category:
        tip = Tip.get_next_by_category(id)
        if tip:
            p = []
            p.append(f"Tip **{tip.norder}** sobre **{category.name}**")
            p.append(tip.text)
            message = "\n".join(p)
            requests.post(category.tip_webhook, {"content": message})
            tip.publish()
            return make_response(jsonify({'status': 'OK',
                                          'msg': 'Published'}), 200)
    return not_found(404)


@app.route('/api/v1/tip', methods=['GET'])
@app.route('/api/v1/tip/<int:id>', methods=['GET'])
def index_tip(id=None):
    if id:
        return make_response(jsonify(Tip.get_by_id(id)))
    return make_response(jsonify(Tip.get_all()))


@app.errorhandler(404)
def not_found(error):
    msg = str(error)
    return make_response(jsonify({'status': 'error', 'msg': msg}), 404)


def init():
    Log.info("==================================")
    Log.info(Table.DATABASE)
    Log.info("==================================")
    Category.inicializate()
    Reto.inicializate()
    Tip.inicializate()
    Option.inicializate()


init()
