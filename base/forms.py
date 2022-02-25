from dataclasses import fields
import imp
from operator import mod
from pyexpat import model
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm,TextInput


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','username','email','password1','password2']

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields="__all__"
        exclude=['host','participants']
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['name'].widget.attrs.update({'class': 'form-control'})
           self.fields['description'].widget.attrs.update({'class':'form-control'})
           self.fields['topic'].widget.attrs.update({'class':'form-control'})


class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['name','username','email','bio']
