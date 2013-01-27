# -*- coding: latin-1 -*-

from django import forms
from routemaker.vpsaapi import *
import re

class FilterPedidoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        token_acesso = kwargs.pop('token')
        super(FilterPedidoForm, self).__init__(*args, **kwargs)
        
        vpsa_api2 = VpsaApi2()
        self.fields['entidade'].choices = [(ent.id, ent.nome) for ent in vpsa_api2.get_entidades(token_acesso)]
    
    entidade = forms.ChoiceField(choices=())