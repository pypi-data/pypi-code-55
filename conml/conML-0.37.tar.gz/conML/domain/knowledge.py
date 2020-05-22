#  C O N S T R U C T I V I S T__ __
#   _____ ____   ____   /  |/  // /
#  / ___// __ \ / __ \ / /|_/ // /
# / /__ / /_/ // / / // /  / // /___
# \___/ \____//_/ /_//_/  /_//_____/
#  M A C H I N E   L E A R N I N G
#
#
# A Project by
# Thomas Schmid | UNIVERSITÄT LEIPZIG
# www.constructivist.ml
#
# Code Author: Dmitrij Denisenko
# Licence: MIT


"""Define the knowledge database.

"""


import pickle
from bisect import bisect
from contextlib import suppress
from collections import defaultdict

from conML.shared.errors import IndexOutOfBucket


def notify_inverted_index(func):
    def wrapper(self, *args, **kwargs):
        for obs in self.observer:
            getattr(obs, func.__name__)(*args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper


class KnowledgeDatabase:
    """Responsible for holding all models that are saved during the
    training.

    Args:
        highest_level (int): The maximal level of the database.
        build_block_from_rows (Callable): Interface to create a
            PandasBlock from pandas.Dataframe samples.

    Attributes:
        database (list): List the KnowledgeDomains.
        source (KnowledgeSource): Holds valid learnblocks.
        n_models (int): Number of models int the database.
        observer (RelativeFinder): Object that monitors changes done
            to the database.


    """

    def __init__(self, highest_level, build_block_from_rows):
        self.highest_level = highest_level
        self.database = [KnowledgeDomain(i) for i in range(highest_level+1)]
        self.source = KnowledgeSource(build_block_from_rows)
        self.observer = []
        self.n_models = 0

    def __str__(self):
        string = "{}".format(str(self.source))
        for domain in self.database:
            string = "\n".join([string, str(domain)])

        return string

    def __repr__(self):
        string = "N_models={}, Source={}".format(str(self.n_models), repr(self.source))
        for domain in self.database:
            domain_repr = repr(domain)
            string = " ".join([
                string, "[{}={}]".format("KnowledgeDomain", domain_repr)
                ]
            )
        return string

    def __contains__(self, item):
        with suppress(KeyError):
            self.get_model(item.uid)
            return True

        return False

    def extend(self, block):
        """Save the learnblock into knowledge database.

        Args:
            block (PandasBlock): Valid learnblock.

        Returns:
            int:
                Number of the inserted block.

        """
        return self.source.append(block)

    def get_block(self, indices):
        """Get learnblock by indices.

        Args:
            indices (list): List with valid indices.

        Returns:
            PandasBlock:
                Constructed from the indices.

        """
        return self.source.get(indices)

    def remove_dependent(self, model):
        """Remove the given model from the database with all other models that
        depend on it.

        Args:
            model (PragmaticMachineLearningModel): Model to be removed.

        Returns:
            List:
                List the deleded models.

        """
        if model.level == self.highest_level:
            self.remove(model)
            return [model]

        else:
            to_delete = [[model]]
            for i in range(self.highest_level):
                d = []
                for m in to_delete[i]:
                    d.extend(list(self.find_dependence_on_next_level(m)))
                to_delete.append(d)

            flatted = set([item for lst in to_delete for item in lst])
            for candidate in flatted:
                try:
                    self.remove(candidate)
                except KeyError:
                    continue

            return flatted

    @notify_inverted_index
    def insert(self, model):
        """Insert model into knowledge database.

        Args:
            model (PragmaticMachineLearningModel): Model to be inserted.

        """
        if model not in self:
            self.database[model.level].insert(model)
            self.n_models += 1

    @notify_inverted_index
    def remove(self, model):
        """Remove model from knowledge database.

        Args:
            model (PragmaticMachineLearningModel): Model to be removed.

        """
        self.database[model.level].remove(model)
        self.n_models -= 1

    def get_model(self, uid):
        """Return model by uid.

        Args:
            uid (str): Unique model identifier.

        Returns:
            PragmaticMachineLearningModel

        """
        _, level, _ = uid.split(".")
        return self.database[int(level)].get(uid)

    def save(self, path):
        """Serialize the knowledge database to the harddrive.

        Args:
            path (str): Storage destination.

        """
        with open(path, "wb") as file:
            pickle.dump(self, file)

    def find_dependence_on_next_level(self, model):
        """Yield all dependencies model on the next higher level.

        Args:
            model (PragmaticMachineLearningModel): On which the dependencies
                are searched.

        Yields:
            PragmaticMachineLearnignModel:
                Dependent on the given model.

        """
        if model.level == self.highest_level:
            yield model
        else:
            domain = self.database[model.level+1]
            for m in domain.knowledge.values():
                if model.uid in m.origin:
                    yield m

    def get_next_identifier(self, level):
        """Return valid identifier for a PragmaticMachineLearningModel.

        Args:
            level (int): Database level.

        Returns:
            int:
                Valid identifier.

        """
        return self.database[level].next_id


class KnowledgeDomain:
    """Representing a domain within a knowledge database.

    Args:
        level (int): Domain level.

    Attributes:
        knowledge (dict): Storage for PragmaticMachineLearningModel.
        biggest_id (int): Largest assigned identifier.

    """

    def __init__(self, level):
        self.level = level
        self.knowledge = {}
        self.biggest_id = 0

    def __str__(self):
        pragmatics = ", ".join([str(v.uid) for k, v in self.knowledge.items()])
        return "\n".join([
                "{:*^100}".format("Level {}".format(str(self.level))),
                "{:20}: {}".format("Models", pragmatics if pragmatics else []),
            ]
        )

    def __repr__(self):
        pragmatics = ", ".join([str(v.uid) for k, v in self.knowledge.items()])
        return ", ".join([
                "{}={}".format("Level", self.level),
                "{}={}".format("Models", pragmatics if pragmatics else []),
                "{}={}".format("Biggest ID", self.biggest_id)
            ]
        )

    @property
    def next_id(self):
        """Return next valid identifier.

        Returns:
            int:
                Valid identifier.

        """
        self.biggest_id += 1
        return self.biggest_id

    def get(self, uid):
        """Return model with the given uid.

        Args:
            uid (str): Unique model identifer.

        Returns:
            PragmaticMachineLearningModel

        """
        return self.knowledge[uid]

    def insert(self, model):
        """Insert model on this domain.

        Args:
            model (PragmaticMachinelearningModel): To be inserted.

        """
        self.knowledge[model] = model

    def remove(self, model):
        """Remove given model from this domain.

        Args:
            model (PragmaticMachineLearnignModel): To be removed.

        """
        del self.knowledge[model]


class KnowledgeSource:
    """Responsible for storing valid learnblocks. So they can be
    restored using indices.

    Args:
        pandas_factory (Callable): Builds PandasBlocks from indices.

    Attributes:
        source (dict): Maps block number to learnblock.
        n_blocks (int): Counts the inserted blocks.
        __last_index (int): Last index in the last block.
        __search_ranges (list): Last indecis of every stored block.

    """
    def __init__(self, pandas_factory):
        self.source = {}
        self.n_block = 0
        self.pandas_factory = pandas_factory
        self.__last_index = 0
        self.__search_ranges = []

    def __str__(self):
        return "\n".join([
                "{:20}: {}".format("# Blocks", str(self.n_block)),
            ]
        )

    def __repr__(self):
        range_repr = {}
        for i, range_end in enumerate(self.__search_ranges):
            if i == 0:
                range_repr[i] = {"range": (0, range_end)}

            else:
                range_repr[i] = {
                    "range": (self.__search_ranges[i-1], range_end)
                }

        for k, v in self.source.items():
            range_repr[k]["shape"] = v.shape()

        return ", ".join([
                "{}={}".format("Blocks", str(self.n_block)),
                "{}={}".format("Sources", range_repr)
            ]
        )

    def append(self, block):
        """Store block into dictionary.

        After storing the block, update the indices to be consistent with
        every other stored block.

        Args:
            block (PandasBlock):  Valid learnblock.

        Returns:
            int:
                Number of the stored block.

        """
        self.source[self.n_block] = block
        self.__reindex(block)
        self.__update_search_range()
        self.n_block += 1
        return self.n_block - 1

    def get(self, indices):
        """Get block via indices.

        Args:
            indices (list): List of indices.

        Returns:
            PandasBlock:
                Reconstructed from given indices.

        """
        rows = list(self.indices_to_rows(indices))
        return self.pandas_factory(rows)

    def __reindex(self, block):
        """Adjust the indices of the given block, so that the the new indices
        will start, where idices of the last stored block ended.

        Args:
            block (PandasBlock): Valid learnblock.

        """
        new_end_indx = self.__last_index+block.n_rows()
        block.reindex(range(self.__last_index, new_end_indx))
        self.__last_index = new_end_indx

    def __update_search_range(self):
        """Append the last index of the last stored block.

        """
        self.__search_ranges.append(self.__last_index)

    def indices_to_rows(self, indices):
        """Find the corresponding row given given a list of indices.

        Args:
            indices (list): List of integers representing row indices of a
                learnblock.

        Yields:
            pandas.DataFrame:
                Representing a single row.

        """
        for index in indices:
            bucket_index = self.bucket_search(index)
            yield self.source[bucket_index].row_as_df_via_index(index)

    def bucket_search(self, index):
        """Search the number of block in which the row with the given index
        is stored.

        Args:
            index (int): Rows index.

        Returns:
            int:
                Block number.

        """
        idx = bisect(self.__search_ranges, index, lo=0, hi=self.n_block-1)
        if idx >= len(self.__search_ranges):
            raise IndexOutOfBucket(
                "Row index out of bucket range."
                "Returns the bucket index, in which rows stored."
                "Make sure the row indices are stored in the corresponding "
                "bucket."
            )

        return idx


class RelativeFinder:
    """Inverted index.

    Maps meta data (timestamps, subject and aim) to models.

    Args:
        levels (int): Levels used in the knowledge database.

    """
    def __init__(self, levels):
        self.indices = {}
        for level in range(levels+1):
            self.indices[level] = (defaultdict(set),
                                   defaultdict(set),
                                   defaultdict(set))

    def __repr__(self, *args):
        level = args[0]
        return (
            f"T: {self.indices[level][0]} \n"
            f"Z: {self.indices[level][1]} \n"
            f"Sigma: {self.indices[level][2]} \n"
        )

    def __contains__(self, item):
        t, z, s = self.get_index_level(item)

        in_t = False
        if (item.min_timestamp, item.max_timestamp) in t.keys():
            in_t = item in t[(item.min_timestamp, item.max_timestamp)]

        in_z = False
        if item.aim in z.keys():
            in_z = item in z[item.aim]

        in_s = []
        for subject in item.subjects:
            if subject in s.keys():
                in_s.append(item in s[subject])

        return in_t and in_z and all(in_s)

    def find(self, pair, model, deconst_full_tolerance):
        """Find the all relatives for the given model.

        Args:
            pair (tuple): Relationship.
            model (PragmaticMachineLearningModel): Instantiaed valid model.
            deconst_full_tolerance (float): How big the distance is allowed
                to be in a complete relationship.

        Returns:
            list:
                Sorted list of relatives according their uid..

        """
        index_t, index_z, index_sigma = self.get_index_level(model)
        relatives = {}

        if pair == ("T", "Z"):
            set_t = index_t[(model.min_timestamp, model.max_timestamp)]
            set_z = index_z[model.aim]
            relatives = set_t.intersection(set_z)

        elif pair == ("T", "Sigma"):
            set_t = index_t[(model.min_timestamp, model.max_timestamp)]
            set_s = set()
            for subject in model.subjects:
                set_s = set_s.union(index_sigma[subject])
            relatives = set_t.intersection(set_s)

        elif pair == ("Sigma", "Z"):
            set_s = set()
            for subject in model.subjects:
                set_s = set_s.union(index_sigma[subject])

            set_z = index_z[model.aim]
            relatives = set_s.intersection(set_z)

        elif pair == ("complete", ):
            set_t = set()
            for min_time, max_time in index_t.keys():
                if self.complete_relationship_constraint(
                        model, min_time, max_time, deconst_full_tolerance
                ):
                    set_t.update(index_t[(min_time, max_time)])
            set_s = set()
            for subject in model.subjects:
                set_s = set_s.union(index_sigma[subject])
            set_z = index_z[model.aim]
            relatives = set_t.intersection(set_s).intersection(set_z)

        if model in relatives:
            relatives.remove(model)

        return sorted(relatives, key=lambda m: m.identifier)

    def complete_relationship_constraint(
            self, model, min_t, max_t, deconst_full_tolerance
    ):
        """Check if the model is fullfilling the complete relationship.

        That is, if the time values of the main model are within the given
        min_t and max_t or enclosing these values.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.
            min_t (int): Min time of the possible relative.
            max_t (int): Max time of the possible relative.
            deconst_full_tolerance (float): How big should be the enclosing
                and exclusion distance be allowed.

        Returns:
            bool:
                True if the model is fullfilling the complete relationship
                regarding his time values.

        """
        return (
            self.__time_exclusion(model, min_t, max_t, deconst_full_tolerance)
            or
            self.__time_inclusion(model, min_t, max_t, deconst_full_tolerance)
        )

    def __time_inclusion(self, model, min_t, max_t, tolerance):
        """Check if the model timestamps include the given time values
            on condition that the given distance is not exceeded.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.
            min_t (int): Min time of the possible relative.
            max_t (int): Max time of the possible relative.
            tolerance (float): Distance tolerance.

        Returns:
            bool:
                True if the model time is including the given times.

        """
        return (
            model.min_timestamp >= min_t and model.max_timestamp <= max_t
            and
            model.min_timestamp - min_t <= model.min_timestamp * tolerance
            and
            model.max_timestamp - max_t <= model.max_timestamp * tolerance
        )

    def __time_exclusion(self, model, min_t, max_t, tolerance):
        """Check if the model timestamps exclude both given timestamps.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.
            min_t (int): Min time of the possible relative.
            max_t (int): Max time of the possible relative.
            tolerance (float): Distance tolerance.

        Returns:
            bool:
                True if the model time is excluding both given timestamps.

        """
        return (
            model.min_timestamp <= min_t and model.max_timestamp >= max_t
            and
            model.min_timestamp - min_t <= model.min_timestamp * tolerance
            and
            model.max_timestamp - max_t <= model.max_timestamp * tolerance
        )

    def remove(self, model):
        """Remove given model from the inverted index.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.

        """
        t_list, s_lists, z_list = self.get_index_lists(model,
                                                      time=True,
                                                      subject=True,
                                                      aim=True)
        for s_list in s_lists:
            if model in s_list:
                s_list.remove(model)

            if not s_list:
                del s_list

        if model in z_list:
            z_list.remove(model)

        if model in t_list:
            t_list.remove(model)

        if not t_list:
            del self.indices[model.level][0][(model.min_timestamp,
                                              model.max_timestamp)]

        if not z_list:
            del self.indices[model.level][1][model.aim]

    def insert(self, model):
        """Insert given model into the inverted index.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.

        """
        t, z, sigma = self.get_index_level(model)
        t[(model.min_timestamp, model.max_timestamp)].add(model)
        z[model.aim].add(model)

        for subject in model.subjects:
            sigma[subject].add(model)

    def get_index_lists(self, model, time, subject, aim):
        """Get all models whose meta data equals the model timestamps,
        subject and aim.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.
            time (bool): Indicates if time relatives should be found.
            subject (bool): Indicates if the subject relatives should be found.
            aim (bool): Indicates if the aim relatives should be found.

        Returns:
            tuple:
                Lists with relatives.

        """
        t, z, sigma = self.get_index_level(model)
        t_list = s_list = z_list = None
        if time:
            t_list = t[(model.min_timestamp, model.max_timestamp)]
        if subject:
            s_lists = []
            for subject in model.subjects:
                s_lists.append(sigma[subject])
            # s_list = sigma[model.subject]
        if aim:
            z_list = z[model.aim]

        return t_list, s_lists, z_list

    def get_index_level(self, model):
        """Get time, subject and aim index on model level.

        Args:
            model (PragmaticMachineLearningModel): Instantiaded valid model.

        Returns:
            tuple:
                List with indices.

        """
        index_t = self.indices[model.meta.knowledge_level][0]
        index_z = self.indices[model.meta.knowledge_level][1]
        index_sigma = self.indices[model.meta.knowledge_level][2]
        return index_t, index_z, index_sigma
