# -*- coding: latin-1 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from forms import FilterPedidoForm, UserProfileSignupForm, UserProfileLoginForm
from models import UserProfile
from vpsa import VpsaApi
import jsonpickle, urllib3

def index(request):
    user = request.user
    if user is not None and user.is_authenticated():
        return HttpResponseRedirect('/home/')
    
    request.user = None
    return render_to_response('index.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

def signup(request):
    if request.method == 'POST':
        form = UserProfileSignupForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.set_password(form.cleaned_data['password'])
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            UserProfile.objects.create(user=user, database=form.cleaned_data['database']) # Cria um profile para o user
            messages.success(request, 'Conta criada com sucesso!') # Add mensagem de sucesso
            return HttpResponseRedirect('/login/')
    else:
        form = UserProfileSignupForm() # Form vazio
    
    return render_to_response('signup.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

def log_in(request):
    if request.method == 'POST':
        form = UserProfileLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    messages.add_message(request, messages.WARNING, 'Sua conta está inativa, apenas usuários ativos podem acessar.')
                    messages.warning(request, 'Sua conta está inativa, apenas usuários ativos podem acessar.')
            else:
                messages.warning(request, 'Usuário não encontrado. Verifique seu nome de usuário e senha.')
    else:
        form = UserProfileLoginForm() # Form vazio
    
    return render_to_response('login.html',
        locals(),
        context_instance=RequestContext(request)
    )

@login_required(login_url='/')
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def home(request):
    user = request.user
    user_profile = request.user.get_profile()
    
    vpsa = VpsaApi(user_profile.database)
    form = FilterPedidoForm(database=user_profile.database)
    
    return render_to_response('home.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

@login_required(login_url='/')
def pedidos_search(request):
    user = request.user
    user_profile = request.user.get_profile()
    vpsa = VpsaApi(user_profile.database)
    
    if request.method == 'POST':
        entidade = request.POST.get('entidade')
        
        pedidos = vpsa.get_pedidos(entidade)
        
        return render_to_response('ajax/filter-result.html', 
            locals(), 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/')
def pedidos_json(request):
    user = request.user
    user_profile = request.user.get_profile()
    vpsa = VpsaApi(user_profile.database)
    
    pedidos_json = []
    if request.method == 'GET':
        entidade_id = request.GET.get('entidade')
        pedidos_ids = request.GET.get('pedidos[]')

        if entidade_id != None and pedidos_ids != None:
            array_pedidos_id = pedidos_ids.split(',')

            for pedido_id in array_pedidos_id:
                pedido = vpsa.get_pedido(entidade_id, pedido_id, True)
                pedidos_json.append(pedido)

    retorno = jsonpickle.encode(pedidos_json)
    return HttpResponse(retorno, mimetype="text/javascript")