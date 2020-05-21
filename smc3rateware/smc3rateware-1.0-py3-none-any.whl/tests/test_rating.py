from . import common
from ..smc3rateware import core
from ..smc3rateware import utils
from ..smc3rateware import definitions as defs

import os
import logging
import pytest

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def test_username_forapi():
    assert core.get_username_forapi() is not None

def test_password_forapi():
    assert core.get_password_forapi() is not None

def test_licensekey_forapi():
    assert core.get_licensekey_forapi() is not None

@pytest.mark.skipif(core.get_licensekey_forapi() == '', reason='no credentials')
def test_LTLRateShipment():
    client, custom_header = core.init()

    result = client.service.LTLRateShipment(
        _soapheaders=custom_header, 
        LTLRateShipmentRequest=common.test_shipment
    )
    
    assert float(result['LHGrossCharge']) > 0.0

@pytest.mark.skipif(core.get_licensekey_forapi() == '', reason='no credentials')
def test_LTLRateShipmentMultiple():
    client, custom_header = core.init()
    shipments = [common.test_shipment]*5

    response = client.service.LTLRateShipmentMultiple(
        _soapheaders=custom_header, 
        LTLRateShipmentMultipleRequest={'LTLRateShipmentRequest': shipments}
    )

    assert sum([float(r['LHGrossCharge']) for r in response]) > 0.0
    assert len(response) == len(shipments)

@pytest.mark.skipif(core.get_licensekey_forapi() == '', reason='no credentials')
def test_LTLRateShipmentMultiple_fromdf():
    client, custom_header = core.init()
    df = common.get_testingdf()
    shipments = core.get_shipmentsstruct_forLTLRateShipmentMultipleRequest(
        df, 
        tariff='LITECZ02'
    )

    response = client.service.LTLRateShipmentMultiple(
        _soapheaders=custom_header, 
        LTLRateShipmentMultipleRequest={'LTLRateShipmentRequest': shipments}
    )

    assert sum([float(r['LHGrossCharge']) for r in response]) > 0.0
    assert len(response) == len(shipments)

    utils.save_object(
        response, 
        os.path.join(
            common.TestingConfig.root_dir, 
            'LTLRateShipmentMultipleResponse.pickle'
        )
    )

def test_process_shipments_fromLTLRateShipmentMultipleResponse():
    # TODO: make this fire after request test
    response = common.get_testingLTLRateShipmentMultipleResponse()
    shipments = core.get_shipmentsdf_fromLTLRateShipmentMultipleResponse(response)

    assert len(shipments) > 0

    df = common.get_testingdf()
    cols = list(defs.get_dftostruct_renamer_forLTLRateShipmentMultipleRequest().keys())

    # weights were rounded
    cols = [col for col in cols if col != 'weight']
    
    df = df.sort_values(by=df.columns.tolist())
    shipments = shipments.sort_values(by=df.columns.tolist())
    
    assert (shipments[cols].values == df[cols].values).all()