"""flax.nn.Module for wrapping an array

Todo:
    * Validate data and add negative tests
    * Implement batching
"""
import flax


class Precomputed(flax.nn.Module):
    """Wraps an array

    Notes:
        * Assumes the first dimension is a time dimension
        * Assumes the data is accessed in order (i.e., no shuffling)
    
    Warning:
        * Ignores init_by_shape
    """

    def apply(self, x, arr):
        """Apply function"""
        self.index = self.state("index", shape=(), initializer=flax.nn.initializers.zeros)
        val = arr[self.index.value.astype(int)]
        if not self.is_initializing():
            self.index.value += 1
        return val
