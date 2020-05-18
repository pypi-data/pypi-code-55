import pandas as pd
from datetime import datetime


def check_shipment_active(shipment: pd.Series):
    if shipment["cancelled"] == True:
        return False
    if shipment["shipment_status"] in [
        "new",
        "not_answered",
        "propositions_sent",
        "purchase_ready",
        "to_be_requoted",
        "not_answered_declined",
    ]:
        return False
    if shipment["shipment_status"] == "finished" or not pd.isna(shipment["finished_date"]):
        return False
    if (
        pd.isna(shipment["pickup_date"])
        and pd.isna(shipment["departure_date"])
        and pd.isna(shipment["arrival_date"])
        and pd.isna(shipment["delivery_date"])
    ):
        return True
    if not pd.isna(shipment["arrival_date"]) and (datetime.now() - shipment["arrival_date"]).days > -10:
        return True
    if not pd.isna(shipment["departure_date"]) and (datetime.now() - shipment["departure_date"]).days < 4:
        return True
    return False
