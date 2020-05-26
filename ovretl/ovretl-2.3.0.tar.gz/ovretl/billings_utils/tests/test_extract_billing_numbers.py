import pandas as pd
from ovretl.billings_utils.extract_billing_numbers import extract_billing_numbers


def test_extract_billing_numbers():
    billings_df = pd.DataFrame(
        data={"shipment_id": ["0", "1", "0"], "billing_number": ["ABC", "DEF", "GHI"]}
    )
    billing_numbers = extract_billing_numbers(billings_df, "0")
    assert billing_numbers == "ABC, GHI"
