import pandas as pd
from pandas.util.testing import assert_series_equal
from ovretl import calculate_margins, calculate_shipment_prices

df_prices = pd.DataFrame(
    data={
        "category": [
            "departure_truck_freight",
            "arrival_truck_freight",
            "departure_fees",
            "freight",
            "arrival_fees",
            "other",
            "insurance",
        ],
        "price_in_eur": [1336.05, 680, 108.59, 3651, 95, 1000, 400],
        "margin_price_in_eur": [0, 20, 32, 534, 0, 1000, 400],
        "vat_price_in_eur": [0, 10, 0, 20, 0, 0, 0],
    },
)
df_prices_initial = pd.DataFrame(
    data={
        "category": [
            "departure_truck_freight",
            "arrival_truck_freight",
            "departure_fees",
            "freight",
            "arrival_fees",
            "other",
            "insurance",
        ],
        "price_in_eur": [1336.05, 680, 108.59, 3651, 95, 1000, 500],
        "margin_price_in_eur": [0, 10, 32, 534, 0, 1000, 500],
        "vat_price_in_eur": [0, 10, 0, 20, 0, 0, 0],
    },
)


def test_calculate_margins():
    shipment = pd.Series()

    result = calculate_margins(shipment, df_prices, df_prices_initial)
    result_should_be = pd.Series(
        data=[576, 500, 586, 400],
        index=[
            "initial_margin_without_insurance",
            "initial_margin_insurance",
            "margin_without_insurance",
            "margin_insurance",
        ],
    )
    assert_series_equal(result, result_should_be)


def test_calculate_shipment_prices():
    shipment = pd.Series()

    result = calculate_shipment_prices(shipment, df_prices)
    result_should_be = pd.Series(
        data=[1336.05, 108.59, 3651, 95, 680, 400, 1336.05 + 108.59 + 3651 + 95 + 680 + 400, 0, 1000, 30],
        index=[
            "departure_truck_freight_price",
            "departure_fees_price",
            "freight_price",
            "arrival_fees_price",
            "arrival_truck_freight_price",
            "insurance_price",
            "turnover",
            "customs_price",
            "other_price",
            "vat_price",
        ],
    )
    assert_series_equal(result, result_should_be)
