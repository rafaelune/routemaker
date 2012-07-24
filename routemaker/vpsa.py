# -*- coding: latin-1 -*-

from geographics import PositionApi
import urllib3, json, locale, platform

class Pedido(object):
    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get data
    @property
    def data(self):
        return self.__data
    # set data
    @data.setter
    def data(self, data):
        self.__data = data
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
    # get terceiro
    @property
    def terceiro(self):
        return self.__terceiro
    # set terceiro
    @terceiro.setter
    def terceiro(self, terceiro):
        self.__terceiro = terceiro

class Terceiro(object):
    def __init__(self):
        self.__geolocated = False

    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get identificacao
    @property
    def identificacao(self):
        return self.__identificacao
    # set identificacao
    @identificacao.setter
    def identificacao(self, identificacao):
        self.__identificacao = identificacao
    # get nome
    @property
    def nome(self):
        return self.__nome
    # set nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome
    # get email
    @property
    def email(self):
        return self.__email
    # set email
    @email.setter
    def email(self, email):
        self.__email = email
     # get lat
    @property
    def lat(self):
        return self.__lat
    # set lat
    @lat.setter
    def lat(self, lat):
        self.__lat = lat
    # get lng
    @property
    def lng(self):
        return self.__lng
    # set lng
    @lng.setter
    def lng(self, lng):
        self.__lng = lng
    # get cidade
    @property
    def cidade(self):
        return self.__cidade
    # set cidade
    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade
    # get estado
    @property
    def estado(self):
        return self.__estado
    # set estado
    @estado.setter
    def estado(self, estado):
        self.__estado = estado
    # get bairro
    @property
    def bairro(self):
        return self.__bairro
    # set bairro
    @bairro.setter
    def bairro(self, bairro):
        self.__bairro = bairro
    # get pais
    @property
    def pais(self):
        return self.__pais
    # set pais
    @pais.setter
    def pais(self, pais):
        self.__pais = pais
    # get logradouro
    @property
    def logradouro(self):
        return self.__logradouro
    # set logradouro
    @logradouro.setter
    def logradouro(self, logradouro):
        self.__logradouro = logradouro
    # get geolocated
    @property
    def geolocated(self):
        return self.__geolocated
    # set geolocated
    @geolocated.setter
    def geolocated(self, geolocated):
        self.__geolocated = geolocated

    def set_geolocation(self, lat, lng):
        if lat != None and lng != None:
            self.__geolocated = True

        self.__lat = lat
        self.__lng = lng

    def get_full_address(self):
        return '{0}, {1}, {2}-{3}'.format(
            self.logradouro,
            self.bairro,
            self.cidade,
            self.estado
        )

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
        if platform.system() == 'Windows':
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')

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

    def get_terceiros(self, loads_location=False):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('vpsa') + 'terceiros/')
        terceiros_request = json.loads(request.data) # Parse JSON
        terceiros = []
        for iterator in terceiros_request:
            terceiro = Terceiro()
            terceiro.id = iterator['id']
            terceiro.identificacao = iterator['identificacao']
            terceiro.nome = iterator['nome']
            terceiro.email = iterator['email']
            
            if iterator['endereco'] != None:

                if iterator['endereco']['cidade'] != None:
                    terceiro.cidade = iterator['endereco']['cidade']
                else:
                    terceiro.cidade = ''
                
                if iterator['endereco']['logradouro'] != None:
                    terceiro.logradouro = iterator['endereco']['logradouro']
                else:
                    terceiro.logradouro = ''
                
                if iterator['endereco']['bairro'] != None:
                    terceiro.bairro = iterator['endereco']['bairro']
                else:
                    terceiro.bairro = ''
                
                if iterator['endereco']['pais'] != None:
                    terceiro.pais = iterator['endereco']['pais']
                else:
                    terceiro.pais = ''
                
                if iterator['endereco']['siglaEstado'] != None:
                    terceiro.estado = iterator['endereco']['siglaEstado']
                else:
                    terceiro.estado = ''
                
                if loads_location == True:
                    position_api = PositionApi()
                    location = position_api.get_location_by_address(terceiro.get_full_address())
                    if location != None:
                        terceiro.set_geolocation(location.lat, location.lng)

            terceiros.append(terceiro)
        return terceiros

    def get_terceiro(self, terceiro_id, loads_location=False):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('vpsa') + 'terceiros/' + str(terceiro_id))
        terceiros_request = json.loads(request.data) # Parse JSON
        terceiro = Terceiro()
        terceiro.id = terceiros_request['id']
        terceiro.identificacao = terceiros_request['identificacao']
        terceiro.nome = terceiros_request['nome']
        terceiro.email = terceiros_request['email']
        
        if terceiros_request['endereco'] != None:
            terceiro.cidade = terceiros_request['endereco']['cidade']
            terceiro.logradouro = terceiros_request['endereco']['logradouro']
            terceiro.bairro = terceiros_request['endereco']['bairro']
            terceiro.pais = terceiros_request['endereco']['pais']
            terceiro.estado = terceiros_request['endereco']['siglaEstado']
            
            if loads_location == True:
                position_api = PositionApi()
                location = position_api.get_location_by_address(terceiro.get_full_address())
                if location != None:
                    terceiro.set_geolocation(location.lat, location.lng)
        
        return terceiro

    def __get_terceiro(self, terceiros, terceiro_id):
        for item in terceiros:
            if item.id == terceiro_id:
                return item
        return None

    def get_pedido(self, entidade_id, pedido_id, loads_location=False):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('estoque') + str(entidade_id) + '/pedidos/' + str(pedido_id))
        pedido_request = json.loads(request.data) # Parse JSON
        pedido = Pedido()
        pedido.id = pedido_request['id']
        pedido.data = pedido_request['data']
        pedido.numero = pedido_request['numero']
        if platform.system() == 'Windows':
            pedido.valor_total = locale.currency(float(pedido_request['valorTotal']), grouping=True)
        else:
            pedido.valor_total = 'R$' + str(pedido_request['valorTotal'])
        pedido.plano_pagamento = pedido_request['planoPagamento']
        pedido.representante = pedido_request['representante']
        pedido.terceiro = self.get_terceiro(pedido_request['idTerceiroCliente'], loads_location)
        return pedido

    def get_pedidos(self, entidade_id, loads_location=False):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('estoque') + str(entidade_id) + '/pedidos/')
        pedidos_request = json.loads(request.data) # Parse JSON
        pedidos = []
        entidades = self.get_terceiros(loads_location)
        for iterator in pedidos_request:
            pedido = Pedido()
            pedido.id = iterator['id']
            pedido.data = iterator['data']
            pedido.numero = iterator['numero']
            if platform.system() == 'Windows':
                pedido.valor_total = locale.currency(float(iterator['valorTotal']), grouping=True)
            else:
                pedido.valor_total = 'R$'+ str(iterator['valorTotal'])
            pedido.plano_pagamento = iterator['planoPagamento']
            pedido.representante = iterator['representante']
            pedido.terceiro = self.__get_terceiro(entidades, iterator['idTerceiroCliente'])
            pedidos.append(pedido)
        return pedidos