#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# System imports
import os
import random
# Third party imports
import serial
import yaml
# Local imports

# Relays status
ON = 'on'
OFF = 'off'

RELAY = 'relay'
SENSOR = 'sensor'
ELEMENT_TYPES = ['relay', 'sensor', 'humidity', ]

VALID_ELEMENTS = []


class ElectricElement:

    def __init__(self, element_type, id, port_name):
        if element_type not in ELEMENT_TYPES:
            raise ValueError('Element type name not recognized: {}'.format(
                element_type
            ))
        self.type = element_type
        self.id = id
        # FIXME: D or A type
        self.port_type, self.port_code = self.build_port_name(port_name)

    @staticmethod
    def build_port_name(name):
        """Try to build port characteristics using an string input

        :param name:
        :return: list with [port_type, port_code]
        """
        if len(name) < 2:
            error_msg = 'Port name must have almost 2 chars: {}'.format(
                name
            )
            raise ValueError(error_msg)

        port_type = name[0]
        if port_type not in ['A', 'D']:
            error_msg = 'Port type must be A (analog) or D (digital): {}'.format(
                port_type
            )
            raise ValueError(error_msg)
        port_str = name[1:]
        try:
            port_code = int(port_str)
        except ValueError:
            error_msg = 'Invalid port code: {}'.format(
                port_str
            )
            raise ValueError(error_msg)
        return port_type, port_code

    def read_value(self):
        return random.randint(1, 1000)

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.id,
            'port_type': self.port_type,
            'port_code': self.port_code,
            'value': self.read_value(),
        }


class Relay(ElectricElement):

    def __init__(self, id, port, default_status=ON) -> None:
        super(Relay, self).__init__(RELAY, id, port)
        if default_status not in [ON, OFF]:
            raise ValueError('Status is not valid for relay: {}'.format(
                default_status
            ))
        self.is_on = default_status

    def turn_on(self):
        raise NotImplemented('Method turn_on not implemented')

    def turn_off(self):
        raise NotImplemented('Method turn_off not implemented')


class Sensor(ElectricElement):

    def __init__(self, id, port):
        super(Sensor, self).__init__(SENSOR, id, port)


class Board:

    def __init__(self, id, sensors=None, relays=None):
        self.id = id
        self.sensors = {}
        if sensors:
            for sensor in sensors:
                sensor_item = Sensor(
                    port=sensor['port'],
                    id=sensor['id'],
                )
                self.sensors[sensor_item.id] = sensor_item
        self.relays = {}
        if relays:
            for relay in relays:
                relay_item = Relay(
                    id=relay['id'],
                    port=relay['port'],
                )
                if 'status' in relay:
                    relay_item.is_on = relay['status']
                self.relays[relay_item.id] = relay_item


class SetupConfig:

    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise ValueError('File {} doesn\'t exist'.format(
                config_path
            ))
        self.raw_config = yaml.load(open(config_path))
        self.boards = {}
        for board in self.raw_config:
            board_id = board['boardId']
            board_item = Board(
                id=board_id,
                sensors=board['sensors'],
                relays=board['sensors'],
            )
            self.boards[board_id] = board_item


class Arduino:

    """ Models Arduino object"""

    def __init__(self, serial_port, config_path, baud_rate=115200,
                 read_timeout=5):
        """
        Initializes the serial connection to the Arduino board
        """
        self.config = SetupConfig(config_path)
        self.boards = self.config.boards
        # self.conn = serial.Serial(serial_port, baud_rate)
        # self.conn.timeout = read_timeout  # Timeout for readline()

    def get_all(self, element_type):
        result = {}
        for board in self.boards.values():
            elements = getattr(board, element_type)
            if elements:
                result.update(elements)
        return result

    def get_one(self, element_type, element_id):
        for board in self.boards.values():
            elements = getattr(board, element_type)
            element = elements.get(element_id)
            if element:
                return element

