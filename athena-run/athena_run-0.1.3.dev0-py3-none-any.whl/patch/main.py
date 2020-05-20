import patch.pandas as patch_pandas
import patch.sklearn as patch_sklearn


def patch_all():
    patch_pandas.patch()
    patch_sklearn.patch()
