import unittest
from  testchapter.address import Address

class AddressTestCase(unittest.TestCase):


    def test_init(self):
        address = Address()
        self.assertTrue( isinstance( address, Address) )


    def test_get_random_address_and_random_housenumber(self):
        address = Address()
        random_address = address._lookup_in_antwerp_random()
        self.assertTrue( isinstance( random_address, dict ) )

        list_of_keys = list( random_address.keys() )
        list_of_keys.sort()

        self.assertTrue( list_of_keys == ['district', 'postnummer', 'straat'] )


if __name__ == '__main__':
    unittest.main()
