from django.test import TestCase
from helper.forms import LoginForm

class LoginTestCase(TestCase):
    def test_forms_success(self):
        form_data = {'email': 'name@mail.com', 'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_forms_email_failure(self):
        form_data = {'email': '', 'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_password_failure(self):
        form_data = {'email': 'name@mail.com', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())