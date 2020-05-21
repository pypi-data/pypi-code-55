from lexsub.algorithms.embedding_utils import EmbeddingLookup
from lexsub.process_data.definition import LexSubExample


class DataReader:
    def __init__(self, fi, data_set: str, embedding_file: str):
        self.fi = fi
        self.num_lines = 0
        self.vocab = set()
        self.data_points = []
        # Read Data
        if data_set == 'SEMEVAL':
            self.process_semeval_data()
        else:
            raise NotImplementedError

        # populate indexer etc for embedding utils
        self.embed_lookup = EmbeddingLookup(embed_file=embedding_file)

    def process_semeval_data(self):
        for line in self.fi:
            self.num_lines += 1
            # Process / Read Lines and wrap into a LexSub Example template
            segments = line.split('\t')
            data_point = LexSubExample(key=segments[0],
                                       idx=segments[1],
                                       word_pos=int(segments[2]),
                                       context=segments[3])
            self.data_points.append(data_point)

