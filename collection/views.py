from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from collection.models import Artwork

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/')

    else:
        f = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': f})


def index(request):
    artworks = Artwork.objects.all()[:10]


    return render(request, 'collection/index.html', {'artworks': artworks})
