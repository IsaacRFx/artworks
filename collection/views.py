from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from collection.forms import SignUpForm
#import Listview
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from collection.filters import ArtworkFilterSet
from django.db.models import Count
from collection.forms import CollectionForm
from collection.models import Collection
from django.shortcuts import redirect

from collection.models import Artwork

def register(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            f.save() #
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

    collections = Collection.objects.filter(owner=request.user)
    artworks = Artwork.objects.all()[:50]


    return render(request, 'collection/index.html', {'artworks': artworks, 'collections': collections})


class ArtworkListView(ListView):
    model = Artwork
    paginate_by = 25
    ordering = "title"
    

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = ArtworkFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        collection = Collection.objects.filter(owner=self.request.user) #
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        context["collections"] = collection # #
        return context

def collections(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'collection/collections.html',
                  {'collections': collections})


def collection_list(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'collection/collection_list.html',
                  {'collections': collections})


def collection_add(request):
    form = None
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            collection = Collection(
                    name=name,
                    description=description,
                    owner=request.user)
            collection.save()
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'listChanged'})

    return render(request,
                  'collection/collection_form.html',
                  {'form': form})

def collection_edit(request, name):
    # edit the collection using update method
    form = None
    collection = Collection.objects.get(name=name)
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection.name = form.cleaned_data['name']
            collection.description = form.cleaned_data['description']
            collection.save()
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'listChanged'})
    return render(request,
                    'collection/collection_edit.html',
                    {'form': form, 'name': name})

def collection_artwork_add(request, artwork_id, collection_id):
    # add the artwork to the collection
    collection = Collection.objects.get(id=collection_id)
    artwork = Artwork.objects.get(id=artwork_id)
    collection.artworks.add(artwork)
    return redirect('/collections')

def artwork(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    return render(request, 'collection/artwork.html',
                  {'artwork': artwork})
 
