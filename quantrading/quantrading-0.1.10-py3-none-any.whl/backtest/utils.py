import pandas as pd


def divide_code_list_by_quantiles(asset_series: pd.Series, quantiles: int, target_tile: int) -> tuple:
    counts_per_division = len(asset_series) / quantiles
    counts_per_division = int(counts_per_division)

    tile = target_tile
    first_quantile = asset_series.index.to_list()[counts_per_division * tile: counts_per_division * (tile + 1)]
    last_quantile = asset_series.index.to_list()[-counts_per_division * (tile + 1):-counts_per_division * tile]
    return first_quantile, last_quantile


def apply_equal_weights(code_list: list, for_short=False) -> dict:
    total_weight = -1 if for_short else 1
    if len(code_list) == 0:
        weights = {}
    else:
        weights = {}
        weight_per_stock = total_weight / len(code_list)
        for ticker in code_list:
            weights[ticker] = weight_per_stock
    return weights
