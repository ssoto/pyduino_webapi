#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import argparse

import time
from pyfirmata import Arduino, util
from influxdb import InfluxDBClient

# FIXME: this must should be set by arguments
DATABASE = 'poc_humidity'


def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-dev', '--arduino-device',
                        type=str, required=True, dest='arduino_device',
                        help='This will be device where arduino is '
                             'connected. Should something like '
                             '/dev/cu.usbmodem1411')
    parser.add_argument('-ap', '--analog-ports',
                        nargs='+', type=int, required=True,
                        dest='analog_ports',
                        help='Should be a list of integers. P.e.: 3 5 8'
                        )
    parser.add_argument('-s', '--sleep-seconds',
                        type=int, required=False, default=1,
                        dest='sleep_seconds',
                        help='Number of seconds to wait. Default 1')
    parser.add_argument('-i', '--influx_host',
                        type=str, required=False, default=None,
                        dest='influxdb_host',
                        help='If specified, data will be send to influxdb')
    return parser.parse_args()


def initialize_arduino_reading(board,
                               analog_ports=None,
                               digital_ports=None):
    it = util.Iterator(board)
    if analog_ports:
        for port in analog_ports:
            board.analog[port].enable_reporting()
    if digital_ports:
        for port in digital_ports:
            board.digital[port].enable_reporting()
    it.start()


def main():
    args = get_arguments()
    print('Initializing....')
    board = Arduino(args.arduino_device)
    print('Arduino connected to: {}'.format(args.arduino_device))
    initialize_arduino_reading(board, args.analog_ports)

    client = None
    if args.influxdb_host:
        client = InfluxDBClient(args.influxdb_host, 8086,
                                'root', 'root', DATABASE)
        client.create_database(DATABASE)

    while True:
        print('{}'.format(datetime.datetime.now()))
        points = []
        for port in args.analog_ports:
            port_read = board.analog[port].read()
            print('Port {}: {}'.format(port, port_read))
            if client:
                points.append(
                    dict(
                        measurement='humidity_sensor',
                        time=datetime.datetime.now().isoformat(),
                        fields={'value': port_read},
                        tags={'sensor_port': port}
                    )
                )
        if client and points:
            client.write_points(points)
        print('====================')
        # FIXME: parametrize
        time.sleep(args.sleep_seconds)


if __name__ == '__main__':
    main()