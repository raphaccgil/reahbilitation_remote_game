"""
Test mongoDB configuration
"""

from src.util.mongo_conn import MongoConn
import pytest
from datetime import datetime

class TestMongoConn:
    """
    Test mongo class
    """
    def mongo_conn_test(self):

        flag = MongoConn().mongodb_conn('reahbilitation_db',
                     'sensor_coll',
                     'mongodb://localhost:27017/')
        assert flag == 0

    def insert_data_test(self):

        print("Ola test")
        test_conn =  MongoConn()
        test_conn.mongodb_conn('reahbilitation_db_test',
                     'sensor_coll',
                     'mongodb://localhost:27017/')

        values = {}
        values['Date'] = datetime.now()
        values['pitch'] = 3.11111111111111111
        values['median_pitch'] = 3.11111111111111111
        values['roll'] = 3.11111111111111111
        values['median_roll'] = 3.11111111111111111
        values['yam'] = 3.11111111111111111
        values['median_yam'] = 3.11111111111111111
        values['game_selection'] = 'Game1'
        values['name_patient'] = 'Carlos'
        values['id_patient'] = 1001

        flag = test_conn.insert_data(values)

        assert flag == 0

    def insert_data_many_test(self):

        print("Ola test")
        test_conn =  MongoConn()
        test_conn.mongodb_conn('reahbilitation_db_test',
                     'sensor_coll',
                     'mongodb://localhost:27017/')

        values = {}
        values['Date'] = datetime.now()
        values['pitch'] = 3.11111111111111111
        values['median_pitch'] = 3.11111111111111111
        values['roll'] = 3.11111111111111111
        values['median_roll'] = 3.11111111111111111
        values['yam'] = 3.11111111111111111
        values['median_yam'] = 3.11111111111111111
        values['game_selection'] = 'Game1'
        values['name_patient'] = 'Carlos'
        values['id_patient'] = 1001

        values_all = []

        values_all.append(values)
        flag = test_conn.insert_data_many(values_all)

        assert flag == 0

    def collect_partial_doctor_test(self):
        """
        Check on mongoDB if has a doctor message
        :return: Return collect data
        """
        test_conn = MongoConn()
        test_conn.mongodb_conn('reahbilitation_db',
                               'doctor_coll',
                               'mongodb://localhost:27017/')

        values = {}
        values['datetime'] = datetime.now()
        values['doctor_message'] = 'Nova Mensagem'
        test_conn.insert_data(values)

        test_conn = MongoConn()
        test_conn.mongodb_conn('reahbilitation_db',
                               'doctor_coll',
                               'mongodb://localhost:27017/')

        flag = test_conn.collect_partial_doctor()
        assert flag == 'Nova Mensagem'

if __name__ == "__main__":
    TestMongoConn().collect_partial_doctor_test()