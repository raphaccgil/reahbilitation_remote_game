import psutil
import time
from src.util.check_conn_quality import CheckConnQuality
from datetime import datetime


class CheckConnQualityTest:


    def internet_quality_test(self):
        """
        :param last_time:
        :param : Difference between last verification and actual (ms)
        :return: Return mesure of couting value
        """
        t1 = datetime.now()
        last_tot = 0
        flag = 0
        while True:
            ret_list = CheckConnQuality().internet_quality(t1, last_tot, flag)
            rate = ret_list[0]
            last_tot = ret_list[1]
            t1 = ret_list[2]
            flag = ret_list[3]
            print('Download {} Upload {}'.format(rate[1], rate[0]))
            time.sleep(3)


    def get_bytes_test(self):
        CheckConnQuality().get_bytes()

if __name__ == '__main__':
    CheckConnQualityTest().get_bytes_test()