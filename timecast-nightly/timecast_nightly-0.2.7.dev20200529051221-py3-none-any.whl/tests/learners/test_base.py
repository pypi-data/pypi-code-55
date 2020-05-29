"""timecast.learners.base: testing"""
import flax
import pytest

from timecast.learners.base import FitMixin
from timecast.learners.base import NewMixin


def test_fit_mixin_abc():
    """Test that FitMixin is abstract"""
    with pytest.raises(TypeError):
        FitMixin()


def test_fit_mixin_subclass():
    """Test that subclass must implement abstract classes"""

    class Dummy(FitMixin):
        """Dummy class"""

    with pytest.raises(TypeError):
        Dummy()


def test_fit_mixin_fit():
    """Test unimplemented class method"""
    with pytest.raises(NotImplementedError):
        FitMixin.fit([], 1)


def test_new_mixin():
    """Test common case"""

    class DummyNew(NewMixin, flax.nn.Module):
        """Dummy class"""

        def apply(self, x, a=2, b=3):
            """Dummy apply"""
            return x + 2 + 3

    DummyNew.new([(1, 2)])


def test_new_mixin_multiple_args():
    """Test multiple unnamed args"""

    class DummyNew(NewMixin, flax.nn.Module):
        """Dummy class"""

        def apply(self, x, a, b=3):
            """Dummy apply"""
            return x + 2 + 3

    with pytest.raises(TypeError):
        DummyNew.new([(1, 2)])

    DummyNew.new([(1, 2)], a=2)

    with pytest.raises(ValueError):
        DummyNew.new([(1, 2)], c=4)
