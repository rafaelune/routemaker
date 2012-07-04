# -*- coding: latin-1 -*-

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from models import UserProfile
from forms import UserProfileSignupForm
from vpsa import VpsaApi

class VpsaApiTestCase(TestCase):
    def test_valid_database(self):
        """
        Testa se o database informado a 
        API VPSA é valida.
        """
        vpsa = VpsaApi('showroom')
        self.assertEqual(vpsa.get_base_url_api(), 'https://www.vpsa.com.br/vpsa/rest/externo/showroom/')
        self.assertTrue(vpsa.is_valid_database())

    def test_invalid_database(self):
        """
        Testa se o database informado a 
        API VPSA é valida.
        """
        vpsa = VpsaApi('base_exemplo')
        self.assertFalse(vpsa.is_valid_database())

    def test_retorno_entidades(self):
        """
        Testa o retorno de entidades.
        """
        vpsa = VpsaApi('showroom')
        self.assertTrue(len(vpsa.get_entidades()) > 0)

class UserProfileSignupFormTestCase(TestCase):
    def setUp(self):
        user = User(username="demo", password="123456")
        user.is_staff = False
        user.is_superuser = False
        user.save()
        self.demo = UserProfile.objects.create(user=user, database="showroom")

    def test_invalid_form_when_username_lower_than_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': 'de',
            'password': 'teste', 
            'password_confirm': 'teste', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_invalid_form_when_username_already_taken(self):
        signup_form = UserProfileSignupForm({
            'username': 'demo',
            'password': 'teste', 
            'password_confirm': 'teste', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_invalid_form_when_username_contains_special_characters(self):
        signup_form = UserProfileSignupForm({
            'username': 'demonstração#$%',
            'password': 'teste', 
            'password_confirm': 'teste', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_password_menor_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': 'usuario1',
            'password': '12', 
            'password_confirm': '654321', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_password_confirm_menor_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': 'usuario1',
            'password': '123456', 
            'password_confirm': '65', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())
        
    def test_formulario_invalido_quando_senhas_nao_coincidirem(self):
        signup_form = UserProfileSignupForm({
            'username': 'usuario1',
            'password': '123456', 
            'password_confirm': '654321', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_database_ja_cadastrado(self):
        signup_form = UserProfileSignupForm({
            'username': 'usuario1',
            'password': '123456', 
            'password_confirm': '654321', 
            'database': 'showroom'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_valido(self):
        signup_form = UserProfileSignupForm({
            'username': 'usuario1',
            'password': '123456', 
            'password_confirm': '123456', 
            'database': 'base_exemplo'
        })
        self.assertTrue(signup_form.is_valid())

class ControllerTestCase(TestCase):
    def test_http200_get_home(self):
        """
        Testa o retorno da homepage.
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_http200_get_cadastro(self):
        """
        Testa o retorno de uma pagina
        na url '/cadastro/'.
        """
        client = Client()
        response = client.get('/cadastro/')
        self.assertEqual(response.status_code, 200)

    def test_http200_post_cadastro(self):
        """
        Testa o POST do form de cadastro
        para a url '/cadastro/'.
        """
        client = Client(enforce_csrf_checks=True)
        response = client.post('/cadastro/', {
            'username': 'usuario1',
            'password': '123456', 
            'password_confirm': '654321', 
            'database': 'showroom'
        })

    def test_http200_get_login(self):
        """
        Testa o retorno de uma pagina
        na url '/login/'.
        """
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)