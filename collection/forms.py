from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CollectionForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=80, required=True)
    description = forms.CharField(label="Descripción", required=True) # # # # # #