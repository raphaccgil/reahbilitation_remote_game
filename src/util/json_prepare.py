"""
subroutine to prepare json to be sent or read from mongodb
"""


class JsonPrepare:


    def local_to_mongo(self, local_list):
        """
        :param local_list: All data stored in list to be prepared in json
        :return: return a list of json prepared
        """
        json_collect = []
        for cont, val in enumerate(local_list[0]):
            json_collect.append({})
            json_collect[-1]['time_coll'] = local_list[0][cont]
            json_collect[-1]['pitch'] = local_list[1][cont]
            json_collect[-1]['pitch_median'] = local_list[2][cont]
            json_collect[-1]['roll'] = local_list[3][cont]
            json_collect[-1]['roll_median'] = local_list[4][cont]
            json_collect[-1]['yam'] = local_list[5][cont]
            json_collect[-1]['yam_median'] = local_list[6][cont]

        return json_collect

    def message_doctor(self, remote_info, conn_status):
        """
        :param remote_info: Return remote info
        :return: return a list of json prepared
        """
        if conn_status == 1:
            info_doctor = remote_info['message']
        else:
            info_doctor = "No internet connection - No doctor message"

        return info_doctor
