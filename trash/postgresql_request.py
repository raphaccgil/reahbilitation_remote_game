'''  Created on Tue Marc 07 14:42:00 2017
@author: Raphael Gil
Support file to extract data from PostgreSQL
'''

import psycopg2 as postsql


class PostgreSQL:

    def __init__(self):
        pass

    def sql_con(self, host, user, passwd, db, port):
        self.postsql_connection = postsql.connect(host=host,  # your host, usually localhost
                                                  user=user,  # your username
                                                  password=passwd,  # your password
                                                  dbname=db,  # name of the data bas
                                                  port= port  # port
                                                  )

    def write_temp(self, id1, dat1, dat2, acx, acy, acz, mgx, mgy, mgz, gyx, gyy, gyz,
                                head, pitch, roll, hd_med, pt_med, rl_med):
            cursor = self.postsql_connection.cursor()
            #try:
            cursor.execute('''insert into public.temp_data_acquire
                              (ID_LOG,datetime_unix, data_log, accx, accy, accz,
                               magx, magy, magz, gyrx, gyry, gyrz, head ,
                               pitch, roll, head_median,pitch_median, roll_median)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                               (id1, dat1, dat2, acx, acy, acz, mgx, mgy, mgz, gyx, gyy, gyz,
                                head, pitch, roll, hd_med, pt_med, rl_med))
            self.postsql_connection.commit()
            #except:
            #self.postsql_connection.rollback()

    def write_temp2(self, dat1, dat2, hd_med, pt_med, rl_med):
            cursor = self.postsql_connection.cursor()
            #try:
            cursor.execute('''insert into public.temp_data_acquire2
                              (datetime_unix, data_log, head_median, pitch_median, roll_median)
                               VALUES (%s,%s,%s,%s,%s)''',
                               (dat1, dat2, hd_med, pt_med, rl_med))
            self.postsql_connection.commit()
            #except:
            #self.postsql_connection.rollback()

    def up_table(self):
        cursor = self.postsql_connection.cursor()
        cursor.execute('''update public.gps_table set local =
                          ST_GeomFromText('SRID=4326;POINT(' || (longit) || ' ' ||  (lat) || ')');''')
        self.postsql_connection.commit()

    def read_sensor_game2(self):
        cursor = self.postsql_connection.cursor()
        cursor.execute('''SELECT *from public.temp_data_acquire2 db
                          where db.datetime_unix = (select MAX(datetime_unix) from public.temp_data_acquire2)''')
        all_val = cursor.fetchall()
        var1 = 0
        var2 = 0
        var3 = 0
        var4 = 0
        var5 = 0
        for count1, row in enumerate(all_val):
            for count2, columns in enumerate(row):
                if count2 == 0:
                    var1 = columns
                elif count2 == 1:
                    var2 = columns
                elif count2 == 2:
                    var3 = columns
                elif count2 == 3:
                    var4 = columns
                elif count2 == 4:
                    var5 = columns

        return var1, var2, var3, var4, var5

    def read_sensor_game(self):
        cursor = self.postsql_connection.cursor()
        cursor.execute('''SELECT *from public.temp_data_acquire db
                          where db.datetime_unix = (select MAX(datetime_unix) from public.temp_data_acquire)''')
        all_val = cursor.fetchall()
        var1 = 0
        var2 = 0
        var3 = 0
        var4 = 0
        var5 = 0
        var6 = 0
        var7 = 0
        var8 = 0
        var9 = 0
        var10 = 0
        var11 = 0
        var12 = 0
        var13 = 0
        var14 = 0
        var15 = 0
        var16 = 0
        var17 = 0
        for count1, row in enumerate(all_val):
            for count2, columns in enumerate(row):
                if count2 == 1:
                    var1 = columns
                elif count2 == 2:
                    var2 = columns
                elif count2 == 3:
                    var3 = columns
                elif count2 == 4:
                    var4 = columns
                elif count2 == 5:
                    var5 = columns
                elif count2 == 6:
                    var6 = columns
                elif count2 == 7:
                    var7 = columns
                elif count2 == 8:
                    var8 = columns
                elif count2 == 9:
                    var9 = columns
                elif count2 == 10:
                    var10 = columns
                elif count2 == 11:
                    var11 = columns
                elif count2 == 12:
                    var12 = columns
                elif count2 == 13:
                    var13 = columns
                elif count2 == 14:
                    var14 = columns
                elif count2 == 15:
                    var15 = columns
                elif count2 == 16:
                    var16 = columns
                elif count2 == 17:
                    var17 = columns
        return var1, var2, var3, var4,\
               var5, var6, var7, var8,\
               var9, var10, var11, var12,\
               var13, var14, var15,\
               var16, var17

    def deltabletemp(self):
        cursor = self.postsql_connection.cursor()
        cursor.execute('''delete from public.temp_data_acquire''')
        self.postsql_connection.commit()

    def tabledata2(self):
        cursor = self.postsql_connection.cursor()
        cursor.execute('''CREATE TABLE If NOT EXISTS  public.temp_data_acquire
                          (
                          ID_LOG integer,
                          datetime_unix bigint,
                          data_log timestamp without time zone,
                          accx DOUBLE PRECISION,
			              accy DOUBLE PRECISION,
			              accz DOUBLE PRECISION,
                          magx DOUBLE PRECISION,
                          magy DOUBLE PRECISION,
                          magz DOUBLE PRECISION,
                          gyrx DOUBLE PRECISION,
                          gyry DOUBLE PRECISION,
                          gyrz DOUBLE PRECISION,
                          head DOUBLE PRECISION,
                          pitch DOUBLE PRECISION,
                          roll DOUBLE PRECISION,
                          head_median DOUBLE PRECISION,
			              pitch_median DOUBLE PRECISION,
			              roll_median DOUBLE PRECISION,
                          CONSTRAINT unique_time UNIQUE (datetime_unix)
                          )''')
        self.postsql_connection.commit()

    def post_close_connection(self):
        self.postsql_connection.close()

if __name__ == '__main__':
    print 'start analyzes from main program'
    alfa = PostgreSQL()
    alfa.sql_con("10.93.1.62", "postgres", 'ra2730ar', "Mill_GPS")
    alfa.tabledata2()
