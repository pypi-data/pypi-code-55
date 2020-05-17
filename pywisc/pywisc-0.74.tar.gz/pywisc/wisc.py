import json
import logging
import os
from pywisc.prueba import Prueba


logger = logging.getLogger(__name__)
VALID_VERSIONS = [4]
VALID_LANGUAGES = ['es']
VALID_COUNTRIES = ['ar']


class Wisc:
    """ a WISC test """
    def __init__(self, wisc_version=4, language='es', country='ar'):
        """ start a wisc test instance
            Params:
                wisc_version: 4 or versiones futuras
                language: 'es'
                country: 'ar' """
        assert wisc_version in VALID_VERSIONS
        assert language in VALID_LANGUAGES
        assert country in VALID_COUNTRIES
        here = os.path.dirname(os.path.realpath(__file__))
        json_wisc = f'wisc_{wisc_version}_{language}_{country}.json'
        definition_data = os.path.join(here, 'data', json_wisc)
        if type(definition_data) == dict:
            self.data = definition_data
        elif type(definition_data) == str:
            self.data = self.load_from_file(definition_file_path=definition_data)
        self.language = self.data['language']
        self.version = self.data['version']
        self.country = self.data['country']

        self.validate()
        self.pruebas = []
        self.load_pruebas(data=self.data)

        # required data to start
        self.required_to_start = self.data['required_to_start']

    def load_from_file(self, definition_file_path):
        f = open(definition_file_path, 'r')
        data = json.loads(f.read())
        f.close()
        return data
    
    def validate(self):
        self.is_valid = False
        assert self.data['version'] in VALID_VERSIONS
        assert self.data['language'] in VALID_LANGUAGES
        assert self.data['country'] in VALID_COUNTRIES
        assert len(self.data['tests']) > 0
        for prueba in self.data['tests']:
            assert type(prueba['name']) == str
            assert type(prueba['code']) == str
            assert len(prueba['subtests']) > 0
            for subprueba in prueba['subtests']:
                assert type(subprueba['name']) == str
                assert type(subprueba['code']) == str
                assert type(subprueba['mandatory']) == bool
                assert type(subprueba['orden']) == int

        self.is_valid = True
        return True

    def load_pruebas(self, data):
        for prueba in self.data['tests']:
            p = Prueba()
            p.load_from_dict(data=prueba)
            self.pruebas.append(p)
    
    def __str__(self):
        tot_pruebas = len(self.pruebas)
        return f'WISC {self.version} ({self.language}-{self.country}). Pruebas: {tot_pruebas}.'
