import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.functions.functions import search_multiple_fields
from .models import Country, State, City
from .serializers import (
    CountrySerializer,
    CountryWithDetailSerializer,
    StateSerializer,
    StateWithDetailSerializer,
    CitySerializer,
    CityWithDetailSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.prefetch_related('states').all()

    @action(detail=False, methods=['post'])
    def create_multiple_countries(self, request):
        from .services import create_multiple_countries
        countries = json.loads(request.POST.get('countries'))
        create_multiple_countries(
            countries=countries
        )
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_multiple_states_by_country(self, request, pk=None):
        from .services import create_multiple_states
        states = json.loads(request.POST.get('states'))
        create_multiple_states(
            states=states
        )
        self.serializer_class = CountryWithDetailSerializer

    @action(detail=False, methods=['post'])
    def create_multiple_states(self, request):
        from .services import create_multiple_states
        states = json.loads(request.POST.get('states'))
        create_multiple_states(
            states=states
        )
        return Response({'result': 'Se han creado los Departamentos/Estados con éxito'})

    @action(detail=False, methods=['post'])
    def create_multiple_cities(self, request):
        from .services import create_multiple_cities
        cities = json.loads(request.POST.get('cities'))
        create_multiple_cities(
            cities=cities
        )
        return Response({'result': 'Se han creado las ciudades con éxito'})

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CountryWithDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class StateViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.select_related('country').all()

    @action(detail=True, methods=['post'])
    def create_multiple_cities(self, request, pk=None):
        from .services import create_multiple_cities
        cities = json.loads(request.POST.get('cities'))
        create_multiple_cities(
            cities=cities
        )
        self.serializer_class = StateWithDetailSerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = StateWithDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CityWithDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        name = request.GET.get('name')
        qs = None
        search_fields = ['state__country__iso3', 'state__country__name', 'state__name', 'name']
        self.serializer_class = CityWithDetailSerializer

        if len(name) > 2:
            qs = search_multiple_fields(self.queryset.select_related('state', 'state__country'), search_fields, name)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
