# -*- coding: latin-1 -*-

from django import forms
from django.contrib.auth.models import User
from models import UserProfile
from vpsa import VpsaApi
import re

class FilterPedidoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        database = kwargs.pop('database')
        super(FilterPedidoForm, self).__init__(*args, **kwargs)
        vpsa = VpsaApi(database)
        self.fields['entidade'].choices = [(ent.id, ent.nome) for ent in vpsa.get_entidades()]
    
    entidade = forms.ChoiceField(choices=())

class UserProfileLoginForm(forms.Form):
    username = forms.RegexField(label='Nome de usuário', required=True,
        regex=r'^[a-zA-Z0-9_.-]+$', error_messages={'invalid': 'Apenas caracteres, dígitos, "_", "-" e ".".'}
    )
    password = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput(render_value=False))
    
    
class UserProfileSignupForm(forms.Form):
    username = forms.RegexField(label='Nome de usuário', max_length=50, min_length=3, required=True,
        regex=r'^[a-zA-Z0-9_.-]+$', error_messages={'invalid': 'Apenas caracteres, dígitos, "_", "-" e ".".'}
    )
    password = forms.CharField(label='Senha', max_length=50, min_length=6, required=True, widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Confirmar senha', max_length=50, min_length=6, required=True,widget=forms.PasswordInput(render_value=False))
    database = forms.CharField(label='Banco de dados', max_length=256, required=True)

    def clean_username(self):
        """Clean username validation to check if an username is
        valid and was not taken."""        
        if User.objects.filter(
            username=self.cleaned_data['username'],
        ).count():
            raise forms.ValidationError(
                'Nome de usuário "%s" já cadastrado.' % self.cleaned_data['username']
            )
        return self.cleaned_data['username']

    def clean_password_confirm(self):
        if self.cleaned_data['password_confirm'] != self.data['password']:
            raise forms.ValidationError(
                'Senhas não conferem.'
            )
        return self.cleaned_data['password_confirm']

    def clean_database(self):
        vpsa_api = VpsaApi(self.cleaned_data['database'])
        if not vpsa_api.is_valid_database():
            forms.ValidationError('Banco de dados "%s" não está disponível.' % self.cleaned_data['database'])
        return self.cleaned_data['database']

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data