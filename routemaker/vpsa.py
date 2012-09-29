# -*- coding: latin-1 -*-

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib3, urllib2, urllib, json, locale, platform, httplib

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

class TokenAcesso(object):
    # get access_token
    @property
    def access_token(self):
        return self.__access_token
    # set access_token
    @access_token.setter
    def access_token(self, access_token):
        self.__access_token = access_token

    # get expires_in
    @property
    def expires_in(self):
        return self.__expires_in
    # set expires_in
    @expires_in.setter
    def expires_in(self, expires_in):
        self.__expires_in = expires_in

    # get refresh_token
    @property
    def refresh_token(self):
        return self.__refresh_token
    # set refresh_token
    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self.__refresh_token = refresh_token

    # get cnpj_empresa
    @property
    def cnpj_empresa(self):
        return self.__cnpj_empresa
    # set cnpj_empresa
    @cnpj_empresa.setter
    def cnpj_empresa(self, cnpj_empresa):
        self.__cnpj_empresa = cnpj_empresa

    # get terceiro_id
    @property
    def terceiro_id(self):
        return self.__terceiro_id
    # set terceiro_id
    @terceiro_id.setter
    def terceiro_id(self, terceiro_id):
        self.__terceiro_id = terceiro_id

    # get terceiro_nome
    @property
    def terceiro_nome(self):
        return self.__terceiro_nome
    # set terceiro_nome
    @terceiro_nome.setter
    def terceiro_nome(self, terceiro_nome):
        self.__terceiro_nome = terceiro_nome

class VpsaApi2(object):
    def __init__(self):
        current_site = Site.objects.get_current()
        domain_site = current_site.domain
        callback_url = reverse('callback', args=None)

        self.__app__id = getattr(settings, 'VPSA_APP_ID')
        self.__app__secret = getattr(settings, 'VPSA_APP_SECRET')
        self.__redirect__uri = domain_site + callback_url
        self.__oauth__url = 'https://www.vpsa.com.br/apps/oauth/authorization?response_type=code&app_id={0}&redirect_uri={1}'
        self.__entidades__url = 'https://www.vpsa.com.br/apps/api/entidades'
        self.__pedidos__url = 'https://www.vpsa.com.br/apps/api/pedidos/'
        self.__terceiro__url = 'https://www.vpsa.com.br/apps/api/terceiros/'

    def get_oauth_url(self):
        return self.__oauth__url.format(self.__app__id, self.__redirect__uri)

    def get_token_accesso(self, auth_code):
        body_fields = {
            'grant_type': 'authorization_code',
            'app_id': self.__app__id,
            'app_secret': self.__app__secret,
            'redirect_uri': self.__redirect__uri,
            'code': auth_code
        }

        headers = {
            'Content-Type': 'application/json'
        }

        request = urllib2.Request('https://www.vpsa.com.br/apps/oauth/token', json.dumps(body_fields))
        request.add_header('Content-Type', 'application/json')

        token_acesso = None
        try:
            response = urllib2.urlopen(request)
            response_data = json.loads(response.read())
            print response_data
            
            token_acesso = TokenAcesso()
            token_acesso.access_token = response_data['access_token']
            token_acesso.expires_in = response_data['expires_in']
            token_acesso.refresh_token = response_data['refresh_token']
            token_acesso.terceiro_id = response_data['id_terceiro']
            token_acesso.terceiro_nome = response_data['nome_terceiro']
            token_acesso.cnpj_empresa = response_data['cnpj_empresa']
        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return token_acesso

    def __request__data(self, url, token, entidades=None):
        url += '?token=' + token

        if entidades != None:
            url += '&entidades=' + entidades

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return json.loads(response.read())

    def is_token_valid(self, token_acesso):
        entidades = self.get_entidades(token_acesso)
        return (entidades != None and len(entidades) > 0)

    def get_entidades(self, token_acesso):
        lista_entidades = []
        response_data = None

        try:
            response_data = self.__request__data(self.__entidades__url, token_acesso.access_token)
            if response_data == None:
                response_data = self.__request__data(self.__entidades__url, token_acesso.refresh_token)

            for iterator in response_data:
                entidade = Entidade(id = iterator['id'], nome = iterator['nome'])
                lista_entidades.append(entidade)

        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return lista_entidades

    def get_terceiro(self, token_acesso, terceiro_id):
        terceiro = None
        response_data = None

        print 'requisicao get_terceiro inicio'

        try:
            response_data = self.__request__data(self.__terceiro__url + str(terceiro_id), token_acesso.access_token)
            if response_data == None:
                response_data = self.__request__data(self.__terceiro__url + str(terceiro_id), token_acesso.refresh_token)

            terceiro = Terceiro()
            terceiro.id = response_data['id']
            terceiro.nome = response_data['nome']
            terceiro.identificacao = response_data['identificacao']
            
            terceiro.email = response_data['emails'][0]
            
            if response_data['enderecos'] != None:
                terceiro.cidade = response_data['enderecos'][0]['cidade']
                terceiro.logradouro = response_data['enderecos'][0]['logradouro']
                terceiro.bairro = response_data['enderecos'][0]['bairro']
                terceiro.estado = response_data['enderecos'][0]['siglaEstado']

            print 'requisicao get_terceiro fim'

        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return terceiro

    def get_pedido(self, token_acesso, pedido_id):
        response_data = None
        pedido = None
        print pedido_id
        print self.__pedidos__url + str(pedido_id)
        try:
            response_data = self.__request__data(self.__pedidos__url + str(pedido_id), token_acesso.access_token)
            if response_data == None:
                response_data = self.__request__data(self.__pedidos__url + str(pedido_id), token_acesso.refresh_token)

            pedido = Pedido()
            pedido.id = response_data['id']
            pedido.data = response_data['data']
            pedido.numero = response_data['numero']
            # not working on heroku
            #pedido.valor_total = locale.currency(float(iterator['valorTotal']), grouping=True)
            pedido.valor_total = 'R$'+ str(response_data['valorTotal'])
            pedido.plano_pagamento = response_data['planoPagamento']
            #pedido.representante = iterator['representante']
            pedido.terceiro = self.get_terceiro(token_acesso, response_data['idTerceiroCliente'])
        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return pedido
        
    def get_pedidos(self, token_acesso, entidade_id):
        lista_pedidos = []
        response_data = None

        contador = 1
        print 'requisicao get_pedidos inicio'
        try:
            response_data = self.__request__data(
                self.__pedidos__url, 
                token_acesso.access_token,
                entidades=entidade_id
                )
            if response_data == None:
                response_data = self.__request__data(
                    self.__pedidos__url, 
                    token_acesso.refresh_token,
                    entidades=entidade_id
                    )

            for iterator in response_data:
                print 'pedido: ' + str(contador)
                contador = contador + 1
                
                pedido = Pedido()

                pedido.id = iterator['id']
                pedido.data = iterator['data']
                pedido.numero = iterator['numero']
                # not working on heroku
                #pedido.valor_total = locale.currency(float(iterator['valorTotal']), grouping=True)
                pedido.valor_total = 'R$'+ str(iterator['valorTotal'])
                pedido.plano_pagamento = iterator['planoPagamento']
                #pedido.representante = iterator['representante']
                pedido.terceiro = self.get_terceiro(token_acesso, iterator['idTerceiroCliente'])
                lista_pedidos.append(pedido)

            print 'requisicao get_pedidos fim'
        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return lista_pedidos