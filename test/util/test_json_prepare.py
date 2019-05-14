"""
Routine to test json preparation
"""

import pytest
from src.util.json_prepare import JsonPrepare


class TestJsonPrepare:


    def test_local_to_mongo(self):
        """

        :assert: Verify if its ok the dict expectation
        """

        list_val = [[], [], [], [], [], [], []]
        list_val[0].append(0)
        list_val[1].append(0)
        list_val[2].append(0)
        list_val[3].append(0)
        list_val[4].append(0)
        list_val[5].append(0)
        list_val[6].append(0)

        json_expect = {}
        json_expect['time_coll'] = 0
        json_expect['pitch'] = 0
        json_expect['pitch_median'] = 0
        json_expect['roll'] = 0
        json_expect['roll_median'] = 0
        json_expect['yam'] = 0
        json_expect['yam_median'] = 0

        dict_return = JsonPrepare().local_to_mongo(list_val)
        assert dict_return == json_expect

    def test_message_doctor1(self):
        """
        :assert: Verify if receives no internnet connection
        """
        conn_active = 0
        text_val = "Test de leitura"
        dict_test = {}
        dict_test['message'] = text_val
        val_return = JsonPrepare().message_doctor(conn_active, dict_test)
        assert val_return == "No internet connection - No doctor message"

    def test_message_doctor2(self):
        """
        python test1 on doctor message
        """

        conn_active = 1
        text_val = "Test de leitura"
        dict_test = {}
        dict_test['message'] = text_val
        val_return = JsonPrepare().message_doctor(conn_active, dict_test)
        assert val_return == text_val