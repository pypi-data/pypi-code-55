import unittest

from testchapter.address import Address

class RandomAddressTestCase(unittest.TestCase):

    def test_get_random_in_antwerp(self):
        address = Address()
        address_dictionary = address.get_random_in_antwerp()
        address_dictionary_keys_list = list( address_dictionary.keys() )
        address_dictionary_keys_list.sort()
        self.assertTrue( address_dictionary_keys_list == ['district', 'huisnummer', 'postnummer', 'straat'] )


if __name__ == '__main__':
    unittest.main()
