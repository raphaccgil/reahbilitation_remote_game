"""
Verify if has internet connection
"""

import urllib3


class CheckConn:

    def internet_on(self):
        """
        Check with Google server if internet is available
        :return: Status of Internet Connection
        """

        http = urllib3.PoolManager()
        try:
            http.request('GET',
                         'http://216.58.192.142',
                         timeout=5)
            return True
        except:
            return False
