# -*- coding: latin-1 -*-

import urllib3

class VpsaApi(object):
    def __init__(self, database):
        self.__base_url_api = ('https://www.vpsa.com.br/vpsa/rest/externo/%s/' % database)

    def get_base_url_api(self):
        return self.__base_url_api

    def is_valid_database(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.__base_url_api + 'entidades/')
        return r.status == 200