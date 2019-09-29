'''
Routine to manipulate from mongoDB
'''

from pymongo import MongoClient, errors, DESCENDING
from pprint import pprint

class MongoConn:
    """
    Prepare to collect mongoDB info
    """

    def __init__(self):
        """
        Load parameter
        """
        self.cliente = ""
        self.banco = ""
        self.album = ""

    def mongodb_conn(self, base, collection, stringconn):
        """
        :param base: Database to collect
        :param collection: Collection used on mongoDB
        :param stringconn: string of connection
        :return: if ok, return value
        """
        try:
            self.cliente = MongoClient(stringconn)
            self.banco = self.cliente[base]
            self.album = self.banco[collection]
            return 0
        except errors.ConnectionFailure:
            return 1

    def mongo_create_index_sensor(self):
        """
        Create index for sensor
        :return:
        """

        index_name1 = 'datetime_int'
        index_name2 = 'id_patient'

        try:
            if 'index_sensor' not in self.album.index_information():
                self.album.create_index([(index_name1,1), (index_name2,1)], name='index_sensor', unique=True)
            self.cliente.close()
            return 0
        except:
            self.cliente.close()
            return 1

    def insert_data(self, sample):
        """
        :param sample: json list with data
        :return: status of insertion
        """
        try:
            self.album.insert_one(sample)
            self.cliente.close()
            return 0
        except:
            self.cliente.close()
            return 1

    def insert_data_many(self, sample_all):
        """
        :param sample: json list with data
        :return: status of insertion
        """
        try:
            self.album.insert_many(sample_all, ordered=False)
            self.cliente.close()
            return 0
        except errors.BulkWriteError:
            pprint(errors.BulkWriteError.details)
            self.cliente.close()
            return 1

    def collect_data_sensor(self):
        """

        :return:
        """
        collect_lst = [[], [], [], []]
        try:
            values = self.album.find()
            for obj in values:
                collect_lst[0].append(obj['datetime_server'])
                collect_lst[1].append(obj['datetime_server_unix'])
                collect_lst[2].append(obj['datetime_sensor'])
                collect_lst[3].append(obj['datetime_sensor_unix'])
        except:
            print('Error')

        return collect_lst

    def collect_partial_doctor(self):
        """
        Check on mongoDB if has a doctor message
        :return: Return collect data
        """
        try:
            latest_doc = self.album.find().sort("datetime", DESCENDING).limit(1)
            self.cliente.close()
            return latest_doc[0]['doctor_message']
        except:
            self.cliente.close()
            return 1
