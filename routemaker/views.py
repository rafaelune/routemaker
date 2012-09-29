# -*- coding: latin-1 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth.models import User
from forms import FilterPedidoForm
from models import UserProfile
from vpsa import VpsaApi2
import jsonpickle, urllib3

def index(request):
    # redirects user if authenticated
    if request.session.has_key('token'):
        token_acesso = request.session['token']

        vpsa_api2 = VpsaApi2()
        if vpsa_api2.is_token_valid(token_acesso):
            return HttpResponseRedirect('/home/')
        else:
            del request.session['token']

    return render_to_response('index.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

def signup(request):
    vpsa_api2 = VpsaApi2()
    oauth_url = vpsa_api2.get_oauth_url()
    return HttpResponseRedirect(oauth_url)

def oauth_callback(request):
    auth_code = request.GET.get('code')
    vpsa_api2 = VpsaApi2()
    token_acesso = vpsa_api2.get_token_accesso(auth_code)

    if request.session.has_key('token'):
        del request.session['token']

    request.session['token'] = token_acesso

    return HttpResponseRedirect('/home/')

def log_in(request):
    vpsa_api2 = VpsaApi2()
    oauth_url = vpsa_api2.get_oauth_url()
    return HttpResponseRedirect(oauth_url)

def log_out(request):
    if request.session.has_key('token'):
        del request.session['token']

    return HttpResponseRedirect('/')

def home(request):
    is_authenticated = request.session.has_key('token')
    if is_authenticated:
        token_acesso = request.session['token']

        cnpj_empresa = token_acesso.cnpj_empresa
        nome_terceiro = token_acesso.terceiro_nome

        vpsa_api2 = VpsaApi2()
        vpsa_api2.get_entidades(token_acesso)

        form = FilterPedidoForm(token=token_acesso)

        return render_to_response('home.html', 
            locals(), 
            context_instance=RequestContext(request)
        )

    return HttpResponseRedirect('/')

def pedidos_search(request):
    if request.session.has_key('token') and request.method == 'POST':
        token_acesso = request.session['token']
        entidade = request.POST.get('entidade')

        vpsa_api2 = VpsaApi2()
        pedidos = vpsa_api2.get_pedidos(token_acesso, entidade)
        return render_to_response('ajax/filter-result.html', 
            locals(), 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/')

def pedidos_json(request):
    pedidos_json = []

    if request.session.has_key('token') and request.method == 'GET':
        pedidos_ids = request.GET.get('pedidos[]')
        token_acesso = request.session['token']
        vpsa_api2 = VpsaApi2()

        if pedidos_ids != None:
            array_pedidos_id = pedidos_ids.split(',')
    
            for pedido_id in array_pedidos_id:
                pedido = vpsa_api2.get_pedido(token_acesso, pedido_id)
                pedidos_json.append(pedido)



    retorno = jsonpickle.encode(pedidos_json)
    return HttpResponse(retorno, mimetype="text/javascript")