'''
Test Routine to collect the information and save on sqllite
'''

from src.util.local_db import LocalDb
from datetime import datetime
import os
import re


class TestSaveDb:

    def test_create_db(self):
        """

        :return: Verify if return a database after creation
        """

        path_now = os.path.dirname(os.getcwd())
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)

        flag = test_connection.create_db()
        print(flag)

        assert flag == 0


    def test_create_calibration(self):
        """

        :return: Verify if return a table created
        """

        path_now = os.path.dirname(os.getcwd())
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)

        flag = test_connection.create_tbl_calibration()
        print(flag)

        assert flag == 0

    def test_insert_db2(self):
        '''

        :return: Verify if the same quantity of data was sent on local database
        '''
        now = datetime.now()
        list_values_data = [now, 1.1111, 2.22222, 3.33333,1.1111, 2.22222, 3.33333]

        path_now = os.path.dirname(os.getcwd())
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)
        flag = test_connection.insert_db(list_values_data)

        assert flag == 0

    def test_insert_calibration1(self):
        '''

        :return: Verify if the same quantity of data was sent on local database
        '''
        list_values = [1.1111, 2.22222, 3.33333]
        path_now = os.path.dirname(os.getcwd())
        print(path_now)
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)
        flag = test_connection.insert_tbl_calibration(list_values)
        assert flag == 0

    def test_verify_data_calibration(self):
        """

        :return: Verify if the same quantity of data was sent on local database
        """

        path_now = os.path.dirname(os.getcwd())
        print(path_now)
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)
        list_flag = test_connection.verify_data_calibration()
        assert len(list_flag) == 3

    def test_clean_data_calibration(self):
        """
        Clean table calibration
        """
        path_now = os.path.dirname(os.getcwd())
        print(path_now)
        files_path_test = re.sub("/test", "", path_now)

        list_temp = [1.1,1.2,1.3]
        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)
        test_connection.insert_tbl_calibration(list_temp)
        test_connection.clean_data_calibration()
        values = test_connection.verify_data_calibration()
        assert len(values) == 0

    def test_create_tbl_conn_speed(self):

        """
        Buff connection speed
        :return: Create database if not exists
        """
        path_now = os.path.dirname(os.getcwd())
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)

        flag = test_connection.create_tbl_conn_speed()
        print(flag)

        assert flag == 0

    def test_insert_tbl_conn_speed(self):
        """

        :return:
        """
        path_now = os.path.dirname(os.getcwd())
        files_path_test = re.sub("/test", "", path_now)

        test_connection = LocalDb()
        test_connection.conn_db(files_path_test)

        val = [datetime.now(), 10.0, 10.0, 25]

        flag = test_connection.insert_tbl_conn_speed(val)
        assert flag == 0

if __name__ == "__main__":
    TestSaveDb().test_insert_tbl_conn_speed()
