"""
Routine to chek conn quality
"""

import psutil
import time
from datetime import datetime
import speedtest
import speedtest_cli


class CheckConnQuality:

    def __int__(self):
        self.interface = 'WiFi'

    def internet_quality(self, last_time, last_tot, flag):
        """
        :param last_time:
        :param : Difference between last verification and actual (ms)
        :return: Return mesure of couting value
        """
        try:
            temp = psutil.net_io_counters().bytes_sent(permin=True)
            print(temp['WiFi'])
        except:
            print('no wifi')

        t1 = datetime.now()
        diff = (t1 - last_time).microseconds
        if flag == 0:
            last_tot = (psutil.net_io_counters().bytes_sent,
                        psutil.net_io_counters().bytes_recv)
            flag = 1

        tot = (psutil.net_io_counters().bytes_sent,
               psutil.net_io_counters().bytes_recv)

        ul, dl = [(now - last) / (float(diff)/1000000.0) / 100000.0
                  for now, last in zip(tot, last_tot)]
        print()
        print(tot)
        print(last_tot)
        rate = (ul, dl)
        return [rate, tot, t1, flag]


    def get_bytes(self):
        alfa = datetime.now()
        s = speedtest.Speedtest()

        down = round(s.download()/1000.0, 2)
        upl = round(s.upload()/1000.0, 2)
        ping = s.results.ping
        beta = datetime.now()
        diff = (beta - alfa).total_seconds()
        print(ping)
        print('Download {}Kbps Upload {}Kbps analisado em {}s'.format(down, upl, diff))
