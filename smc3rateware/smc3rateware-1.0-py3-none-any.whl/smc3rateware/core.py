import os
import logging

from .config import SMC3RatewareConfig
from . import definitions as defs
from . import utils

from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
import pandas as pd
import numpy as np


def check_cols(to_check:list, check_against:list=defs.get_reqiredfields_forapi()):
    missingany = False
    for col in to_check:
        if col not in check_against: 
            logging.warn('could not find %s' % col)
            missingany = True
    
    assert not missingany

def check_shipmentsstruct_forapi(struct:dict):
    check_cols(
        to_check=list(struct.keys()),
        check_against=defs.get_reqiredfields_forapi()
    )

def check_shipmentsdf_forapi(df:pd.DataFrame):
    check_cols(
        to_check=df.columns.tolist(), 
        check_against=list(defs.get_expecteddtypes_formodule().keys())
    )

def get_username_forapi():
    return os.getenv('API_USERNAME') or ''

def get_password_forapi():
    # TODO: only for root processes(?)
    return os.getenv('API_PASSWORD') or ''

def get_licensekey_forapi():
    # TODO: only for root processes(?)
    return os.getenv('API_LICENSE_KEY') or ''

def get_customheader(username:str, password:str, license_key:str):
    return {
        'AuthenticationToken': {
            'username': username, 
            'password': password, 
            'licenseKey': license_key
            }
        }

def get_authenticated_session(username:str, password:str, license_key:str):
    session = Session()
    session.auth = HTTPBasicAuth(username, password)

    return session

def get_client(username:str, password:str, license_key:str):
    session = get_authenticated_session(username, password, license_key)
    target = '%s?WSDL' % SMC3RatewareConfig.ENDPOINT

    logging.debug('endpoint target: %s' % target)
    client = Client(target, transport=Transport(session=session))

    return client

def process_dfdata_forapi(df:pd.DataFrame):
    """returns converted dates, weights, and classes"""
    df.ship_date = df.ship_date.apply(defs.format_date)
    df.weight = np.ceil(df.weight).astype(int).astype(str)
    df.freight_class = df.freight_class.astype(int).astype(str)
    df.ship_id = df.ship_id.astype(str)
    return df

def get_shipmentsstruct_forLTLRateShipmentMultipleRequest(df:pd.DataFrame, tariff:str):
    """
    a.
    df (minimum columns) = [ship_id,ship_date,origin_zip,origin_country,
        dest_zip,dest_country,class,weight]

    b.
    struct (dict) = {
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

    NOTE: assumes origins, destinations, and dates are the same for each
    unique ship_id.
    TODO: add argument for tariff selection (if rate by tariff).
    """
    df = process_dfdata_forapi(df)
    renamer = defs.get_dftostruct_renamer_forLTLRateShipmentMultipleRequest()

    # would love c++ here (TODO: try numpy arrays)
    shipments = []

    # TODO: derive from definitions
    unique_fields = defs.get_uniquefields_forapi()
    shared_fields = [col for col in renamer if col not in unique_fields]

    for shipment in df.ship_id.unique():
        new_shipment = dict(defs.get_requiredstruct_forLTLRateShipmentRequest())
        detail_struct = dict(new_shipment['details']['LTLRequestDetail'][0])
        new_shipment['details']['LTLRequestDetail'] = []
        fshipments = df[df.ship_id == shipment][list(renamer)]

        for field in shared_fields:
            new_shipment[renamer[field]] = str(fshipments[field].iloc[0])
        
        for order in range(len(fshipments)):
            new_detail = dict(detail_struct)

            for field in unique_fields:
                new_detail[renamer[field]] = fshipments[field].iloc[order]
            
            new_shipment['details']['LTLRequestDetail'].append(new_detail)
        
        new_shipment['tariffName'] = tariff # TODO: make arg
        shipments.append(new_shipment)
    
    return shipments

def get_shipmentsdf_fromLTLRateShipmentMultipleResponse(response:list):
    # TODO: add more testing here (include checks for input vs output)
    renamer = defs.get_dftostruct_renamer_forLTLRateShipmentMultipleRequest()
    cols = list(renamer.keys())
    
    # TODO: derive from definitions
    unique_fields = defs.get_uniquefields_forapi()
    shared_fields = [renamer[col] for col in cols if col not in unique_fields]
    unique_fields = [renamer[col] for col in list(unique_fields)] 

    # reversed the renamer to apply the input-mapping to outputs
    rrenamer = {v: k for k, v in renamer.items()}

    df = pd.DataFrame(columns=cols)
    for r in response:
        orders = list(range(len(r['details']['LTLResponseDetail'])))
        detail_cols = [col for col in list(r['details']['LTLResponseDetail'][0]) if col not in list(rrenamer.keys())]
        for order in orders:
            rrated = pd.DataFrame({rrenamer[field]: [r[field]] for field in shared_fields})
            for field in unique_fields:
                rrated[rrenamer[field]] = r['details']['LTLResponseDetail'][order][field]
            
            for field in detail_cols:
                rrated[field] = r['details']['LTLResponseDetail'][order][field]
                
            df = df.append(rrated, sort=False)
    
    df['ship_date'] = pd.to_datetime(df.ship_date.apply(utils.get_datetimestr_fromCCYYMMDD))

    return df

def get_df_fromLTLRateShipmentMultiple(results:list):
    return pd.DataFrame() # TODO

def init():
    """returns client, custom_header"""
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    username = get_username_forapi()
    password = get_password_forapi()
    license_key = get_licensekey_forapi()

    client = get_client(username, password, license_key)
    custom_header = get_customheader(username, password, license_key)
    
    return client, custom_header

def rate_usingLTLRateShipmentMultipleRequest_fromdf(df:pd.DataFrame, tariff:str='LITECZ02'):
    """returns df rated"""
    # TODO: add checks
    logging.info('rating %s with %s using LTLRateShipmentMultiple.' % (str(df.shape), tariff))
    
    client, custom_header = init()
    shipments = get_shipmentsstruct_forLTLRateShipmentMultipleRequest(
        df, 
        tariff=tariff
    )

    response = client.service.LTLRateShipmentMultiple(
        _soapheaders=custom_header, 
        LTLRateShipmentMultipleRequest={'LTLRateShipmentRequest': shipments}
    )

    df = get_shipmentsdf_fromLTLRateShipmentMultipleResponse(response)
    logging.info('rated %s using LTLRateShipmentMultiple.' % str(df.shape))
    
    return df
    