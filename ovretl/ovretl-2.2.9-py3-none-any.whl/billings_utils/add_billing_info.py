import pandas as pd

from ovretl.billings_utils.extract_billing_numbers import extract_billing_numbers
from ovretl.billings_utils.compute_billing_status import compute_billing_status


def add_billing_info(shipments_df: pd.DataFrame, billings_df: pd.DataFrame):
    shipments_df["billing_numbers"] = shipments_df.apply(
        lambda row: extract_billing_numbers(billings_df, row["shipment_id"]), axis=1
    )
    shipments_df["billing_status"] = shipments_df.apply(
        lambda row: compute_billing_status(billings_df, row["shipment_id"]), axis=1
    )
    return shipments_df
