from unittest import TestCase

from .context import extract_informations


class ExtractInformationsTest(TestCase):

    def test_should_have_tags(self):
        headers = {'params': {'tags': ['cat', 'dog']},
                   'operations': ['to_save'],
                   'pipeline': 'idp',
                   'step': 'ids',
                   'name': 'test',
                   'extension': 'jpeg'}

        params, operations, _, _, name, extension = extract_informations(headers)

        self.assertEqual(params, {'tags': ['cat', 'dog']})
        self.assertEqual(operations, ['to_save'])
        self.assertEqual(name, "test")
        self.assertEqual(extension, "jpeg")
