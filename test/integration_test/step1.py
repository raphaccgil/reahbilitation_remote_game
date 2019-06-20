"""
Integration test
"""
import socket, re, time, numpy
import threading
from src.util.mongo_conn import MongoConn
from src.util.fusion import Fusion
from datetime import datetime, timedelta


def threading_sensor(sock, flagtime, acquir_data, acq_list, time_check, upload_speed):

    a = 0
    last_t = datetime.now()
    now_t = datetime.now()

    inc_check = 0

    while a < 6000:

        if upload_speed > 100:
            inc_check += 1
        elif 50 <= upload_speed <= 100:
            inc_check += 0.5
        else:
            inc_check += 0.1

        data, addr = sock.recvfrom(1024)
        date_time, accx, accy, accz, magx, magy, magz, gyrx, gyry, gyrz,  = re.split(',', data.decode('utf-8'))
        check_time = datetime.now()
        sensor_time = datetime.fromtimestamp(float(date_time) / 1000.0)
        acc = (float(accx), float(accy), float(accz))
        mag = (float(magx), float(magy), float(magz))
        gyr = (float(gyrx), float(gyry), float(gyrz))
        if flagtime == 0:
            acquir_data.update(acc, gyr, mag, 0)
            flagtime = 1
            last_t = datetime.now()
        else:
            now_t = datetime.now()
            diff = float((now_t - last_t).microseconds)
            acquir_data.update(acc, gyr, mag, diff)

        if inc_check >= 1:
            acq_list[0].append(acquir_data.heading)
            acq_list[1].append(acquir_data.pitch)
            acq_list[2].append(acquir_data.roll)
            #acq_list[3].append(date_time)
            #acq_list[4].append(datetime.fromtimestamp(float(date_time) / 1000.0) \
            #    .strftime('%Y-%m-%d %H:%M:%S.%f'))
            acq_list[4].append(datetime.now())
            alfa = lambda: int(round(time.time() * 1000))
            acq_list[3].append(alfa())

            inc_check = 0

        a += 1


