from django.db import models
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class Character(models.Model):
    name = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    weapon = models.CharField(max_length=30)
    equipment = models.CharField(max_length=30)
    armor = models.CharField(max_length=30)
    age = models.IntegerField()
    eye_colour = models.CharField(max_length=30)
    hair_colour = models.CharField(max_length=30)
    star_sign = models.CharField(max_length=30)
    sex = models.CharField(max_length=30)
    weight = models.IntegerField()
    origin = models.CharField(max_length=30)
    userUID = models.CharField(max_length=30, default="0")
    primary_statistics = models.IntegerField(blank=True, null=True)
    secondary_statistics = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.name
    

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Character._meta.fields]

   