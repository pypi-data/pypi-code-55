"""
metric库
参考：https://github.com/quantopian/empyrical
https://github.com/scikit-learn/scikit-learn/tree/master/sklearn/metrics
"""
from skydl.metrics.alphalens_utils import  build_merged_factory_price_data, factory_mean_ic, factory_ir, rank_ic

__all__ = [
    "build_merged_factory_price_data",
    "factory_mean_ic",
    "factory_ir",
    "rank_ic"
]
