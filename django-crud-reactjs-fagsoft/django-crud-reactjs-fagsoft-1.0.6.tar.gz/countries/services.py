from .models import State, City, Country


def create_multiple_countries(
        countries
):
    countries_to_create = []
    for kwards in countries:
        country = Country()
        for field in kwards:
            value = kwards[field]
            if hasattr(country, field):
                setattr(country, field, value)
        countries_to_create.append(country)

    if len(countries_to_create) > 0:
        Country.objects.bulk_create(countries_to_create, batch_size=1000)


def create_multiple_states(
        states
):
    states_to_create = []
    for kwards in states:
        state = State()
        for field in kwards:
            value = kwards[field]
            if hasattr(state, field):
                setattr(state, field, value)
        states_to_create.append(state)

    if len(states_to_create) > 0:
        State.objects.bulk_create(states_to_create)


def create_multiple_cities(
        cities
):
    cities_to_create = []
    for kwards in cities:
        city = City()
        for field in kwards:
            value = kwards[field]
            if hasattr(city, field):
                setattr(city, field, value)
        cities_to_create.append(city)

    if len(cities_to_create) > 0:
        City.objects.bulk_create(cities_to_create, batch_size=1000)
