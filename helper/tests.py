from django.test import TestCase
from django.urls import reverse_lazy

from helper.forms import LoginForm
from helper.models import Character
from helper.views import lore

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
        
class CharacterTest(TestCase):

    def create_character(self, 
                        name = "123",
                        race = "123",
                        profession = "123",
                        weapon = "123",
                        equipment = "123",
                        armor = "123",
                        age = 123,
                        eye_colour = "123",
                        hair_colour = "123",
                        star_sign = "123",
                        sex = "123",
                        weight = 123,
                        origin = "123",
                        userUID = "123",
                        primary_statistics = 123,
                        secondary_statistics = 123
        ):
        return Character.objects.create(name = name,
                        race = race,
                        profession = profession,
                        weapon = weapon,
                        equipment = equipment,
                        armor = armor,
                        age = age,
                        eye_colour = eye_colour,
                        hair_colour = hair_colour,
                        star_sign = star_sign,
                        sex = sex,
                        weight = weight,
                        origin = origin,
                        userUID = userUID,
)

    def test_character_creation(self):
        test = self.create_character()
        self.assertTrue(isinstance(test, Character))
        self.assertEqual(test.__str__(), test.name)

class ViewTest(TestCase):

    def test_home_view(self):
        response = self.client.post('/helper/home', follow=True)
        self.assertTemplateUsed(response, 'helper/Home.html')
        self.assertEqual(response.status_code, 200)

    def test_lore_view(self):
        response = self.client.post('/helper/lore/', follow=True)
        self.assertTemplateUsed(response, 'helper/lore.html')
        self.assertEqual(response.status_code, 200)
    
    def test_register_view(self):
        response = self.client.post('/helper/register/', follow=True)
        self.assertTemplateUsed(response, 'helper/register.html')
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):
        response = self.client.post('/helper/login/', follow=True)
        self.assertTemplateUsed(response, 'helper/login.html')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.post('/helper/logout/', follow=True)
        self.assertTemplateUsed(response, 'helper/Home.html')
        self.assertEqual(response.status_code, 200)


