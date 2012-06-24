# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from models import UserProfile

class UserProfileSignupForm(forms.Form):
    username = forms.CharField(label=u'Nome de usuário', max_length=50, min_length=3, required=True)
    password = forms.CharField(label='Senha', max_length=50, min_length=6, required=True,widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Confirmar senha', max_length=50, min_length=6, required=True,widget=forms.PasswordInput(render_value=False))
    database = forms.CharField(label='Banco de dados', max_length=256, required=True)

    def clean_username(self):
        "Clean username validation, to check if an username is already in use."
        if User.objects.filter(
            username=self.cleaned_data['username'],
        ).count():
            raise forms.ValidationError(
                u'Nome de usuário "%s" já cadastrado.' % self.cleaned_data['username']
            )
        return self.cleaned_data['username']

    def clean_password_confirm(self):
        if self.cleaned_data['password_confirm'] != self.data['password']:
            raise forms.ValidationError(
                u'Senhas não conferem.'
            )
        return self.cleaned_data['password_confirm']

    def clean_database(self):
        try:
            user = UserProfile.objects.get(database=self.cleaned_data['database'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data['database']
        raise forms.ValidationError(u'Banco de dados "%s" já cadastrado.' % self.cleaned_data['database'])

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data