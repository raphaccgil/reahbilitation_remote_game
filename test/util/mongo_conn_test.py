"""
Test mongoDB configuration
"""

from src.util.mongo_conn import MongoConn
import pytest
from datetime import datetime

class TestMongoConn:
    """
    Test mongo class
    """
    def mongo_conn_test(self):

        flag = MongoConn().mongodb_conn('reahbilitation_db',
                     'sensor_coll',
                     'mongodb://localhost:27017/')
        assert flag == 0

    def mongo_create_index_sensor_test(self):
        val = MongoConn()
        val.mongodb_conn('reahbilitation_db_test',
                     'sensor_coll',
                     'mongodb://localhost:27017/')
        val2 = MongoConn()
        flag = val.mongo_create_index_sensor()

        assert flag == 0

    def insert_data_test(self):

        print("Ola test")
        test_conn =  MongoConn()
        test_conn.mongodb_conn('reahbilitation_db_test',
                     'sensor_coll',
                     'mongodb://localhost:27017/')

        values = {}
        values['datetime'] = datetime.now()
        values['datetime_int'] = datetime.now()
        values['pitch'] = 3.11111111111111111
        values['median_pitch'] = 3.11111111111111111
        values['roll'] = 3.11111111111111111
        values['median_roll'] = 3.11111111111111111
        values['yam'] = 3.11111111111111111
        values['free1'] = 3.11111111111111111
        values['free2'] = 3.11111111111111111
        values['free3'] = 3.11111111111111111
        values['free4'] = 3.11111111111111111
        values['free5'] = 3.11111111111111111
        values['free6'] = 3.11111111111111111
        values['free7'] = 3.11111111111111111
        values['free8'] = 3.11111111111111111
        values['free9'] = 3.11111111111111111
        values['free10'] = 3.11111111111111111
        values['free11'] = 3.11111111111111111
        values['free12'] = 3.11111111111111111
        values['free13'] = 3.11111111111111111
        values['free14'] = 3.11111111111111111
        values['free15'] = 3.11111111111111111
        values['free16'] = 3.11111111111111111
        values['free17'] = 3.11111111111111111
        values['free18'] = 3.11111111111111111
        values['free19'] = 3.11111111111111111
        values['free20'] = 3.11111111111111111
        values['free21'] = 3.11111111111111111
        values['free22'] = 3.11111111111111111
        values['free23'] = 3.11111111111111111
        values['free24'] = 3.11111111111111111
        values['free25'] = 3.11111111111111111
        values['free26'] = 3.11111111111111111
        values['free27'] = 3.11111111111111111
        values['free28'] = 3.11111111111111111
        values['free29'] = 3.11111111111111111
        values['free30'] = 3.11111111111111111
        values['free31'] = 3.11111111111111111
        values['free32'] = 3.11111111111111111
        values['free33'] = 3.11111111111111111
        values['free34'] = 3.11111111111111111
        values['free35'] = 3.11111111111111111
        values['free36'] = 3.11111111111111111
        values['free37'] = 3.11111111111111111
        values['free38'] = 3.11111111111111111
        values['free39'] = 3.11111111111111111
        values['free40'] = 3.11111111111111111
        values['free41'] = 3.11111111111111111
        values['free42'] = 3.11111111111111111
        values['free43'] = 3.11111111111111111
        values['free44'] = 3.11111111111111111
        values['free45'] = 3.11111111111111111
        values['free46'] = 3.11111111111111111
        values['free47'] = 3.11111111111111111
        values['free48'] = 3.11111111111111111
        values['free49'] = 3.11111111111111111
        values['free50'] = 3.11111111111111111
        values['free51'] = 3.11111111111111111
        values['free52'] = 3.11111111111111111
        values['free53'] = 3.11111111111111111
        values['free54'] = 3.11111111111111111
        values['free55'] = 3.11111111111111111
        values['free56'] = 3.11111111111111111
        values['free57'] = 3.11111111111111111
        values['free58'] = 3.11111111111111111
        values['free59'] = 3.11111111111111111
        values['free60'] = 3.11111111111111111
        values['free61'] = 3.11111111111111111
        values['free62'] = 3.11111111111111111
        values['free63'] = 3.11111111111111111
        values['free64'] = 3.11111111111111111
        values['free65'] = 3.11111111111111111
        values['free66'] = 3.11111111111111111
        values['free67'] = 3.11111111111111111
        values['free68'] = 3.11111111111111111
        values['free69'] = 3.11111111111111111
        values['free70'] = 3.11111111111111111
        values['free71'] = 3.11111111111111111
        values['free72'] = 3.11111111111111111
        values['free73'] = 3.11111111111111111
        values['free74'] = 3.11111111111111111
        values['free75'] = 3.11111111111111111
        values['free76'] = 3.11111111111111111
        values['free77'] = 3.11111111111111111
        values['free78'] = 3.11111111111111111
        values['free79'] = 3.11111111111111111
        values['free80'] = 3.11111111111111111
        values['free81'] = 3.11111111111111111
        values['free82'] = 3.11111111111111111
        values['free83'] = 3.11111111111111111
        values['free84'] = 3.11111111111111111
        values['free85'] = 3.11111111111111111
        values['free86'] = 3.11111111111111111
        values['free87'] = 3.11111111111111111
        values['free88'] = 3.11111111111111111
        values['free89'] = 3.11111111111111111
        values['free90'] = 3.11111111111111111
        values['free91'] = 3.11111111111111111
        values['free92'] = 3.11111111111111111
        values['free93'] = 3.11111111111111111
        values['free94'] = 3.11111111111111111
        values['free95'] = 3.11111111111111111
        values['free96'] = 3.11111111111111111
        values['free97'] = 3.11111111111111111
        values['free98'] = 3.11111111111111111
        values['free99'] = 3.11111111111111111
        values['free100'] = 3.11111111111111111
        values['free101'] = 3.11111111111111111
        values['free102'] = 3.11111111111111111
        values['free103'] = 3.11111111111111111
        values['free104'] = 3.11111111111111111
        values['free105'] = 3.11111111111111111
        values['free106'] = 3.11111111111111111
        values['free107'] = 3.11111111111111111
        values['free108'] = 3.11111111111111111
        values['free109'] = 3.11111111111111111
        values['free110'] = 3.11111111111111111
        values['free111'] = 3.11111111111111111
        values['free112'] = 3.11111111111111111
        values['free113'] = 3.11111111111111111
        values['free114'] = 3.11111111111111111
        values['free115'] = 3.11111111111111111
        values['free116'] = 3.11111111111111111
        values['free117'] = 3.11111111111111111
        values['free118'] = 3.11111111111111111
        values['free119'] = 3.11111111111111111
        values['free120'] = 3.11111111111111111
        values['free121'] = 3.11111111111111111
        values['free122'] = 3.11111111111111111
        values['free123'] = 3.11111111111111111
        values['free124'] = 3.11111111111111111
        values['free125'] = 3.11111111111111111
        values['free126'] = 3.11111111111111111
        values['free127'] = 3.11111111111111111
        values['free128'] = 3.11111111111111111
        values['free129'] = 3.11111111111111111
        values['free130'] = 3.11111111111111111
        values['free131'] = 3.11111111111111111
        values['free132'] = 3.11111111111111111
        values['free133'] = 3.11111111111111111
        values['free134'] = 3.11111111111111111
        values['free135'] = 3.11111111111111111
        values['free136'] = 3.11111111111111111
        values['free137'] = 3.11111111111111111
        values['free138'] = 3.11111111111111111
        values['free139'] = 3.11111111111111111
        values['free140'] = 3.11111111111111111
        values['free141'] = 3.11111111111111111
        values['free142'] = 3.11111111111111111
        values['free143'] = 3.11111111111111111
        values['free144'] = 3.11111111111111111
        values['free145'] = 3.11111111111111111
        values['free146'] = 3.11111111111111111
        values['free147'] = 3.11111111111111111
        values['free148'] = 3.11111111111111111
        values['free149'] = 3.11111111111111111
        values['free150'] = 3.11111111111111111
        values['free151'] = 3.11111111111111111
        values['free152'] = 3.11111111111111111
        values['free153'] = 3.11111111111111111
        values['free154'] = 3.11111111111111111
        values['free155'] = 3.11111111111111111
        values['free156'] = 3.11111111111111111
        values['free157'] = 3.11111111111111111
        values['free158'] = 3.11111111111111111
        values['free159'] = 3.11111111111111111
        values['free160'] = 3.11111111111111111
        values['free161'] = 3.11111111111111111
        values['free162'] = 3.11111111111111111
        values['free163'] = 3.11111111111111111
        values['free164'] = 3.11111111111111111
        values['free165'] = 3.11111111111111111
        values['free166'] = 3.11111111111111111
        values['free167'] = 3.11111111111111111
        values['free168'] = 3.11111111111111111
        values['free169'] = 3.11111111111111111
        values['free170'] = 3.11111111111111111
        values['free171'] = 3.11111111111111111
        values['free172'] = 3.11111111111111111
        values['free173'] = 3.11111111111111111
        values['free174'] = 3.11111111111111111
        values['free175'] = 3.11111111111111111
        values['free176'] = 3.11111111111111111
        values['free177'] = 3.11111111111111111
        values['free178'] = 3.11111111111111111
        values['free179'] = 3.11111111111111111
        values['free180'] = 3.11111111111111111
        values['free181'] = 3.11111111111111111
        values['free182'] = 3.11111111111111111
        values['free183'] = 3.11111111111111111
        values['free184'] = 3.11111111111111111
        values['free185'] = 3.11111111111111111
        values['free186'] = 3.11111111111111111
        values['free187'] = 3.11111111111111111
        values['free188'] = 3.11111111111111111
        values['free189'] = 3.11111111111111111
        values['free190'] = 3.11111111111111111
        values['free191'] = 3.11111111111111111
        values['free192'] = 3.11111111111111111
        values['free193'] = 3.11111111111111111
        values['free194'] = 3.11111111111111111
        values['free195'] = 3.11111111111111111
        values['free196'] = 3.11111111111111111
        values['free197'] = 3.11111111111111111
        values['free198'] = 3.11111111111111111
        values['free199'] = 3.11111111111111111
        values['free200'] = 3.11111111111111111
        values['free201'] = 3.11111111111111111
        values['free202'] = 3.11111111111111111
        values['free203'] = 3.11111111111111111
        values['free204'] = 3.11111111111111111
        values['free205'] = 3.11111111111111111
        values['free206'] = 3.11111111111111111
        values['free207'] = 3.11111111111111111
        values['free208'] = 3.11111111111111111
        values['free209'] = 3.11111111111111111
        values['free210'] = 3.11111111111111111
        values['free211'] = 3.11111111111111111
        values['free212'] = 3.11111111111111111
        values['free213'] = 3.11111111111111111
        values['free214'] = 3.11111111111111111
        values['free215'] = 3.11111111111111111
        values['free216'] = 3.11111111111111111
        values['free217'] = 3.11111111111111111
        values['free218'] = 3.11111111111111111
        values['free219'] = 3.11111111111111111
        values['free220'] = 3.11111111111111111
        values['free221'] = 3.11111111111111111
        values['free222'] = 3.11111111111111111
        values['free223'] = 3.11111111111111111
        values['free224'] = 3.11111111111111111
        values['free225'] = 3.11111111111111111
        values['free226'] = 3.11111111111111111
        values['free227'] = 3.11111111111111111
        values['free228'] = 3.11111111111111111
        values['free229'] = 3.11111111111111111
        values['free230'] = 3.11111111111111111
        values['free231'] = 3.11111111111111111
        values['free232'] = 3.11111111111111111
        values['free233'] = 3.11111111111111111
        values['free234'] = 3.11111111111111111
        values['free235'] = 3.11111111111111111
        values['free236'] = 3.11111111111111111
        values['free237'] = 3.11111111111111111
        values['free238'] = 3.11111111111111111
        values['free240'] = 3.11111111111111111
        values['free241'] = 3.11111111111111111
        values['free242'] = 3.11111111111111111
        values['free243'] = 3.11111111111111111
        values['free244'] = 3.11111111111111111
        values['free245'] = 3.11111111111111111
        values['free246'] = 3.11111111111111111
        values['free247'] = 3.11111111111111111
        values['free248'] = 3.11111111111111111
        values['free249'] = 3.11111111111111111
        values['free250'] = 3.11111111111111111
        values['free251'] = 3.11111111111111111
        values['free252'] = 3.11111111111111111
        values['free253'] = 3.11111111111111111
        values['free254'] = 3.11111111111111111
        values['free255'] = 3.11111111111111111
        values['free256'] = 3.11111111111111111
        values['free257'] = 3.11111111111111111
        values['free258'] = 3.11111111111111111
        values['free259'] = 3.11111111111111111
        values['free260'] = 3.11111111111111111
        values['free260'] = 3.11111111111111111
        values['free261'] = 3.11111111111111111
        values['free262'] = 3.11111111111111111
        values['free263'] = 3.11111111111111111
        values['free264'] = 3.11111111111111111
        values['free265'] = 3.11111111111111111
        values['free266'] = 3.11111111111111111
        values['free267'] = 3.11111111111111111
        values['free268'] = 3.11111111111111111
        values['free269'] = 3.11111111111111111
        values['free270'] = 3.11111111111111111
        values['free271'] = 3.11111111111111111
        values['free272'] = 3.11111111111111111
        values['free273'] = 3.11111111111111111
        values['free274'] = 3.11111111111111111
        values['free275'] = 3.11111111111111111
        values['free277'] = 3.11111111111111111
        values['free278'] = 3.11111111111111111
        values['free279'] = 3.11111111111111111
        values['free280'] = 3.11111111111111111
        values['free281'] = 3.11111111111111111
        values['free282'] = 3.11111111111111111
        values['free283'] = 3.11111111111111111
        values['free284'] = 3.11111111111111111
        values['free285'] = 3.11111111111111111
        values['free286'] = 3.11111111111111111
        values['free287'] = 3.11111111111111111
        values['free288'] = 3.11111111111111111
        values['free289'] = 3.11111111111111111
        values['free290'] = 3.11111111111111111



        values['game_selection'] = 'Game1'
        values['name_patient'] = 'Carlos'
        values['id_patient'] = 1001

        flag = test_conn.insert_data(values)

        assert flag == 0

    def insert_data_many_test(self):

        print("Ola test")
        test_conn =  MongoConn()
        test_conn.mongodb_conn('reahbilitation_db_test',
                     'sensor_coll',
                     'mongodb://localhost:27017/')

        values = {}
        values['datetime'] = datetime.now()
        values['pitch'] = 3.11111111111111111
        values['median_pitch'] = 3.11111111111111111
        values['roll'] = 3.11111111111111111
        values['median_roll'] = 3.11111111111111111
        values['yam'] = 3.11111111111111111
        values['median_yam'] = 3.11111111111111111
        values['game_selection'] = 'Game1'
        values['name_patient'] = 'Carlos'
        values['id_patient'] = 1001

        values_all = []

        values_all.append(values)
        flag = test_conn.insert_data_many(values_all)

        assert flag == 0

    def collect_partial_doctor_test(self):
        """
        Check on mongoDB if has a doctor message
        :return: Return collect data
        """
        test_conn = MongoConn()
        test_conn.mongodb_conn('reahbilitation_db',
                               'doctor_coll',
                               'mongodb://localhost:27017/')

        values = {}
        values['datetime'] = datetime.now()
        values['doctor_message'] = 'Nova Mensagem'
        test_conn.insert_data(values)

        test_conn = MongoConn()
        test_conn.mongodb_conn('reahbilitation_db',
                               'doctor_coll',
                               'mongodb://localhost:27017/')

        flag = test_conn.collect_partial_doctor()
        assert flag == 'Nova Mensagem'

if __name__ == "__main__":
    TestMongoConn().insert_data_test()