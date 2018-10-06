#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import argparse
import sys

from pyfirmata import Arduino, util
from influxdb import InfluxDBClient

# FIXME: this must should be set by arguments
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def log(msg):
    time = datetime.datetime.utcnow().strftime(TIME_FORMAT)
    print('{} - {}'.format(time, msg))


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
    parser.add_argument('-i', '--influx-host',
                        type=str, required=False, default=None,
                        dest='influxdb_host',
                        help='If specified, data will be send to influxdb')
    parser.add_argument('-db', '--database-name',
                        type=str, required=False, default='poc_humidity',
                        dest='database',
                        help='Influxdb database name. Default value will be'
                             'poc_humidity')
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
    log('Initializing....')
    board = Arduino(args.arduino_device)
    log('Arduino connected to: {}'.format(args.arduino_device))
    initialize_arduino_reading(board, args.analog_ports)

    client = None
    if args.influxdb_host:
        client = InfluxDBClient(args.influxdb_host, 8086,
                                'root', 'root', args.database)
        client.create_database(args.database)

    points = []
    for port in args.analog_ports:
        port_read = board.analog[port].read()
        log('Port {}: {}'.format(port, port_read))
        if client:
            time = datetime.datetime.utcnow().strftime(TIME_FORMAT)
            port_name = 'A{}'.format(port)
            point = dict(
                measurement='humidity_sensor',
                time=time,
                fields={'value': port_read},
                tags={'sensor_port': port_name}
            )
            log(point)
            points.append(point)
    if client and points:
        client.write_points(points)
    board.exit()
    log('Connection with board has been closed')
    log('Finish')


if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit(1)
    sys.exit(0)
