# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from models import UserProfile
from forms import UserProfileSignupForm

class UserTestCase(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class UserProfileSignupFormTestCase(TestCase):
    def setUp(self):
        user = User(username="demo", password="123456")
        user.is_staff = False
        user.is_superuser = False
        user.save()
        self.demo = UserProfile.objects.create(user=user, database="showroom")

    def test_formulario_invalido_quando_username_menor_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': u'de',
            'password': u'teste', 
            'password_confirm': u'teste', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())
        
    def test_formulario_invalido_quando_username_ja_cadastrado(self):
        signup_form = UserProfileSignupForm({
            'username': u'demo',
            'password': u'teste', 
            'password_confirm': u'teste', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_password_menor_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': u'usuario1',
            'password': u'12', 
            'password_confirm': u'654321', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_password_confirm_menor_min_length(self):
        signup_form = UserProfileSignupForm({
            'username': u'usuario1',
            'password': u'123456', 
            'password_confirm': u'65', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())
        
    def test_formulario_invalido_quando_senhas_nao_coincidirem(self):
        signup_form = UserProfileSignupForm({
            'username': u'usuario1',
            'password': u'123456', 
            'password_confirm': u'654321', 
            'database': 'teste'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_invalido_quando_database_ja_cadastrado(self):
        signup_form = UserProfileSignupForm({
            'username': u'usuario1',
            'password': u'123456', 
            'password_confirm': u'654321', 
            'database': 'showroom'
        })
        self.assertFalse(signup_form.is_valid())

    def test_formulario_valido(self):
        signup_form = UserProfileSignupForm({
            'username': u'usuario1',
            'password': u'123456', 
            'password_confirm': u'123456', 
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
            'username': u'usuario1',
            'password': u'123456', 
            'password_confirm': u'654321', 
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