"""
subroutine to prepare json to be sent or read from mongodb
"""


class JsonPrepare:
    """
    Prepare Json to different scenario
    """

    def local_to_mongo(self, local_list):
        """
        :param local_list: All data stored in list to be prepared in json
        :return: return a list of json prepared
        """
        json_collect = {}
        json_collect['datetime'] = local_list[0]
        json_collect['datetime_int'] = local_list[1]
        json_collect['pitch'] = local_list[2]
        json_collect['pitch_median'] = local_list[3]
        json_collect['roll'] = local_list[4]
        json_collect['roll_median'] = local_list[5]
        json_collect['yam'] = local_list[6]
        json_collect['yam_median'] = local_list[7]
        json_collect['game_selection'] = local_list[8]
        json_collect['name_patient'] = local_list[9]
        json_collect['id_patient'] = local_list[10]

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


