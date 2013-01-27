# -*- coding: latin-1 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from routemaker.vpsaapi import *
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib3, urllib2, urllib, json, locale, platform, httplib

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

    def __request__data(self, url, token, entidades=None, date_from=None, date_to=None):
        url += '?token=' + token

        if entidades != None:
            url += '&entidades=' + entidades

        if date_from != None and date_to != None:
            url += '&desde=' + date_from + '&ate=' + date_to

        print url
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

        try:
            response_data = self.__request__data(self.__terceiro__url + str(terceiro_id), token_acesso.access_token)
            print response_data
            if response_data == None:
                response_data = self.__request__data(self.__terceiro__url + str(terceiro_id), token_acesso.refresh_token)

            terceiro = Terceiro()
            terceiro.id = response_data['id']
            terceiro.nome = response_data['nome']
            terceiro.identificacao = response_data['documento']
            
            terceiro.email = response_data['emails'][0]
            
            if response_data['enderecos'] != None:
                terceiro.cidade = response_data['enderecos'][0]['cidade']
                terceiro.logradouro = response_data['enderecos'][0]['logradouro']
                terceiro.bairro = response_data['enderecos'][0]['bairro']
                terceiro.estado = response_data['enderecos'][0]['siglaEstado']

        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return terceiro
        
    def get_pedidos(self, token_acesso, entidade_id=None):
        lista_pedidos = []
        response_data = None

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
            print response_data
            for iterator in response_data:
                pedido = Pedido()

                pedido.id = iterator['id']
                pedido.data = iterator['data']
                pedido.numero = iterator['numero']
                # not working on heroku
                #pedido.valor_total = locale.currency(float(iterator['valorTotal']), grouping=True)
                pedido.valor_total = 'R$'+ str(iterator['valorTotal'])
                pedido.plano_pagamento = iterator['planoPagamento']
                #pedido.representante = iterator['representante']
                pedido.terceiro_id = iterator['idTerceiroCliente']

                lista_pedidos.append(pedido)

            lista_pedidos[0].terceiro = self.get_terceiro(token_acesso, lista_pedidos[0].terceiro_id)
        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return lista_pedidos

    def get_pedidos_items(self, items):
        lista_items = []

        for item in items:
            pedido_item = PedidoItem()

            pedido_item.id_produto = item['idProduto']
            pedido_item.descricao = item['descricao']
            pedido_item.unidade = item['unidade']
            pedido_item.quantidade = item['quantidade']

            lista_items.append(pedido_item)

        return lista_items

    def get_pedidos_by_date(self, token_acesso, date_from, date_to):
        lista_pedidos = []
        response_data = None

        try:
            response_data = self.__request__data(
                self.__pedidos__url, 
                token_acesso.access_token,
                date_from=date_from,
                date_to=date_to
                )
            if response_data == None:
                response_data = self.__request__data(
                    self.__pedidos__url, 
                    token_acesso.refresh_token,
                    date_from=date_from,
                    date_to=date_to
                    )

            for iterator in response_data:
                pedido = Pedido()

                pedido.id = iterator['id']
                pedido.data = iterator['data']
                pedido.numero = iterator['numero']
                # not working on heroku
                #pedido.valor_total = locale.currency(float(iterator['valorTotal']), grouping=True)
                pedido.valor_total = 'R$'+ str(iterator['valorTotal'])
                pedido.plano_pagamento = iterator['planoPagamento']
                #pedido.representante = iterator['representante']
                pedido.terceiro_id = iterator['idTerceiroCliente']

                pedido.items = self.get_pedidos_items(iterator['itens'])

                lista_pedidos.append(pedido)
        except URLError, e:
            print e.read()
        else:
            pass
        finally:
            return lista_pedidos