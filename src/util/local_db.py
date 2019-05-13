'''
Routine to collect the information and save on sqllite
'''

class SaveDb:

    def create_db(self):
        '''
        :return: Create database if not exists
        '''

        pass

    def insert_db(self):
        '''

        :return: The information that database was inserted
        '''

        pass

class Check_db:

    def check_data(self):
        '''

        :return: Verify if have data to send to mongoDB
        '''
        pass

    def check_conn(self):
        '''

        :return: Verify if is possible to connect on mongoDB
        '''
        pass

    def send_data(self):
        '''

        :return: Send data to database
        '''
        pass

    def clean_data(self):
        '''

        :return: If the data was sent, we need to clean the local database
        '''
        pass
