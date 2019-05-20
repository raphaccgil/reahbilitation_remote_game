'''
Routine to manipulate from mongoDB
'''

from pymongo import MongoClient, errors


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
            self.album.insert_many(sample_all)
            self.cliente.close()
            return 0
        except:
            self.cliente.close()
            return 1

    def collect_partial(self):
        """

        :return: Return collect data
        """
