import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ovretl.tracking_utils.check_shipment_active import check_shipment_active


def test_check_shipment_active():
    quotation = pd.Series(data=["to_be_requoted", False], index=["shipment_status", "cancelled"])
    assert check_shipment_active(quotation, pd.DataFrame()) == False
    finished = pd.Series(data=["finished", False], index=["shipment_status", "cancelled"])
    assert check_shipment_active(finished, pd.DataFrame()) == False
    arrival_date_active = pd.Series(
        data=["in_progress", np.nan, np.nan, np.nan, datetime.now() + timedelta(days=5), np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert check_shipment_active(arrival_date_active, pd.DataFrame()) == True
    arrival_date_not_active = pd.Series(
        data=["booking_request", np.nan, np.nan, np.nan, datetime.now() + timedelta(days=11), np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert check_shipment_active(arrival_date_not_active, pd.DataFrame()) == False
    departure_date_active = pd.Series(
        data=["in_progress", np.nan, np.nan, datetime.now() - timedelta(days=1), np.nan, np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert check_shipment_active(departure_date_active, pd.DataFrame())
    departure_date_not_active = pd.Series(
        data=["in_progress", np.nan, np.nan, datetime.now() - timedelta(days=5), np.nan, np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert not check_shipment_active(departure_date_not_active, pd.DataFrame())
    is_arrived = pd.Series(
        data=["in_progress", np.nan, np.nan, datetime.now() - timedelta(days=1), np.nan, np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert not check_shipment_active(is_arrived, pd.DataFrame(data={"date_type": ["actual", "actual"]}))
    is_not_arrived_and_active = pd.Series(
        data=["in_progress", np.nan, np.nan, datetime.now() - timedelta(days=1), np.nan, np.nan, False],
        index=[
            "shipment_status",
            "finished_date",
            "pickup_date",
            "departure_date",
            "arrival_date",
            "delivery_date",
            "cancelled",
        ],
    )
    assert check_shipment_active(is_not_arrived_and_active, pd.DataFrame(data={"date_type": ["actual", "estimated"]}))
