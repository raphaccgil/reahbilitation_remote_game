"""
Routine to test socket connection
"""

import pytest
import socket
import re
from datetime import datetime
#from src.business.calibration import Calibration

class TestConnection:

    def __init__(self):
        """
        Load variables
        """
        self.UDP_IP = ""
        self.UDP_PORT = 0
        self.sock = ""
        self.cont = 0

    def test_conn(self):

        self.UDP_IP = ""
        self.UDP_PORT = 2055
        self.sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (self.UDP_IP, self.UDP_PORT)
        udp.bind(orig)
        while self.cont < 100000:
            self.cont += 1
            msg, cliente = udp.recvfrom(1024)
            date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz, = re.split(',', msg.decode('utf-8'))
            print(date_time)
            print(datetime.fromtimestamp(
                float(date_time) / 1000.0
            ).strftime('%Y-%m-%d %H:%M:%S.%f'))

        udp.close()

if __name__ == "__main__":
    TestConnection().test_conn()



