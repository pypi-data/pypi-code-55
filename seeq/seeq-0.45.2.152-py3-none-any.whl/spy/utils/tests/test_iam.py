import pytest

import pandas as pd

from .. import _iam
from ...tests import test_common

from seeq.sdk import *

from seeq import spy


def setup_module():
    test_common.login()


@pytest.mark.system4
def test_get_acl():
    push_df = spy.push(metadata=pd.DataFrame([{
        'Type': 'Signal',
        'Name': 'test_get_acl'
    }]))

    item_id = push_df.iloc[0]['ID']

    acl_df = _iam.get_acl(item_id)

    assert len(acl_df) > 0
