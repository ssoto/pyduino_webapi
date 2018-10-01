#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# System imports
import os
# Third party imports
from flask import Flask, abort, url_for, render_template, jsonify
# Local imports
from .models import Arduino


SENSORS = 'sensors'
RELAYS = 'relays'
VALID_ELEMENTS = [SENSORS, RELAYS, ]
TTY_PORT = os.getenv('ARDUINO_TTL_PORT', '/dev/ttyACM0')
CONFIG_SETTINGS = os.getenv('BOARD_YML', 'setup.yml')


def create_app():
    # create and configure the app
    app = Flask(__name__)
    arduino = Arduino(serial_port=TTY_PORT,
                      config_path=CONFIG_SETTINGS)

    @app.route('/', methods=['GET'])
    def index():
        sensors = [
            sensor.to_dict()
            for sensor in arduino.get_all(SENSORS).values()
        ]
        relays = [
            relay.to_dict()
            for relay in arduino.get_all(RELAYS).values()
        ]
        return render_template(
            'index.html',
            sensors=sensors,
            relays=relays,
        )

    @app.route('/<element_type>/<element_id>', methods=['GET'])
    def element_page(element_type, element_id):
        if element_type not in VALID_ELEMENTS:
            url = url_for('get_elements')
            raise abort(500, 'Invalid url {}'.format(url))

        element = arduino.get_one(element_type, element_id)
        if element:
            return render_template(
                'single_element.html',
                element=element.to_dict()
            )
        else:
            raise abort(500, 'Invalid url {}'.format(url))


    @app.route('/data/<element_type>/', methods=['GET'])
    def get_elements(element_type):
        if element_type not in VALID_ELEMENTS:
            url = url_for('get_elements')
            raise abort(500, 'Invalid url {}'.format(url))

        return str([
            element
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

