import django_filters

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet

from collection.models import Artist, Artwork, Genre, Style


class ArtworkFilterSet(FacetedFilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Artwork
        fields = ["author","date","style", "period", "genre"]

    def configure_facets(self):
        self.filters["style"].facet = Facet()
        self.filters["period"].facet = Facet()
        self.filters["genre"].facet = Facet()

    def filter_search(self, queryset, name, value):
        vector = (
            search.SearchVector("title", weight="A")
            + search.SearchVector("author__name", weight="B")
            + search.SearchVector("style__name", weight="B")
            + search.SearchVector("period__name", weight="B")
            + search.SearchVector("genre__name", weight="C")
        )
        query = search.SearchQuery(value, search_type="websearch")
        return (
            queryset.annotate(
                search=vector,
                rank=search.SearchRank(vector, query),
            )
            .filter(search=query)
            .order_by("-rank")
        )
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # print()