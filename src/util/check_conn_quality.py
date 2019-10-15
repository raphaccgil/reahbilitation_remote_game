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
        try:
            s = speedtest.Speedtest()
            #down = round(s.download()/1024.0, 2)
            #upl = round(s.upload()/1024.0, 2)
            s.download()
            s.upload()
            res = s.results.dict()
            down = round(float(res["download"])/1024.0, 2)
            upl = round(float(res["upload"])/1024.0, 2)
            ping = round(s.results.ping, 2)

        except:
            down = 0.0
            upl = 0.0
            ping = 999
        return [ping, down, upl]
