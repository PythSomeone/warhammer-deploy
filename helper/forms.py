from django import forms
from django.forms import ModelForm
from helper.models import Character
import json

from firebase_admin import db

from helper.services.handler import Handler

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class CreatorForm(ModelForm):
    """
    def __init__(self, *args, userUID):
        super(CreatorForm, self).__init__(*args)
        self.userUID = userUID
    """
    class Meta:
        model = Character
        fields = '__all__'
        widgets = {
            'profession': forms.Select(choices=Handler.get_data_in_list('Professions')),
            'race': forms.Select(choices=Handler.get_data_in_list('Races')),
            'sex': forms.Select(choices=Handler.get_data_in_list('Sex')),
            'star_sign': forms.Select(choices=Handler.get_data_in_list('Starsigns')),
            'userUID' : forms.HiddenInput(),
            #'keyid' : forms.HiddenInput()
            #'date' : forms.HiddenInput()
        }

class CreatorForm1(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ('profession', 'weapon', 'equipment',)
        widgets = {
            'race': forms.Select(choices=Handler.get_data_in_list('Races')),
            'star_sign': forms.Select(choices=Handler.get_data_in_list('Starsigns')),
            'userUID' : forms.HiddenInput(),
            'primary_statistics' : forms.HiddenInput(),
            'secondary_statistics' : forms.HiddenInput(),
            #'keyid' : forms.HiddenInput()
            #'date' : forms.HiddenInput()
        }

class CreatorForm2(forms.Form):
    """
    def __init__(self, *args, **kwargs):
        race = kwargs.pop('race')
        print(race)
        super(CreatorForm2, self).__init__(*args, **kwargs)
        self.fields['professions'] = forms.ChoiceField(widget=RadioSelect(), choices=[Handler.get_all_allowed_professions(Handler.get_data('Professions'), race)])
    """
    def __init__(self, race, *args, **kwargs):
        super(CreatorForm2, self).__init__(*args, **kwargs)
        self.fields['profession'] = forms.ChoiceField(widget=forms.RadioSelect(), choices=Handler.get_all_allowed_professions(Handler.get_data('Professions'), race))

class CreatorForm3(forms.Form):
    """
    def __init__(self, *args, **kwargs):
        race = kwargs.pop('race')
        print(race)
        super(CreatorForm2, self).__init__(*args, **kwargs)
        self.fields['professions'] = forms.ChoiceField(widget=RadioSelect(), choices=[Handler.get_all_allowed_professions(Handler.get_data('Professions'), race)])
    """
    def __init__(self, *args, **kwargs):
        super(CreatorForm3, self).__init__(*args, **kwargs)
        


"""
    class Meta:
        model = Character
        fields = ('profession',)
        widgets = {
            #'profession': forms.Select(choices=Handler.get_all_allowed_professions(Handler.get_data('Professions'), race)),
            #'keyid' : forms.HiddenInput()
            #'date' : forms.HiddenInput()
        }
"""