def prepare_json(acq_list, old_len, new_len):
    data_collect = []
    for cont in range(old_len, new_len):
        dict_val = {}
        alfa = datetime.now()
        server_time = lambda: int(round(time.time() * 1000))
        dict_val['datetime_server'] = alfa
        dict_val['datetime_server_unix'] = int(server_time())
        dict_val['yam'] = acq_list[0][cont]
        dict_val['median_yam'] = numpy.median(acq_list[0])
        dict_val['pitch'] = acq_list[1][cont]
        dict_val['median_pitch'] = numpy.median(acq_list[1])
        dict_val['roll'] = acq_list[2][cont]
        dict_val['median_roll'] = numpy.median(acq_list[2])
        dict_val['datetime_sensor'] = acq_list[4][cont]
        dict_val['datetime_sensor_unix'] = int(acq_list[3][cont])
        dict_val['game_selection'] = 'Game1'
        dict_val['name_patient'] = 'Carlos'
        dict_val['id_patient'] = 1001
        '''
        dict_val['free1'] = 3.11111111111111111
        dict_val['free2'] = 3.11111111111111111
        dict_val['free3'] = 3.11111111111111111
        dict_val['free4'] = 3.11111111111111111
        dict_val['free5'] = 3.11111111111111111
        dict_val['free6'] = 3.11111111111111111
        dict_val['free7'] = 3.11111111111111111
        dict_val['free8'] = 3.11111111111111111
        dict_val['free9'] = 3.11111111111111111
        dict_val['free10'] = 3.11111111111111111
        dict_val['free11'] = 3.11111111111111111
        dict_val['free12'] = 3.11111111111111111
        dict_val['free13'] = 3.11111111111111111
        dict_val['free14'] = 3.11111111111111111
        dict_val['free15'] = 3.11111111111111111
        dict_val['free16'] = 3.11111111111111111
        dict_val['free17'] = 3.11111111111111111
        dict_val['free18'] = 3.11111111111111111
        dict_val['free19'] = 3.11111111111111111
        dict_val['free20'] = 3.11111111111111111
        dict_val['free21'] = 3.11111111111111111
        dict_val['free22'] = 3.11111111111111111
        dict_val['free23'] = 3.11111111111111111
        dict_val['free24'] = 3.11111111111111111
        dict_val['free25'] = 3.11111111111111111
        dict_val['free26'] = 3.11111111111111111
        dict_val['free27'] = 3.11111111111111111
        dict_val['free28'] = 3.11111111111111111
        dict_val['free29'] = 3.11111111111111111
        dict_val['free30'] = 3.11111111111111111
        dict_val['free31'] = 3.11111111111111111
        dict_val['free32'] = 3.11111111111111111
        dict_val['free33'] = 3.11111111111111111
        dict_val['free34'] = 3.11111111111111111
        dict_val['free35'] = 3.11111111111111111
        dict_val['free36'] = 3.11111111111111111
        dict_val['free37'] = 3.11111111111111111
        dict_val['free38'] = 3.11111111111111111
        dict_val['free39'] = 3.11111111111111111
        dict_val['free40'] = 3.11111111111111111
        dict_val['free41'] = 3.11111111111111111
        dict_val['free42'] = 3.11111111111111111
        dict_val['free43'] = 3.11111111111111111
        dict_val['free44'] = 3.11111111111111111
        dict_val['free45'] = 3.11111111111111111
        dict_val['free46'] = 3.11111111111111111
        dict_val['free47'] = 3.11111111111111111
        dict_val['free48'] = 3.11111111111111111
        dict_val['free49'] = 3.11111111111111111
        dict_val['free50'] = 3.11111111111111111
        dict_val['free51'] = 3.11111111111111111
        dict_val['free52'] = 3.11111111111111111
        dict_val['free53'] = 3.11111111111111111
        dict_val['free54'] = 3.11111111111111111
        dict_val['free55'] = 3.11111111111111111
        dict_val['free56'] = 3.11111111111111111
        dict_val['free57'] = 3.11111111111111111
        dict_val['free58'] = 3.11111111111111111
        dict_val['free59'] = 3.11111111111111111
        dict_val['free60'] = 3.11111111111111111
        dict_val['free61'] = 3.11111111111111111
        dict_val['free62'] = 3.11111111111111111
        dict_val['free63'] = 3.11111111111111111
        dict_val['free64'] = 3.11111111111111111
        dict_val['free65'] = 3.11111111111111111
        dict_val['free66'] = 3.11111111111111111
        dict_val['free67'] = 3.11111111111111111
        dict_val['free68'] = 3.11111111111111111
        dict_val['free69'] = 3.11111111111111111
        dict_val['free70'] = 3.11111111111111111
        dict_val['free71'] = 3.11111111111111111
        dict_val['free72'] = 3.11111111111111111
        dict_val['free73'] = 3.11111111111111111
        dict_val['free74'] = 3.11111111111111111
        dict_val['free75'] = 3.11111111111111111
        dict_val['free76'] = 3.11111111111111111
        dict_val['free77'] = 3.11111111111111111
        dict_val['free78'] = 3.11111111111111111
        dict_val['free79'] = 3.11111111111111111
        dict_val['free80'] = 3.11111111111111111
        dict_val['free81'] = 3.11111111111111111
        dict_val['free82'] = 3.11111111111111111
        dict_val['free83'] = 3.11111111111111111
        dict_val['free84'] = 3.11111111111111111
        dict_val['free85'] = 3.11111111111111111
        dict_val['free86'] = 3.11111111111111111
        dict_val['free87'] = 3.11111111111111111
        dict_val['free88'] = 3.11111111111111111
        dict_val['free89'] = 3.11111111111111111
        dict_val['free90'] = 3.11111111111111111
        dict_val['free91'] = 3.11111111111111111
        dict_val['free92'] = 3.11111111111111111
        dict_val['free93'] = 3.11111111111111111
        dict_val['free94'] = 3.11111111111111111
        dict_val['free95'] = 3.11111111111111111
        dict_val['free96'] = 3.11111111111111111
        dict_val['free97'] = 3.11111111111111111
        dict_val['free98'] = 3.11111111111111111
        dict_val['free99'] = 3.11111111111111111
        dict_val['free100'] = 3.11111111111111111
        dict_val['free101'] = 3.11111111111111111
        dict_val['free102'] = 3.11111111111111111
        dict_val['free103'] = 3.11111111111111111
        dict_val['free104'] = 3.11111111111111111
        dict_val['free105'] = 3.11111111111111111
        dict_val['free106'] = 3.11111111111111111
        dict_val['free107'] = 3.11111111111111111
        dict_val['free108'] = 3.11111111111111111
        dict_val['free109'] = 3.11111111111111111
        dict_val['free110'] = 3.11111111111111111
        dict_val['free111'] = 3.11111111111111111
        dict_val['free112'] = 3.11111111111111111
        dict_val['free113'] = 3.11111111111111111
        dict_val['free114'] = 3.11111111111111111
        dict_val['free115'] = 3.11111111111111111
        dict_val['free116'] = 3.11111111111111111
        dict_val['free117'] = 3.11111111111111111
        dict_val['free118'] = 3.11111111111111111
        dict_val['free119'] = 3.11111111111111111
        dict_val['free120'] = 3.11111111111111111
        dict_val['free121'] = 3.11111111111111111
        dict_val['free122'] = 3.11111111111111111
        dict_val['free123'] = 3.11111111111111111
        dict_val['free124'] = 3.11111111111111111
        dict_val['free125'] = 3.11111111111111111
        dict_val['free126'] = 3.11111111111111111
        dict_val['free127'] = 3.11111111111111111
        dict_val['free128'] = 3.11111111111111111
        dict_val['free129'] = 3.11111111111111111
        dict_val['free130'] = 3.11111111111111111
        dict_val['free131'] = 3.11111111111111111
        dict_val['free132'] = 3.11111111111111111
        dict_val['free133'] = 3.11111111111111111
        dict_val['free134'] = 3.11111111111111111
        dict_val['free135'] = 3.11111111111111111
        dict_val['free136'] = 3.11111111111111111
        dict_val['free137'] = 3.11111111111111111
        dict_val['free138'] = 3.11111111111111111
        dict_val['free139'] = 3.11111111111111111
        dict_val['free140'] = 3.11111111111111111
        dict_val['free141'] = 3.11111111111111111
        dict_val['free142'] = 3.11111111111111111
        dict_val['free143'] = 3.11111111111111111
        dict_val['free144'] = 3.11111111111111111
        dict_val['free145'] = 3.11111111111111111
        dict_val['free146'] = 3.11111111111111111
        dict_val['free147'] = 3.11111111111111111
        dict_val['free148'] = 3.11111111111111111
        dict_val['free149'] = 3.11111111111111111
        dict_val['free150'] = 3.11111111111111111
        dict_val['free151'] = 3.11111111111111111
        dict_val['free152'] = 3.11111111111111111
        dict_val['free153'] = 3.11111111111111111
        dict_val['free154'] = 3.11111111111111111
        dict_val['free155'] = 3.11111111111111111
        dict_val['free156'] = 3.11111111111111111
        dict_val['free157'] = 3.11111111111111111
        dict_val['free158'] = 3.11111111111111111
        dict_val['free159'] = 3.11111111111111111
        dict_val['free160'] = 3.11111111111111111
        dict_val['free161'] = 3.11111111111111111
        dict_val['free162'] = 3.11111111111111111
        dict_val['free163'] = 3.11111111111111111
        dict_val['free164'] = 3.11111111111111111
        dict_val['free165'] = 3.11111111111111111
        dict_val['free166'] = 3.11111111111111111
        dict_val['free167'] = 3.11111111111111111
        dict_val['free168'] = 3.11111111111111111
        dict_val['free169'] = 3.11111111111111111
        dict_val['free170'] = 3.11111111111111111
        dict_val['free171'] = 3.11111111111111111
        dict_val['free172'] = 3.11111111111111111
        dict_val['free173'] = 3.11111111111111111
        dict_val['free174'] = 3.11111111111111111
        dict_val['free175'] = 3.11111111111111111
        dict_val['free176'] = 3.11111111111111111
        dict_val['free177'] = 3.11111111111111111
        dict_val['free178'] = 3.11111111111111111
        dict_val['free179'] = 3.11111111111111111
        dict_val['free180'] = 3.11111111111111111
        dict_val['free181'] = 3.11111111111111111
        dict_val['free182'] = 3.11111111111111111
        dict_val['free183'] = 3.11111111111111111
        dict_val['free184'] = 3.11111111111111111
        dict_val['free185'] = 3.11111111111111111
        dict_val['free186'] = 3.11111111111111111
        dict_val['free187'] = 3.11111111111111111
        dict_val['free188'] = 3.11111111111111111
        dict_val['free189'] = 3.11111111111111111
        dict_val['free190'] = 3.11111111111111111
        dict_val['free191'] = 3.11111111111111111
        dict_val['free192'] = 3.11111111111111111
        dict_val['free193'] = 3.11111111111111111
        dict_val['free194'] = 3.11111111111111111
        dict_val['free195'] = 3.11111111111111111
        dict_val['free196'] = 3.11111111111111111
        dict_val['free197'] = 3.11111111111111111
        dict_val['free198'] = 3.11111111111111111
        dict_val['free199'] = 3.11111111111111111
        dict_val['free200'] = 3.11111111111111111
        dict_val['free201'] = 3.11111111111111111
        dict_val['free202'] = 3.11111111111111111
        dict_val['free203'] = 3.11111111111111111
        dict_val['free204'] = 3.11111111111111111
        dict_val['free205'] = 3.11111111111111111
        dict_val['free206'] = 3.11111111111111111
        dict_val['free207'] = 3.11111111111111111
        dict_val['free208'] = 3.11111111111111111
        dict_val['free209'] = 3.11111111111111111
        dict_val['free210'] = 3.11111111111111111
        dict_val['free211'] = 3.11111111111111111
        dict_val['free212'] = 3.11111111111111111
        dict_val['free213'] = 3.11111111111111111
        dict_val['free214'] = 3.11111111111111111
        dict_val['free215'] = 3.11111111111111111
        dict_val['free216'] = 3.11111111111111111
        dict_val['free217'] = 3.11111111111111111
        dict_val['free218'] = 3.11111111111111111
        dict_val['free219'] = 3.11111111111111111
        dict_val['free220'] = 3.11111111111111111
        dict_val['free221'] = 3.11111111111111111
        dict_val['free222'] = 3.11111111111111111
        dict_val['free223'] = 3.11111111111111111
        dict_val['free224'] = 3.11111111111111111
        dict_val['free225'] = 3.11111111111111111
        dict_val['free226'] = 3.11111111111111111
        dict_val['free227'] = 3.11111111111111111
        dict_val['free228'] = 3.11111111111111111
        dict_val['free229'] = 3.11111111111111111
        dict_val['free230'] = 3.11111111111111111
        dict_val['free231'] = 3.11111111111111111
        dict_val['free232'] = 3.11111111111111111
        dict_val['free233'] = 3.11111111111111111
        dict_val['free234'] = 3.11111111111111111
        dict_val['free235'] = 3.11111111111111111
        dict_val['free236'] = 3.11111111111111111
        dict_val['free237'] = 3.11111111111111111
        dict_val['free238'] = 3.11111111111111111
        dict_val['free240'] = 3.11111111111111111
        dict_val['free241'] = 3.11111111111111111
        dict_val['free242'] = 3.11111111111111111
        dict_val['free243'] = 3.11111111111111111
        dict_val['free244'] = 3.11111111111111111
        dict_val['free245'] = 3.11111111111111111
        dict_val['free246'] = 3.11111111111111111
        dict_val['free247'] = 3.11111111111111111
        dict_val['free248'] = 3.11111111111111111
        dict_val['free249'] = 3.11111111111111111
        dict_val['free250'] = 3.11111111111111111
        dict_val['free251'] = 3.11111111111111111
        dict_val['free252'] = 3.11111111111111111
        dict_val['free253'] = 3.11111111111111111
        dict_val['free254'] = 3.11111111111111111
        dict_val['free255'] = 3.11111111111111111
        dict_val['free256'] = 3.11111111111111111
        dict_val['free257'] = 3.11111111111111111
        dict_val['free258'] = 3.11111111111111111
        dict_val['free259'] = 3.11111111111111111
        dict_val['free260'] = 3.11111111111111111
        dict_val['free260'] = 3.11111111111111111
        dict_val['free261'] = 3.11111111111111111
        dict_val['free262'] = 3.11111111111111111
        dict_val['free263'] = 3.11111111111111111
        dict_val['free264'] = 3.11111111111111111
        dict_val['free265'] = 3.11111111111111111
        dict_val['free266'] = 3.11111111111111111
        dict_val['free267'] = 3.11111111111111111
        dict_val['free268'] = 3.11111111111111111
        dict_val['free269'] = 3.11111111111111111
        dict_val['free270'] = 3.11111111111111111
        dict_val['free271'] = 3.11111111111111111
        dict_val['free272'] = 3.11111111111111111
        dict_val['free273'] = 3.11111111111111111
        dict_val['free274'] = 3.11111111111111111
        dict_val['free275'] = 3.11111111111111111
        dict_val['free277'] = 3.11111111111111111
        dict_val['free278'] = 3.11111111111111111
        dict_val['free279'] = 3.11111111111111111
        dict_val['free280'] = 3.11111111111111111
        dict_val['free281'] = 3.11111111111111111
        dict_val['free282'] = 3.11111111111111111
        dict_val['free283'] = 3.11111111111111111
        dict_val['free284'] = 3.11111111111111111
        dict_val['free285'] = 3.11111111111111111
        dict_val['free286'] = 3.11111111111111111
        dict_val['free287'] = 3.11111111111111111
        dict_val['free288'] = 3.11111111111111111
        dict_val['free289'] = 3.11111111111111111
        dict_val['free290'] = 3.11111111111111111
        '''
        data_collect.append(dict_val)
    return data_collect


