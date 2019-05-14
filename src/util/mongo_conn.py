'''
Routine to manipulate from mongoDB
'''

from pymongo import MongoClient, errors


class MongoConn:

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
            return self
        except errors.ConnectionFailure:
            return "error"

    def collect_partial(self):
        """
        :return: Return collect data
        """
