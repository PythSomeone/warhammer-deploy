from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.template import loader
from django import forms
from formtools.wizard.views import SessionWizardView

from .forms import RegisterForm
from .forms import LoginForm

from firebase_admin import auth
import pyrebase


from helper.models import Character
from helper import authe
from helper.services.handler import Handler

class CreatorWizard(SessionWizardView):
    primaryStatistics = {}
    secondaryStatistics = {}
    race = ''
    def get_context_data(self, **kwargs):
        context = super(CreatorWizard, self).get_context_data(**kwargs)
        if self.race:
            self.primaryStatistics['primaryStats'] = Handler.get_merged_primary(self.race)
            self.secondaryStatistics['secondaryStats'] = Handler.get_merged_secondary(self.race, self.primaryStatistics['primaryStats'])
            context.update(self.primaryStatistics)
            context.update(self.secondaryStatistics)
        return context

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            self.race = self.get_cleaned_data_for_step('0')['race']
            step0_form_field = self.get_cleaned_data_for_step('0')['race']
            kwargs.update({'race': step0_form_field})
        return kwargs
        if step == '2':
            step0_form_field = self.get_cleaned_data_for_step('0')['race']
            kwargs.update({'race': step0_form_field})
        
        return kwargs 


    def render_template(self, request, form, previous_fields, step, context=None):
        if step == 1:
            race = request.POST.get('0-race')
            form.fields['professions'] = forms.ChoiceField(widget=RadioSelect(), choices = [])
            form.fields['professions'].choices = [Handler.get_all_allowed_professions(Handler.get_data('Professions'), race)]
        return super(CreatorWizard, self).render_template(request, form, previous_fields, step, context)

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        data['primary_statistics'] = self.primaryStatistics['primaryStats']
        data['secondary_statistics'] = self.secondaryStatistics['secondaryStats']
        try:
            data['userUID'] = self.request.session['uid']
        except:
            pass
        data.update(Handler.get_inventory(form_list[1].cleaned_data['profession']))
        Handler.push_data(data,'character')
        messages.info(self.request, 'Character with name '+ data['name']+' has been created!')
        return redirect('/helper/template')
    

def get_all_fields_from_form(instance):

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)

    return fields

def redirect_view(request):
    response = redirect("/redirect-success/")
    return response

def home(request):
    if Handler.user_exists(request):
        email = 'Welcome, '+ request.session['email']
    else:
        email = ""

    return render(request,"helper/Home.html", {'email': email})

def index(response):
    return HttpResponse("<h1>Warhammer-helper!</h1>")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = auth.create_user(email = email , password = password)
            messages.info(request, 'Welcome, '+email+' to the Warhammer world!')
            return redirect('/helper/home')
    else:
        form = RegisterForm()

    return render(request, 'helper/register.html', {'form': form})

def login(request):
    if Handler.user_exists(request):
        messages.info(request, 'You are already logged in')
        return redirect('/helper/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = authe.sign_in_with_email_and_password(email = email , password = password)
                messages.info(request, 'Successfully logged in!')
                print(user['email'] + " logged in")
                Handler.session_handler(request, user)
                return redirect('/helper/home')
            except:
                messages.info(request, 'Invalid email or password!')
                form = LoginForm()
    else:
        form = LoginForm()

    return render(request, 'helper/login.html', {'form': form})


def logout(request):
    try:
        del request.session['uid']
        del request.session['email']
        messages.info(request, 'Successfully logged out!')
    except KeyError:
        pass

    return render(request, 'helper/Home.html')

def profile(request):
    if not Handler.user_exists(request):
        messages.info(request, 'Please log in to see your characters')
        return redirect('/helper/home')
    user_characters = Handler.get_data_by_uid(request, 'character')
    obj = [] 
    if user_characters:
        for entity in user_characters:
            character = Character(**entity)
            obj.append(character)

    return render(request, 'helper/profile.html', {'obj': obj})

def characters(request):
    user_characters = Handler.get_data('character')
    obj = [] 
    if user_characters:
        for entity in user_characters:
            character = Character(**entity)
            obj.append(character)

    return render(request, 'helper/characters.html', {'obj': obj})

def lore(request):
    professions = Handler.get_data('professions')
    races = Handler.get_data('races')

    return render(request, 'helper/lore.html', {'races': races, 'professions':professions})

def character_delete(request, name, userUID):

    if request.method == 'POST':       
        Handler.delete_character('Character', name, userUID)
        return redirect('/helper/profile')

    return render(request, 'helper/profile.html', {'obj': obj})
