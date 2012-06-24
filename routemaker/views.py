# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.conf import settings
from forms import UserProfileSignupForm
from models import UserProfile

def index(request):
    return render_to_response('home.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

def cadastro(request):
    if request.method == 'POST':
        form = UserProfileSignupForm(request.POST)
        if form.is_valid(): # Se o form é válido
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save() # Salva o user
            UserProfile.objects.create(user=user, database=form.cleaned_data['database']) # Cria um profile para o user
            messages.success(request, 'Conta criada com sucesso!') # Add mensagem de sucesso
            return HttpResponseRedirect('/login/')
    else:
        form = UserProfileSignupForm() # Form vazio
    
    return render_to_response('signup.html', 
        locals(), 
        context_instance=RequestContext(request)
    )

def login(request):
    return render_to_response('login.html',
        locals(),
        context_instance=RequestContext(request)
    )