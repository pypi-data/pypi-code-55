from . import utils

import logging
import pandas as pd # TODO: organize


def get_reqiredfields_forapi():
    return [
        'shipmentID',
        'shipmentDateCCYYMMDD', 'originCountry', 
        'originPostalCode', 'destinationCountry', 
        'destinationPostalCode', 'tariffName', 
        'details'
    ]

def get_uniquefields_forapi():
    return ['freight_class', 'weight']

def get_expecteddtypes_formodule():
    return {
        'ship_id': str,
        'ship_date': str,
        'origin_zip': str,
        'origin_country': str,
        'dest_zip': str,
        'dest_country': str,
        'freight_class': str,
        'weight': float
    }

def get_requiredstruct_forLTLRateShipmentRequest():
    return {
        'shipmentDateCCYYMMDD': '',
        'originCountry': '',
        'originPostalCode': '',
        'destinationCountry': '',
        'destinationPostalCode': '',
        'tariffName': '',
        'details': {
                'LTLRequestDetail' : [
                    {
                        'nmfcClass': '',
                        'weight': ''
                    }
                ]
            }
        }

def get_dftostruct_renamer_forLTLRateShipmentMultipleRequest():
    return {
        'ship_id': 'shipmentID',
        'ship_date': 'shipmentDateCCYYMMDD',
        'origin_zip': 'originPostalCode',
        'origin_country': 'originCountry',
        'dest_zip': 'destinationPostalCode',
        'dest_country': 'destinationCountry',
        'freight_class': 'nmfcClass', 'weight' : 'weight'
    }

def format_date(d:str):
    """returns expected input date value as required CCYYMMDD"""
    year = str(int(d.year))
    month = str(int(d.month))
    day = str(int(d.day))
    century = str(utils.get_centuryfromyear(int(year)))

    return '%s%s%s%s' % (century, year[-2:], month.zfill(2), day.zfill(2))

def get_df_fromcsv(filepath:str):
    # TODO: renamer this to something more specific
    logging.info('loading file from %s.' % filepath)
    return pd.read_csv(
        filepath, 
        dtype=get_expecteddtypes_formodule(), 
        parse_dates=['ship_date']
    )