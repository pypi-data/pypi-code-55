from . import common
from ..smc3rateware import core

import os
import logging


def test_shipment_testingstruct():
    from .common import test_shipment

    core.check_shipmentsstruct_forapi(test_shipment)

def test_shipments_testingdf():    
    df = common.get_testingdf()
    core.check_shipmentsdf_forapi(df)

def test_process_shipmnets_forLTLRateShipmentMultipleRequest():
    df = common.get_testingdf()
    shipments = core.get_shipmentsstruct_forLTLRateShipmentMultipleRequest(
        df, 
        tariff='LITECZ02'
    )

    assert len(shipments) > 0

def test_testingLTLRateShipmentMultipleResponse():
    response = common.get_testingLTLRateShipmentMultipleResponse()

    assert isinstance(response, (list,))