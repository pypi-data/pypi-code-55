import unittest
import time
import random
from testchapter.address_base import address_dictionary

class AddressBaseTestCase(unittest.TestCase):

    def test_nbr_of_keys( self ):
        nbr_of_keys = len( address_dictionary.keys() )
        self.assertTrue( nbr_of_keys == 3463 )


    def test_nbr_of_values( self ):
        nbr_of_values = len(address_dictionary.values())
        self.assertTrue( nbr_of_values == 3463 )


    def test_pick_randomly_an_entry( self ):
        address_list = list( address_dictionary.values() )
        nbr_of_items = len( address_list )
        address_list_max_idx = nbr_of_items - 1

        self.assertTrue( isinstance( address_list[ address_list_max_idx ], dict ) )

        with self.assertRaises(IndexError):
            address_list[address_list_max_idx + 1]

        time.sleep(0.125)
        milliseconds = int(round(time.time() * 1000))
        random.seed(milliseconds)
        rInt = random.randint(1, address_list_max_idx)

        self.assertTrue( rInt < nbr_of_items )

        address_dictionary_item = address_list[rInt]

        self.assertTrue( isinstance( address_dictionary_item, dict ) )



    def test_values_of_address_dictionary_item(self):
        address_list = list( address_dictionary.values() )
        nbr_of_items = len( address_list )
        address_list_max_idx = nbr_of_items - 1

        address_dictionary_item = address_list[ address_list_max_idx ]

        address_dictionary_item_keys_list = list( address_dictionary_item.keys() )
        address_dictionary_item_keys_list.sort()

        self.assertTrue( address_dictionary_item_keys_list == [ 'district', 'postnummer', 'straat' ] )


if __name__ == '__main__':
    unittest.main()
