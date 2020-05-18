import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal


from ovretl.loads_utils.merge_shipments_with_loads import (
    split_propositions_shipments_loads,
    merge_with_propositions_loads_then_with_shipments_loads,
)


def test_merge_with_propositions_loads_then_with_shipments_loads():
    loads_df = pd.DataFrame(
        data={
            "total_weight": [200, 100, 200, 200],
            "total_volume": [0.9, 0.9, 1, 0.96],
            "shipment_id": [np.nan, np.nan, "2", "3"],
            "proposition_id": ["0", "1", np.nan, np.nan],
            "taxable_weight": [200, 150, 200, 200],
            "weight_measurable": [1, 1, 1, 1],
        }
    )
    shipments_df = pd.DataFrame(data={"shipment_id": [np.nan, "2", "3"], "proposition_id": ["0", "1", np.nan]})
    shipments_df_true = pd.DataFrame(
        data={
            "shipment_id": [np.nan, "2", "3"],
            "proposition_id": ["0", "1", np.nan],
            "total_volume": [0.9, 0.9, 0.96],
            "total_weight": [200, 100, 200],
            "taxable_weight": [200, 150, 200],
            "weight_measurable": [1, 1, 1],
        }
    )
    (propositions_loads_df, shipments_loads_df,) = split_propositions_shipments_loads(loads_df)

    shipments_df_processed = merge_with_propositions_loads_then_with_shipments_loads(
        shipments_df=shipments_df, propositions_loads_df=propositions_loads_df, shipments_loads_df=shipments_loads_df,
    )
    assert_frame_equal(shipments_df_processed, shipments_df_true, check_dtype=False)
