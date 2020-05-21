from ..smc3rateware import core
from ..smc3rateware.config import TestingConfig
from ..smc3rateware import definitions as defs

import pickle

import os


test_shipment = {
        'shipmentDateCCYYMMDD': '20110110',
        'originCountry': 'USA',
        'originPostalCode': '19106',
        'destinationCountry': 'USA',
        'destinationPostalCode': '07981',
        'tariffName': 'LITECZ02',
        'details': {
                'LTLRequestDetail' : [
                    {
                        'nmfcClass': '100',
                        'weight': '350'
                    },
                    {
                        'nmfcClass': '200',
                        'weight': '800'
                    }
                ]
            }
        }

def get_testingdf():
    filepath = os.path.join(TestingConfig.root_dir, 'shipments.csv')
    return defs.get_df_fromcsv(filepath)

def get_testingLTLRateShipmentMultipleResponse():
    filepath = os.path.join(TestingConfig.root_dir, 'LTLRateShipmentMultipleResponse.pickle')
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)