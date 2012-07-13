# -*- coding: latin-1 -*-

from geographics import PositionApi
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
    # get endereco
    @property
    def endereco(self):
        return self.__endereco
    # set endereco
    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

class Endereco(object):
    # get localizacao
    @property
    def localizacao(self):
        return self.__localizacao
    # set localizacao
    @localizacao.setter
    def localizacao(self, localizacao):
        self.__localizacao = localizacao
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

    def get_terceiros(self):
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
                endereco = Endereco()
                
                if iterator['endereco']['cidade'] != None:
                    endereco.cidade = iterator['endereco']['cidade']
                else:
                    endereco.cidade = ''
                
                if iterator['endereco']['logradouro'] != None:
                    endereco.logradouro = iterator['endereco']['logradouro']
                else:
                    endereco.logradouro = ''
                
                if iterator['endereco']['bairro'] != None:
                    endereco.bairro = iterator['endereco']['bairro']
                else:
                    endereco.bairro = ''
                
                if iterator['endereco']['pais'] != None:
                    endereco.pais = iterator['endereco']['pais']
                else:
                    endereco.pais = ''
                
                if iterator['endereco']['siglaEstado'] != None:
                    endereco.estado = iterator['endereco']['siglaEstado']
                else:
                    endereco.estado = ''
                
                position_api = PositionApi()
                location = position_api.get_location_by_address(endereco.get_full_address())
                endereco.localizacao = location
                
                terceiro.endereco = endereco
            
            terceiros.append(terceiro)
        return terceiros

    def get_terceiro(self, terceiro_id):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('vpsa') + 'terceiros/' + str(terceiro_id))
        terceiros_request = json.loads(request.data) # Parse JSON
        terceiro = Terceiro()
        terceiro.id = terceiros_request['id']
        terceiro.identificacao = terceiros_request['identificacao']
        terceiro.nome = terceiros_request['nome']
        terceiro.email = terceiros_request['email']
        
        endereco = Endereco()
        endereco.cidade = terceiros_request['endereco']['cidade']
        endereco.logradouro = terceiros_request['endereco']['logradouro']
        endereco.bairro = terceiros_request['endereco']['bairro']
        endereco.pais = terceiros_request['endereco']['pais']
        endereco.estado = terceiros_request['endereco']['siglaEstado']
        
        position_api = PositionApi()
        location = position_api.get_location_by_address(endereco.get_full_address())
        endereco.localizacao = location
        
        terceiro.endereco = endereco
        
        return terceiro

    def __get_terceiro(self, terceiros, terceiro_id):
        for item in terceiros:
            if item.id == terceiro_id:
                return item
        return None

    def get_pedido(self, entidade_id, pedido_id):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('estoque') + str(entidade_id) + '/pedidos/' + str(pedido_id))
        pedido_request = json.loads(request.data) # Parse JSON
        pedido = Pedido()
        pedido.id = pedido_request['id']
        pedido.data = pedido_request['data']
        pedido.numero = pedido_request['numero']
        pedido.valor_total = pedido_request['valorTotal']
        pedido.plano_pagamento = pedido_request['planoPagamento']
        pedido.representante = pedido_request['representante']
        pedido.terceiro = self.get_terceiro(pedido_request['idTerceiroCliente'])
        return pedido

    def get_pedidos(self, entidade_id):
        http = urllib3.PoolManager()
        request = http.request('GET', self.get_base_url_api('estoque') + str(entidade_id) + '/pedidos/')
        pedidos_request = json.loads(request.data) # Parse JSON
        pedidos = []
        entidades = self.get_entidades()
        for iterator in pedidos_request:
            pedido = Pedido()
            pedido.id = iterator['id']
            pedido.data = iterator['data']
            pedido.numero = iterator['numero']
            pedido.valor_total = iterator['valorTotal']
            pedido.plano_pagamento = iterator['planoPagamento']
            pedido.representante = iterator['representante']
            pedido.terceiro = self.__get_terceiro(entidades, iterator['idTerceiroCliente'])
            pedidos.append(pedido)
        return pedidos