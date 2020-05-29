import pandas as pd
from ovretl.billings_utils.compute_billing_status import compute_billing_status


def test_compute_billing_status():
    billings_df_awaiting_invoice = pd.DataFrame(
        data={
            "shipment_id": ["0", "1", "0"],
            "status": ["new", "DEF", "in_modification"],
        }
    )
    billing_status_awaiting_invoice = compute_billing_status(
        billings_df_awaiting_invoice, "0"
    )
    billings_df_due = pd.DataFrame(
        data={
            "shipment_id": ["0", "1", "0"],
            "status": ["due", "DEF", "in_modification"],
        }
    )
    billing_status_due = compute_billing_status(billings_df_due, "0")
    billings_df_paid = pd.DataFrame(
        data={
            "shipment_id": ["0", "1", "0"],
            "status": ["paid", "DEF", "in_modification"],
        }
    )
    billing_status_paid = compute_billing_status(billings_df_paid, "0")
    assert billing_status_awaiting_invoice == "awaiting_invoice"
    assert billing_status_due == "due"
    assert billing_status_paid == "paid"
