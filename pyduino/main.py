#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# System imports
import os
# Third party imports
from flask import Flask, abort, url_for
# Local imports
from .models import Arduino


VALID_ELEMENTS = ['sensors', 'relays', ]
TTY_PORT = os.getenv('ARDUINO_TTL_PORT', '/dev/ttyACM0')
CONFIG_SETTINGS = os.getenv('BOARD_YML', 'setup.yml')


def create_app():
    # create and configure the app
    app = Flask(__name__)
    arduino = Arduino(serial_port=TTY_PORT,
                      config_path=CONFIG_SETTINGS)

    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello, World!'

    @app.route('/data/<element_type>/', methods=['GET'])
    def get_elements(element_type):
        if element_type not in VALID_ELEMENTS:
            url = url_for('get_elements')
            raise abort(500, 'Invalid url {}'.format(url))

        return str([
            [element.id, element.port_code, element.port_name, element.read_value()]
            for id, element in arduino.get_all(element_type).items()
        ])

    @app.route('/data/<element_type>/<id>', methods=['GET'])
    def get_element(element_type, id):
        if element_type not in VALID_ELEMENTS:
            url = url_for('get_elements')
            raise abort(500, 'Invalid url {}'.format(url))
        found = arduino.get_one(element_type, id)
        return str([found.id, found.port_code, found.read_value()])

    return app

