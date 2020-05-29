import marso

import pytest


def test_non_unicode():
    with pytest.raises(UnicodeDecodeError):
        marso.parse(b'\xe4')
