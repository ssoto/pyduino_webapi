import datetime

import time
from pyfirmata import Arduino, util


if __name__ == '__main__':
    port = '/dev/cu.usbmodem1411'
    board = Arduino(port)
    print('Arduino connected to: {}'.format(port))

    it = util.Iterator(board)
    board.analog[0].enable_reporting()
    board.analog[2].enable_reporting()
    it.start()

    while True:
        value_0 = board.analog[0].read()
        value_2 = board.analog[2].read()
        print('{}\n Value A0: {}\n Value A2: {}\n======'.format(
            datetime.datetime.now(),
            value_0, value_2))
        time.sleep(1)
