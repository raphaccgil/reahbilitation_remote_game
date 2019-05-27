"""
Routine to chek conn quality
"""

import psutil
import time
from datetime import datetime
import speedtest


class CheckConnQuality:

    def __int__(self):
        self.interface = 'WiFi'

    def internet_quality(self):
        """
        :return: Values of ping, download and upload
        """
        s = speedtest.Speedtest()
        down = round(s.download()/1000.0, 2)
        upl = round(s.upload()/1000.0, 2)
        ping = s.results.ping
        return [ping, down, upl]
