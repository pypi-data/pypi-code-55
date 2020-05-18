import pandas as pd
from ovretl.prices_utils.find_most_relevant_prices import find_prices_from_entity
from pandas.util.testing import assert_frame_equal


def test_find_most_relevant_prices():
    entity_df = pd.DataFrame(data={"foo_id": [2, 1, 3],})
    prices_df = pd.DataFrame(data={"bar_id": [2, 5, 2, 6, 3],})
    result = find_prices_from_entity(
        entity_df=entity_df, prices_df=prices_df, entity_key_in_entity_df="foo_id", entity_key_in_prices_df="bar_id",
    )
    result_should_be = pd.DataFrame(data={"bar_id": [2, 2, 3]})
    assert_frame_equal(result.reset_index(drop=True), result_should_be)