class Step1:

    def log_catch(self, upload_speed):
        """
        Collect info from cellphone and write on mongoDB
        time collection: 10 mins
        :return: excel with log data
        """

        self.UDP_IP = ""
        self.UDP_PORT = 2055
        self.sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        self.data, self.addr = self.sock.recvfrom(1024)
        self.acc = ""
        self.mag = ""
        self.gyr = ""
        self.acquir_data = ""
        self.acq_list = [[], [], [], [], []]
        self.time_diff = 68
        self.flag_time = 0
        self.acquir_data = Fusion()
        x = threading.Thread(target=threading_sensor, args=(self.sock,
                                                            self.flag_time,
                                                            self.acquir_data,
                                                            self.acq_list,
                                                            self.time_diff,
                                                            upload_speed
                                                            ))
        x.start()
        temp = datetime.now()
        old_len = 0
        while x.is_alive():
            new = datetime.now()
            diff = float((new - temp).total_seconds())
            if diff > 3:
                temp = datetime.now()
                buf = len(self.acq_list[0])
                data_transfer = prepare_json(self.acq_list, old_len, buf)
                test_conn = MongoConn()
                test_conn.mongodb_conn('reahbilitation_db_test',
                                       'diff_collection_25kbps',
                                       'mongodb://ec2-3-14-14-152.us-east-2.compute.amazonaws.com:27017/test')
                test_conn.insert_data_many(data_transfer)
                old_len = buf
            print('-----------------------')
            print(new)
            print(temp)
            print("Time {}".format(diff))
            print(len(self.acq_list[0]))
            print('-----------------------')
            #time.sleep(0.05)

    def log_collect(self):
        """

        :return:
        """
        test_conn = MongoConn()
        test_conn.mongodb_conn('reahbilitation_db_test',
                               'diff_collection_25kbps',
                               'mongodb://ec2-3-14-14-152.us-east-2.compute.amazonaws.com:27017/test')
        list_collect = test_conn.collect_data_sensor()
        with open(
                '/Users/raphacgil/Documents/Raphael/Mestrado/git/reahbilitation_remote_game/logs/diff_sensor_25kbps_basic_upload_3s_10%.csv',
                'w') as csvfile:
            csvfile.write("{},{},{},{}".format('server_time',
                                               'server_time_unix',
                                               'sensor_time',
                                               'sensor_time_unix'))
            csvfile.write('\n')
            for cont, val in enumerate(list_collect[0]):
                csvfile.write("{},{},{},{}".format(str(val),
                                                   str(list_collect[1][cont]),
                                                   str(list_collect[2][cont]),
                                                   str(list_collect[3][cont])))
                csvfile.write('\n')

    def log_diff_time(self):
        """
        Collect info from cellphone and write on mongoDB
        time collection: 10 mins
        :return: excel with log data
        """

        self.UDP_IP = ""
        self.UDP_PORT = 2055
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        self.data, self.addr = self.sock.recvfrom(1024)
        self.acc = ""
        self.mag = ""
        self.gyr = ""
        self.acquir_data = ""
        self.acq_list = [[], [], [], [], []]
        self.flag_time = 0
        self.acquir_data = Fusion()

        x = threading.Thread(target=threading_sensor, args=(self.sock,
                                                            self.flag_time,
                                                            self.acquir_data,
                                                            self.acq_list,
                                                            ))
        x.start()


if __name__ == "__main__":
    #Step1().log_catch(25)
    Step1().log_collect()



