# -*- coding: latin-1 -*-

import urllib3, json

class Pedido(object):
    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get numero
    @property
    def numero(self):
        return self.__numero
    # set numero
    @numero.setter
    def numero(self, numero):
        self.__numero = numero
    # get valor_total
    @property
    def valor_total(self):
        return self.__valor_total
    # set valor_total
    @valor_total.setter
    def valor_total(self, valor_total):
        self.__valor_total = valor_total
    # get plano_pagamento
    @property
    def plano_pagamento(self):
        return self.__plano_pagamento
    # set plano_pagamento
    @plano_pagamento.setter
    def plano_pagamento(self, plano_pagamento):
        self.__plano_pagamento = plano_pagamento
    # get representante
    @property
    def representante(self):
        return self.__representante
    # set representante
    @representante.setter
    def representante(self, representante):
        self.__representante = representante
    # get terceiro_id
    @property
    def terceiro_id(self):
        return self.__terceiro_id
    # set terceiro_id
    @terceiro_id.setter
    def terceiro_id(self, terceiro_id):
        self.__terceiro_id = terceiro_id

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
        self.__database = database
        self.__base_url_api = 'https://www.vpsa.com.br/{0}/rest/externo/{1}/'

    def get_base_url_api(self, module):
        return self.__base_url_api.format(module, self.__database)

    def is_valid_database(self):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('vpsa') + 'entidades/')
        return request.status == 200

    def get_entidades(self):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('vpsa') + 'entidades/')
        entidades_request = json.loads(request.data) # Parse JSON
        entidades = []
        for iterator in entidades_request:
            entidade = Entidade(id = iterator['id'], nome = iterator['nome'])
            entidades.append(entidade)
        return entidades

    def get_pedidos(self, entidade_id):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('estoque') + str(entidade_id) + '/pedidos/')
        pedidos_request = json.loads(request.data) # Parse JSON
        pedidos = []
        for iterator in pedidos_request:
            pedido = Pedido()
            pedido.id = iterator['id']
            pedido.numero = iterator['numero']
            pedido.valor_total = iterator['valorTotal']
            pedido.plano_pagamento = iterator['planoPagamento']
            pedido.representante = iterator['representante']
            pedido.terceiro_id = iterator['idTerceiroCliente']
            pedidos.append(pedido)
        return pedidos