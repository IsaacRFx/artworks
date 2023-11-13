from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from collection.forms import SignUpForm
#import Listview
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from collection.filters import ArtworkFilterSet
from django.db.models import Count

from collection.models import Artwork

def register(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/')

    else:
        f = SignUpForm()

    return render(request, 'registration/registration_form.html', {'form': f})


def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')

    artworks = Artwork.objects.all()[:10]
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # print()


    return render(request, 'collection/index.html', {'artworks': artworks})


class ArtworkListView(ListView):
    model = Artwork
    paginate_by = 25
    ordering = "title"

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = ArtworkFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context