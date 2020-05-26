import pandas as pd


def compute_billing_status(billings_df: pd.DataFrame, shipment_id: str):
    df_billings_shipment = billings_df[billings_df["shipment_id"] == shipment_id]
    if len(df_billings_shipment) == 0:
        return "awaiting_invoice"
    if (
        df_billings_shipment["status"]
        .apply(lambda s: s in ["new", "in_modification"])
        .all()
    ):
        return "awaiting_invoice"
    if df_billings_shipment["status"].apply(lambda s: s == "due").any():
        return "due"
    if df_billings_shipment["status"].apply(lambda s: s == "available").any():
        return "available"
    return "paid"
