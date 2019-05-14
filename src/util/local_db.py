"""
Routine to collect the information and save on sqllite
"""

import sqlite3
from src.util.mongo_conn import MongoConn


class LocalDb:

    def __init__(self):

        """
        Create the connection
        """
        self.conn = sqlite3.connect('buff_sensor_data.db')
        self.cursor = self.conn.cursor()

    def create_db(self):

        """
        :return: Create database if not exists
        """
        try:
            self.cursor.execute("""
                           CREATE TABLE DADOS_BUFF(
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           time_collect timestamp,
                           pitch DOUBLE,
                           median_pitch DOUBLE,
                           yam DOUBLE,
                           median_yam DOUBLE,
                           roll DOUBLE,
                           median_roll DOUBLE) 
                       """)
            self.conn.close()
            return 1
        except:
            return 0

    def insert_db(self, list_val):
        """
        :return: The information that database was inserted
        """
        valid_data = [len(list_val[0]), 0, 0]
        for cont, val in enumerate(list_val[0]):
            try:
                self.cursor.execute(
                    """
                    INSERT INTO DADOS_BUFF 
                        (time_collect,
                         pitch,
                         median_pitch,
                         yam, 
                         median_yam,
                         roll,
                         median_roll)
                      VALUES  (?, ?, ?, ?, ?, ?, ?)
                      """, (list_val[0][cont],
                            list_val[1][cont],
                            list_val[2][cont],
                            list_val[3][cont],
                            list_val[4][cont],
                            list_val[5][cont],
                            list_val[6][cont]))
                self.conn.commit()
                valid_data[1] += 1
            except:
                valid_data[2] += 1

        self.conn.close()
        return valid_data

    def verify_data(self):
        """
        :return: The information that database was inserted
        """
        self.cursor.execute(
            """
             SELECT count(*)
             FROM DADOS_BUFF
             """
        )
        cont_val = self.cursor.fetchall()
        if int(cont_val[0]) > 0:
            return 1
        else:
            return 0

    def clean_data(self, list_clean):
        """
        :return: If the data was sent, we need to clean the local database
        """
        error_data = []
        for a in list_clean:
            try:
                self.cursor.execute(
                    """
                     DELETE
                     FROM DADOS_BUFF
                     where id = (?)
                     """,(a)
                )
                self.conn.commit()
            except:
                print("Error cleaning")
                error_data.append(a)

        return error_data


class CheckDb:

    def __init__(self):
        self.check = 0

    def check_data(self):
        """
        :return: Verify if have data to send to mongoDB
        """
        value_data = LocalDb().verify_data()
        return value_data

    def check_conn(self):
        """
        :return: Verify if is possible to connect on mongoDB
        """
        conn_mongo = MongoConn().\
            mongodb_conn('reahbilitation_db',
                         'sensor_coll',
                         'mongodb://localhost:27017/')
        if conn_mongo == "error":
            return 0
        else:
            return 1

    def send_data(self, list_json):
        """
        :return: Send data to database
        """
        status = ""
        while self.check < 5 and status != "ok":
            conn_mongo = MongoConn()
            conn_mongo.mongodb_conn('reahbilitation_db',
                             'sensor_coll',
                             'mongodb://localhost:27017/')
            status = conn_mongo.insert_data(list_json)
            self.check += 1

        if self.check < 5:
            return 0
        else:
            return 1
