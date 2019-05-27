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
        alfa = datetime.now()
        s = speedtest.Speedtest()

        down = round(s.download()/1000.0, 2)
        upl = round(s.upload()/1000.0, 2)
        ping = s.results.ping
        beta = datetime.now()
        diff = (beta - alfa).total_seconds()
        print(ping)
        print('Download {}Kbps Upload {}Kbps analisado em {}s'.format(down, upl, diff))
