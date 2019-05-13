'''
Test Routine to collect the information and save on sqllite
'''

from src.util.local_db import Check_db, SaveDb
import pytest
import sqlite3

class Test_saveDb:

    def test_create_db(self):
        '''

        :return: Verify if return a database after creation
        '''

    def test_insert_db1(self):
        '''

        :return: Verify if data was sent on local database
        '''

        SaveDb().insert_db()

    def test_insert_db2(self):
        '''

        :return: Verify if the same quantity of data was sent on local database
        '''

        SaveDb().insert_db()

