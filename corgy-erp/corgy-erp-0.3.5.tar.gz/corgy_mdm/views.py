from django.shortcuts import render
from material.frontend.views import ModelViewSet
from material import Layout, Fieldset, Row
from django.utils.translation import ugettext_lazy as _
from . import models

# Create your views here.

class PersonModelViewSet(ModelViewSet):
    model = models.PersonModel

    layout = Layout(
        Fieldset(
            _('Personal details'),
            Row(
                'gender',
                'name_prefix'
            ),
            Row(
                'name_prefix',
                'first_name',
                'middle_name',
                'last_name'
            ),
        ),
        Fieldset(
            _('Birth data'),
            Row(
                'birthdate',
                'birthplace',
            ),
            'name_of_mother',
        ),
        Fieldset(
            _('Contact information'),
            'permanent_address',
            'temporary_address',
            Row('email', 'phone_number'),
        ),
    )

class OrganizationModelViewSet(ModelViewSet):
    model = models.OrganizationModel

