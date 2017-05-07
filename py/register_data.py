'''  Created on Tue Jun 24 13:32:00 2016
@author: Raphael Gil
Support file to extract data from MariaDB
'''

import pymysql as mariadb
import pandas as pd
import datetime

class EXTRACTION:

    def __init__(self):
        print "start open database"

    def sql_extr1(self, host, user, password, db):
        self.mariadb_connection = mariadb.connect(host=host,  # your host, usually localhost
                                                  user=user,  # your username
                                                  passwd=password,  # your password
                                                  db=db,  # name of the data bas
                                                  local_infile=1)
        query = pd.read_sql_query('''
        select dst.ID2, dst.GOING_DIST, dst.RETURNING_DIST from sugarcaneagrisys.hit_dist dst
        ''', con=self.mariadb_connection)
        return query