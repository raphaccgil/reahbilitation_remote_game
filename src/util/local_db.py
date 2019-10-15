"""
Routine to collect the information and save on sqllite
"""

import sqlite3
from src.util.mongo_conn import MongoConn


class LocalDb:
    """
    Manipulate local database
    """

    def __init__(self):

        """
        Create the connection
        """
        self.conn = ""
        self.cursor = ""

    def conn_db(self, path):

        """
        Define database connection

        :param path:
        :return:
        """
        new_path = "{}/files/database/buff_sensor_data.db".format(path)
        print(new_path)
        self.conn = sqlite3.connect(new_path)
        self.cursor = self.conn.cursor()

    def create_db(self):

        """
        Create table for not collected data
        :return: Create database if not exists
        """
        try:
            self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS DADOS_BUFF(
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           time_collect_int int,
                           time_collect timestamp,
                           pitch DOUBLE,
                           median_pitch DOUBLE,
                           yam DOUBLE,
                           median_yam DOUBLE,
                           roll DOUBLE,
                           median_roll DOUBLE,
                           game STRING,
                           patient_id INT,
                           patient_name STRING
                           ) 
                       """)
            self.conn.close()
            return 1
        except:
            return 0

    def create_tbl_calibration(self):

        """
        Collect data after calibration
        :return: Create database if not exists
        """
        try:
            self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS CALIBR_REG(
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           median_yam DOUBLE,
                           median_roll DOUBLE,
                           median_pitch DOUBLE) 
                       """)
            self.conn.close()
            return 0
        except:
            return 1

    def create_tbl_conn_speed(self):

        """
        Buff connection speed
        :return: Create database if not exists
        """
        try:
            self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS SPEEDTEST(
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           datetime timestamp,
                           down_kbps DOUBLE,
                           upl_kbps DOUBLE,
                           ping DOUBLE) 
                       """)
            self.conn.close()
            return 0
        except:
            return 1

    def create_tbl_conn_status(self):

        """
        Buff connection speed
        :return: Create database if not exists
        """
        try:
            self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS CONN_STATUS(
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           datetime timestamp,
                           status STRING) 
                       """)
            self.conn.close()
            return 0
        except:
            return 1

    def insert_tbl_sep(self, list_val):
        """
        Insert collect data from sensors

        :return: The information that database was inserted
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO DADOS_BUFF 
                    (
                     time_collect_int,
                     time_collect,
                     pitch,
                     median_pitch,
                     yam, 
                     median_yam,
                     roll,
                     median_roll,
                     game,
                     patient_id,
                     patient_name 
                     )
                  VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """, (int(list_val[0]),
                        list_val[1],
                        str(list_val[2]),
                        str(list_val[3]),
                        str(list_val[4]),
                        str(list_val[5]),
                        str(list_val[6]),
                        str(list_val[7]),
                        str(list_val[8]),
                        int(list_val[9]),
                        str(list_val[10]),
                        ))
            self.conn.commit()
            self.conn.close()
            return 0
        except:
            self.conn.close()
            return 1

    def insert_tbl_conn_speed(self, list_val):
        """
        Insert data from conn speed

        :return: The information that database was inserted
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO SPEEDTEST 
                    (
                     datetime,
                     down_kbps,
                     upl_kbps,
                     ping
                     )
                  VALUES  (?, ?, ?, ?)
                  """, (list_val[0],
                list_val[1],
                list_val[2],
                list_val[3]))
            self.conn.commit()
            self.conn.close()
            return 0
        except:
            self.conn.close()
            return 1

    def insert_db(self, list_val):
        """
        Insert collect data from sensors

        :return: The information that database was inserted
        """
        valid_data = [len(list_val[0]), 0, 0]
        for cont, val in enumerate(list_val[0]):
            try:
                self.cursor.execute(
                """
                INSERT INTO DADOS_BUFF 
                    (time_collect_int
                     time_collect,
                     pitch,
                     median_pitch,
                     yam, 
                     median_yam,
                     roll,
                     median_roll
                     game,
                     patient_id,
                     patient_name 
                     )
                  VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """, (int(list_val[0][cont]),
                        list_val[1][cont],
                        str(list_val[2][cont]),
                        str(list_val[3][cont]),
                        str(list_val[4][cont]),
                        str(list_val[5][cont]),
                        str(list_val[6][cont]),
                        str(list_val[7][cont]),
                        str(list_val[8][cont]),
                        int(list_val[9][cont]),
                        str(list_val[10][cont])))
                self.conn.commit()
                valid_data[1] += 1
            except:
                valid_data[2] += 1

        self.conn.close()
        return valid_data

    def insert_tbl_calibration(self, list_val):
        """
        Insert data after calibration

        :return: The information that database was inserted
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO CALIBR_REG 
                    (median_yam,
                     median_pitch,
                     median_roll)
                  VALUES  (?, ?, ?)
                  """, (list_val[0],
                        list_val[1],
                        list_val[2]))
            self.conn.commit()
            self.conn.close()
            return 0
        except:
            print("Error inserting median")
            self.conn.close()
            return 1

    def insert_tbl_conn_status(self, list_val):

        """
        Insert data according status connection

        :return: The information that database was inserted
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO CONN_STATUS 
                    (datetime,
                     status)
                  VALUES  (?, ?)
                  """, (list_val[0],
                        list_val[1]))
            self.conn.commit()
            self.conn.close()
            return 0
        except:
            print("Error inserting connection")
            self.conn.close()
            return 1

    def verify_data(self):
        """
        Verify if has data on table from sensors

        :return: The information that database was inserted
        """
        self.cursor.execute(
            """
             SELECT count(*)
             FROM DADOS_BUFF
             """
        )
        cont_val = self.cursor.fetchall()
        if int(cont_val[0][0]) > 0:
            self.conn.close()
            return 1
        else:
            self.conn.close()
            return 0

    def verify_speed(self):
        """
        Collect data from speed

        :return: The information of calibration
        """
        speed_list = []
        try:
            self.cursor.execute(
                """
                 SELECT 
                 datetime,
                 down_kbps,
                 upl_kbps,
                 ping
                 FROM SPEEDTEST
                 order by datetime desc
                 LIMIT 1
                 """)
            cont_val = self.cursor.fetchall()
            for cont, val in enumerate(cont_val[0]):
                speed_list.append(val)
        except:
            print("Erro seleção")

        self.conn.close()
        return speed_list

    def verify_status_conn(self):
        """
        Collect data from calibration

        :return: The information of calibration
        """
        conn_status = []
        try:
            self.cursor.execute(
                """
                 SELECT 
                 datetime,
                 status
                 FROM CONN_STATUS
                 order by datetime desc
                 LIMIT 1
                 """)
            cont_val = self.cursor.fetchall()
            for cont, val in enumerate(cont_val[0]):
                conn_status.append(val)
        except:
            print("Erro seleção")

        self.conn.close()
        print(conn_status)
        return conn_status[1]

    def verify_data_calibration(self):
        """
        Collect last day

        :return: The information of calibration
        """
        median_list = []
        try:
            self.cursor.execute(
                """
                 SELECT 
                 median_yam,
                 median_pitch,
                 median_roll
                 FROM CALIBR_REG
                 LIMIT 1
                 """)
            cont_val = self.cursor.fetchall()
            for cont, val in enumerate(cont_val[0]):
                median_list.append(val)
        except:
            print("Erro seleção")
        self.conn.close()
        return median_list

    def clean_data(self, list_clean):
        """
        Clean table of sensors after send to mongoDB

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
                     """, (a)
                )
                self.conn.commit()
            except:
                print("Error cleaning")
                error_data.append(a)
        self.conn.close()
        return error_data

    def clean_data_calibration(self):
        """
        Clean data from calibration

        :return: If the data was sent, we need to clean the local database
        """
        try:
            self.cursor.execute(
                """
                 DELETE
                 FROM CALIBR_REG
                 """
            )
            self.conn.commit()
            self.conn.close()
            return 0
        except:
            print("Error cleaning")
            self.conn.close()
            return 1

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
        conn_mongo = MongoConn(). \
            mongodb_conn('reahbilitation_db_test',
                         'sensor_coll',
                         'mongodb://ec2-3-14-14-152.us-east-2.compute.amazonaws.com:27017/test')
            #mongodb_conn('reahbilitation_db',
            #             'sensor_coll',
            #             'mongodb://localhost:27017/')
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
