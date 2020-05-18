import pandas as pd


def find_shipment_category_shipowner(shipowners_associated_df: pd.DataFrame, role: str):
    if len(shipowners_associated_df) == 0:
        return None
    mask_role = shipowners_associated_df["role"] == role
    shipowners_associated_df_filtered = shipowners_associated_df[mask_role].reset_index(
        drop=True
    )
    if len(shipowners_associated_df_filtered) > 0:
        return shipowners_associated_df_filtered.loc[0, "name"]
    return None


def add_shipowners_to_shipment(
    shipment: pd.Series, shipowner_shipment_with_name_df: pd.DataFrame
) -> pd.Series:
    mask_shipment = (
        shipowner_shipment_with_name_df["shipment_id"] == shipment["shipment_id"]
    )
    shipment["pickup_shipowner"] = find_shipment_category_shipowner(
        shipowners_associated_df=shipowner_shipment_with_name_df[mask_shipment],
        role="departure_truck_freight",
    )
    shipment["departure_shipowner"] = find_shipment_category_shipowner(
        shipowners_associated_df=shipowner_shipment_with_name_df[mask_shipment],
        role="departure_fees",
    )
    shipment["freight_shipowner"] = find_shipment_category_shipowner(
        shipowners_associated_df=shipowner_shipment_with_name_df[mask_shipment],
        role="freight",
    )
    shipment["arrival_shipowner"] = find_shipment_category_shipowner(
        shipowners_associated_df=shipowner_shipment_with_name_df[mask_shipment],
        role="arrival_fees",
    )
    shipment["delivery_shipowner"] = find_shipment_category_shipowner(
        shipowners_associated_df=shipowner_shipment_with_name_df[mask_shipment],
        role="arrival_truck_freight",
    )
    return shipment
