import pandas as pd


def extract_billing_numbers(billings_df: pd.DataFrame, shipment_id: str):
    df_billings_shipment = billings_df[billings_df["shipment_id"] == shipment_id]
    if df_billings_shipment["billing_number"].apply(lambda x: not pd.isna(x)).all():
        return ", ".join(df_billings_shipment["billing_number"])
    return ""
