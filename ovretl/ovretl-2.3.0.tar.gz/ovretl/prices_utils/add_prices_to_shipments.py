import pandas as pd

from ovretl.prices_utils.sum_category_price import select_category_price


def calculate_shipment_prices(shipment: pd.Series, df_prices: pd.DataFrame) -> pd.Series:
    if df_prices is None or len(df_prices) == 0:
        return shipment
    df_prices = df_prices.groupby("category").sum()
    shipment["departure_truck_freight_price"] = select_category_price(
        df_prices, "departure_truck_freight", "price_in_eur"
    )
    shipment["departure_fees_price"] = select_category_price(df_prices, "departure_fees", "price_in_eur")
    shipment["freight_price"] = select_category_price(df_prices, "freight", "price_in_eur")
    shipment["arrival_fees_price"] = select_category_price(df_prices, "arrival_fees", "price_in_eur")
    shipment["arrival_truck_freight_price"] = select_category_price(df_prices, "arrival_truck_freight", "price_in_eur")
    shipment["insurance_price"] = select_category_price(df_prices, "insurance", "price_in_eur")
    shipment["turnover"] = (
        shipment["departure_truck_freight_price"]
        + shipment["departure_fees_price"]
        + shipment["freight_price"]
        + shipment["arrival_fees_price"]
        + shipment["arrival_truck_freight_price"]
        + shipment["insurance_price"]
    )
    shipment["customs_price"] = select_category_price(df_prices, "customs", "price_in_eur")
    shipment["other_price"] = select_category_price(df_prices, "other", "price_in_eur")
    shipment["vat_price"] = df_prices["vat_price_in_eur"].sum()
    return shipment


def calculate_margins(shipment: pd.Series, df_prices: pd.DataFrame, df_prices_initial: pd.DataFrame) -> pd.Series:
    if df_prices is None or len(df_prices) == 0 or df_prices_initial is None or len(df_prices_initial) == 0:
        return shipment
    df_prices = df_prices.groupby("category").sum()
    df_prices_initial = df_prices_initial.groupby("category").sum()

    shipment["initial_margin_without_insurance"] = (
        df_prices_initial["margin_price_in_eur"].sum()
        - select_category_price(df_prices_initial, key="margin_price_in_eur", category="insurance")
        - select_category_price(df_prices_initial, key="margin_price_in_eur", category="customs")
        - select_category_price(df_prices_initial, key="margin_price_in_eur", category="other")
    )
    shipment["initial_margin_insurance"] = select_category_price(
        df_prices_initial, key="margin_price_in_eur", category="insurance"
    )
    shipment["margin_without_insurance"] = (
        df_prices["margin_price_in_eur"].sum()
        - select_category_price(df_prices, key="margin_price_in_eur", category="insurance")
        - select_category_price(df_prices, key="margin_price_in_eur", category="customs")
        - select_category_price(df_prices, key="margin_price_in_eur", category="other")
    )
    shipment["margin_insurance"] = select_category_price(df_prices, key="margin_price_in_eur", category="insurance")
    return shipment


def calculate_shipment_purchase_prices(shipment: pd.Series, df_prices: pd.DataFrame) -> pd.Series:
    if df_prices is None or len(df_prices) == 0:
        return shipment
    df_prices = df_prices.groupby("category").sum()
    shipment["departure_truck_freight_purchase_price"] = select_category_price(
        df_prices, category="departure_truck_freight", key="purchase_price_in_eur"
    )
    shipment["departure_fees_purchase_price"] = select_category_price(
        df_prices, category="departure_fees", key="purchase_price_in_eur"
    )
    shipment["freight_purchase_price"] = select_category_price(
        df_prices, category="freight", key="purchase_price_in_eur"
    )
    shipment["arrival_fees_purchase_price"] = select_category_price(
        df_prices, category="arrival_fees", key="purchase_price_in_eur"
    )
    shipment["arrival_truck_freight_purchase_price"] = select_category_price(
        df_prices, category="arrival_truck_freight", key="purchase_price_in_eur"
    )
    shipment["insurance_purchase_price"] = select_category_price(
        df_prices, category="insurance", key="purchase_price_in_eur"
    )
    return shipment


def add_prices_to_shipments(shipment: pd.Series, find_most_relevant_prices) -> pd.Series:
    df_prices, prices_origin = find_most_relevant_prices(shipment["shipment_id"], shipment["proposition_id"])
    df_prices_initial, initial_prices_origin = find_most_relevant_prices(
        shipment["shipment_id"], shipment["proposition_id"], initial_proposition=True
    )
    shipment = calculate_shipment_prices(shipment=shipment, df_prices=df_prices)
    shipment = calculate_margins(shipment=shipment, df_prices=df_prices, df_prices_initial=df_prices_initial)
    shipment = calculate_shipment_purchase_prices(shipment=shipment, df_prices=df_prices)
    shipment["prices_origin"] = prices_origin
    return shipment
