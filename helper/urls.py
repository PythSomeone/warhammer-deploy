from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from . import views
from .views import redirect_view
from .views import CreatorWizard
from django.conf.urls.static import static
from .forms import CreatorForm1, CreatorForm2, CreatorForm3


app_name = 'helper'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('template/', CreatorWizard.as_view([CreatorForm1, CreatorForm2, CreatorForm3]), name='creator'),
    path('home/', views.home, name='Home'),
    path('profile/', views.profile, name='profile'),
    path('characters/', views.characters, name='characters'),
    path('lore/', views.lore, name='lore'),
    path('helper/', redirect_view),
    url(r'^delete/(?P<userUID>[\w\-]+)/(?P<name>[\w\-]+)/$', views.character_delete, name='character_delete')
]