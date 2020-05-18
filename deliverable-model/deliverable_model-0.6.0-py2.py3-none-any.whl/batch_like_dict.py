from typing import Iterator

from micro_toolkit.data_process.batch_iterator import BatchingIterator


class BatchLikeDict(dict):
    def iterate_sample(self) -> Iterator[dict]:
        batcher = BatchingIterator(1)
        for sub_request_dict in batcher(self):
            yield sub_request_dict
