from sklearn.model_selection import train_test_split
from typing import Tuple


class Dataset:
    def __init__(self, *data, size: Tuple, shuffle=True):
        self.raw_data = data
        assert 4 > len(size) > 0, f"Size length must be 1, 2 and 3" \
                                  f"but now got {len(size)}"
        self.shuffle = shuffle
        self.dataset = None
        if len(size) == 1:
            self.train_size = size[0]
        elif len(size) == 2:
            self.train_size, self.test_size = size
        else:
            self.train_size, self.test_size, self.valid_size = size

    def split(self) -> Tuple:
        # X_train, X_test, y_train, y_test
        self.dataset = train_test_split(*self.raw_data, shuffle=self.shuffle,
                                        train_size=self.train_size)
        return self.dataset  # tuple type

