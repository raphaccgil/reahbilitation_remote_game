from src.util.check_conn_quality import CheckConnQuality


class CheckConnQualityTest:


    def internet_quality_test(self):
        """
        :param last_time:
        :param : Difference between last verification and actual (ms)
        :return: Return mesure of couting value
        """
        list_values = CheckConnQuality().internet_quality()
        assert len(list_values) == 3


if __name__ == '__main__':
    CheckConnQualityTest().internet_quality_test()