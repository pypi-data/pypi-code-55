import random
import time
import requests
from testchapter.address_base import address_dictionary


class Address(object):


    url_request_basis_register_vlaanderen = "https://api.basisregisters.vlaanderen.be/v1/adressen?postcode=%s&straatnaam=%s"


    def __init__(self):
        self.address_list = list( address_dictionary.values() )
        nbr_of_items = len( self.address_list )
        self.address_list_max_idx = nbr_of_items - 1
        self.nbr_of_tries_lookup_digit = 5

    def get_random_in_antwerp(self):
        address_dictionary = self._lookup_in_antwerp_random()
        house_number = self._lookup_random_house_number( **address_dictionary )
        address_dictionary[ 'huisnummer' ] = house_number
        return address_dictionary

    def _lookup_in_antwerp_random(self):
        return self._get_from_antwerp_dictionary()


    def _lookup_random_house_number(self, **kwargs):
        postal_code = kwargs[ 'postnummer' ]
        street = kwargs[ 'straat' ]

        url = self.url_request_basis_register_vlaanderen % ( postal_code, street )
        response = requests.get( url, allow_redirects=False )

        nbr = 0 #house_number as an integer

        if response.status_code == 200:
            addresses = response.json()
            address_list = addresses["adressen"]
            addresses_idx_max = len(address_list) - 1

            if addresses_idx_max > 0:

                nFound = False
                cntr_indx = 0
                cntr_total = self.nbr_of_tries_lookup_digit

                while ((not nFound) and (cntr_indx < cntr_total)):
                    time.sleep(0.125)
                    milliseconds = int(round(time.time() * 1000))
                    random.seed(milliseconds)
                    rInt = random.randint(1, addresses_idx_max)
                    house_number = address_list[rInt]["huisnummer"]

                    if house_number.isdigit():
                        nFound = True
                        nbr = int(house_number)
                    cntr_indx += 1

        return nbr


    def _get_from_antwerp_dictionary(self):
        time.sleep(0.125)
        milliseconds = int( round(time.time() * 1000 ) )
        random.seed( milliseconds )
        rInt = random.randint(1, self.address_list_max_idx )

        return self.address_list[rInt]