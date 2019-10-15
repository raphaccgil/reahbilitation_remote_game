"""
Integration test
"""
from test.util.mongo_conn_test import TestMongoConn

class Step0:
    """
    This class is going to check the speed to collect information
    """
    def start(self, string_pack, type):

        a = 0
        list_collect = [[], []]
        while a < 1200:
            print(a)
            a += 1
            list_collect = TestMongoConn().insert_data_many_remote_test(list_collect, 40, type)
        with open(
                '/Users/raphacgil/Documents/Raphael/Mestrado/git/reahbilitation_remote_game/logs/{}_{}'.format(type, string_pack),
                'w') as csvfile:
            csvfile.write("{},{}".format('step0_seconds', 'ok'))
            csvfile.write('\n')
            for cont, val in enumerate(list_collect[1]):
                csvfile.write("{},{}".format(str(val), str(list_collect[0][cont])))
                csvfile.write('\n')

if __name__ == "__main__":
    Step0().start('upload_2mbps_block40.csv', 'BASIC')

