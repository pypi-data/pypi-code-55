from django.test import TestCase, tag
from django.urls import reverse
from model_bakery.baker import make_recipe

from ..baker_recipes import coronaviruskap_options
from ..forms import CoronavirusKapForm


class TestCoranavirus(TestCase):
    def test_(self):
        make_recipe("sarscov2.coronaviruskap")

    def test_form(self):
        screening_identifier = "12345"
        coronaviruskap_options.update(
            subject_identifier=screening_identifier,
            screening_identifier=screening_identifier,
        )
        form = CoronavirusKapForm(data=coronaviruskap_options)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_form_get(self):
        screening_identifier = "12345"
        coronaviruskap_options.update(
            subject_identifier=screening_identifier,
            screening_identifier=screening_identifier,
        )
        opts = {k: v for k, v in coronaviruskap_options.items() if v is not None}
        url = reverse("admin:sarscov2_coronaviruskap_add")
        response = self.client.post(url, opts)
        self.assertEqual(response.status_code, 302)
