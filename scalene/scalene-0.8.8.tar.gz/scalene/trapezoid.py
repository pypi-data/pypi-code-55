from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterator,
    List,
    NewType,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)


class trapezoid:

    sample_array: List[float] = []
    total_samples = 0
    max_samples = 0
    current_index = 0
    
    def __init__(self, size: int):
        self.max_samples = size
        self.sample_array = [0] * size
        self.length = [0] * size
        pass

    def add(self, value: float) -> None:
        if self.current_index >= self.max_samples:
            # Find the sample which, when merged, results in lowest loss.
            min_val = float('inf')
            min_index = -1
            for i in range(0, self.current_index-1):
                area_1 = self.sample_array[i] * self.length[i] 
                area_2 = self.sample_array[i+1] * self.length[i+1]
                area_merged = ((self.sample_array[i] + self.sample_array[i+1]) / 2) * (self.length[i] + self.length[i+1])
                loss = area_merged - (area_1 + area_2)
                sq_loss = loss * loss
                if sq_loss < min_val:
                    min_index = i
                    min_val = sq_loss
            print(min_val)
        else:
            self.sample_array[self.current_index] = value
            self.length[self.current_index] = 1
            self.current_index += 1

    def get(self) -> List[float]:
        # FIX: adjust result
        return self.sample_array

    def len(self) -> int:
        return self.current_index
