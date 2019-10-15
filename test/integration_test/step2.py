"""
Integration test
"""
import socket, re, time, numpy
import threading
from src.util.mongo_conn import MongoConn
from src.util.fusion import Fusion
from datetime import datetime, timedelta

class Step2:

    def insert_partial_remote_doctor_test(self):
        """
        Check on mongoDB if has a doctor message
        :return: Return collect data
        """
        test_conn = MongoConn()
        #test_conn.mongodb_conn('reahbilitation_db_test',
        #                       'doctor_coll',
        #                       'mongodb://ec2-3-14-14-152.us-east-2.compute.amazonaws.com:27017/test')

        test_conn.mongodb_conn('reahbilitation_db_test',
                               'doctor_coll',
                               'mongodb://localhost:27017/')

        values = {}
        values['datetime'] = datetime.now()
        values['doctor_message'] = 'Cuidado com o joelho'
        test_conn.insert_data(values)


    def collect_partial_remote_doctor_test(self, string_name):
        """
        Check on mongoDB if has a doctor message
        :return: Return collect data
        """
        a = 0
        collect_times = [[], []]
        while a < 200:
            now = datetime.now()
            test_conn = MongoConn()
            test_conn.mongodb_conn('reahbilitation_db_test',
                                   'doctor_coll',
                                   'mongodb://ec2-3-14-14-152.us-east-2.compute.amazonaws.com:27017/test')

            try:
                flag = test_conn.collect_partial_doctor()
                collect_times[1].append(0)
            except:
                collect_times[1].append(1)
            diff = (datetime.now() - now).total_seconds()
            collect_times[0].append(diff)
            a += 1
            print(a)

        with open(
                '/Users/raphacgil/Documents/Raphael/Mestrado/git/reahbilitation_remote_game/logs/{}.csv'
                        .format(string_name),
                'w') as csvfile:
            csvfile.write("{},{}".format('doctor_collect_seconds', "ok"))
            csvfile.write('\n')
            for cont, val in enumerate(collect_times[0]):
                csvfile.write("{},{}".format(str(val), str(collect_times[1][cont])))
                csvfile.write('\n')

if __name__ == "__main__":
    temp = 0
    Step2().insert_partial_remote_doctor_test()
    #Step2().collect_partial_remote_doctor_test('doctor_message_100kbps')
