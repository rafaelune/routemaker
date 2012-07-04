# -*- coding: latin-1 -*-

import urllib3, json

class Entidade(object):
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome
    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get nome
    @property
    def nome(self):
        return self.__nome
    # set nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

class VpsaApi(object):
    def __init__(self, database):
        self.__base_url_api = ('https://www.vpsa.com.br/vpsa/rest/externo/%s/' % database)

    def get_base_url_api(self):
        return self.__base_url_api

    def is_valid_database(self):
        http = urllib3.PoolManager()
        request = http.request('GET', self.__base_url_api + 'entidades/')
        return request.status == 200

    def get_entidades(self):
        http = urllib3.PoolManager()
        request = http.request('GET', self.__base_url_api + 'entidades/')
        entidades_request = json.loads(request.data) # Parse JSON
        entidades = []
        for iterator in entidades_request:
            entidade = Entidade(id = iterator['id'], nome = iterator['nome'])
            entidades.append(entidade)
        return entidades