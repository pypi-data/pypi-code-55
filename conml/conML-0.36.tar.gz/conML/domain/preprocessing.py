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


"""Defines the block drawing, learnlbock identification and cluster search
within one dimensional list.

"""


from itertools import zip_longest

from conML.shared import logger
from conML.shared.logger import LearnblockIdentificationInfo


__all__ = (
    "LearnblockIdentifier",
    "ClusterFinder",
    "Source"
)


class Source:
    """Responsible of preprocessing the given pandas dataframes.

    Converts the the given pandas dataframe to an PandasBlock object and
    saves it into knowledge database.

    Args:
        knowledge (KnowledgeDatabase): Found blocks written to this database.
        df_converter (Callable): Convert pandas dataframe to an PandasBlock.

    """

    def __init__(self, knowledge, df_converter):
        self.knowledge = knowledge
        self.df_converter = df_converter

    def process(self, df):
        """Converts the given dataframe into PandasBlock and logs this
        process.

        Args:
            df (pandas.Dataframe): User provided data as dataframe.

        Returns:
            tuple:
                Logging information and the created PandasBlock.

        """
        pandas_block = self.convert_to_pandas_block(df)
        info = logger.BlockProcessInfo(
            pandas_block.n_rows(),
            pandas_block.n_columns()
        )
        return info, pandas_block

    def convert_to_pandas_block(self, df):
        """Converts the given dataframe into PandasBlock.

        Args:
            df (pandas.Dataframe): User provided data as dataframe.

        Returns:
            PandasBlock

        """
        return self.df_converter(df)

    def append_to_knowledge(self, pandas_block):
        """Inserts the a PandasBlock object into knowledge database.

        Args:
            pandas_block (PandasBlock): Valid instantiated PandasBlock.

        """
        n_block = self.knowledge.extend(pandas_block)
        pandas_block.origin = (n_block, )


class LearnblockIdentifier:
    """Responsible for identification of valid learnblocks.

    Args:
        settings (BlockProcessingSettings): Defines the behaviour of the
            learnblock identification process.
        density_estimator (MachineLearningModel): Estimates the density
            of timestamps.
        ckmeans (Callable): Performs the optimal kmeans on a 1-dimensional
            list.
    """
    def __init__(self, settings, density_estimator, ckmeans):
        self.settings = settings
        self.cluster_finder = ClusterFinder(
            density_estimator, settings, ckmeans
        )

    @classmethod
    def _column_pairs(cls):
        """Yiels the possible relationships for valid learnblocks.

        Yields:
            tuple

        """
        yield "Sigma", "Z"
        # yield "T", "Sigma"
        # yield "T", "Z"

    def identify(self, block):
        """Identify the biggest learnbock within the given PandasBlock.

        Args:
            block (PandasBlock): Instantiated PandasBlock.

        Returns:
            PandasBlock:
                Subset of the given PandasBlock.

        """
        biggest_learn_block = None
        biggest_block_size = 0

        for pair in LearnblockIdentifier._column_pairs():
            for possible_learnblock in self._identify_relatives(block, *pair):
                if self._is_learn_block(possible_learnblock.n_rows()):
                    if possible_learnblock.n_rows() > biggest_block_size:
                        biggest_learn_block = possible_learnblock
                        biggest_learn_block.relationship = pair

        if biggest_learn_block is None:
            return (
                logger.LearnblockIdentificationInfo(
                    LearnblockIdentificationInfo.State.DISCARDED
                ), None, self.get_halde(biggest_learn_block, block))

        else:
            return (
                logger.LearnblockIdentificationInfo(
                    LearnblockIdentificationInfo.State.IDENTIFIED,
                    biggest_learn_block.n_rows(),
                    biggest_learn_block.n_columns(),
                    biggest_learn_block.relationship
                ),
                biggest_learn_block,
                self.get_halde(biggest_learn_block, block)
            )

    def _is_learn_block(self, block_size):
        """Check if the given block size is enough to be classified as a
        learnblock.

        Args:
            block_size (int): Number of samples in a block.

        Returns:
            bool:
                Returns True if the size is enough for a learnblock else False.

        """
        return block_size >= self.settings.learn_block_minimum

    def _identify_relatives(self, block, *args):
        """Find relatives within the given block. And used them to coconstruct
        a new block.

        Args:
            block (PandasBlock): Instantiated PandasBlock.
            *args: Relationship to be used.

        Yiels:
            PandasBlock:
                Constructed from relatives.

        """
        already_seen = set()
        for value_pair in block.get_duplicated_pairs(args[0], args[1]):
            if value_pair not in already_seen:
                already_seen.add(value_pair)

                kw = {args[0]: value_pair[0], args[1]: value_pair[1]}
                if args[0] == "Sigma" and args[1] == "Z":
                    for lb_cand in self._get_sigma_zeta_relatives(block, **kw):
                        yield lb_cand
                else:
                    yield block.construct_from_two_pairs(**kw)

    def _get_sigma_zeta_relatives(self, block, **kw):
        """Find Sigma Z relatives within the given block and used them to
        construct a new block.

        Args:
            block (PandasBlock): Instantiated PandasBlock.
            **kw: Sigma Z relative.

        Yields:
            PandasBlock:
                Possible learnblock with Sigma Z relatives.

        """
        relatives = block.construct_from_two_pairs(**kw)
        time_column = relatives.get_column("T")
        clusters = self.cluster_finder.find(time_column)
        for time_values in clusters:
            yield relatives.new_block_from(time_values, time_column=True)

    def get_halde(self, learnblock, block):
        """Get block subset which is not part of the learnblock.

        Args:
            learnblock (PandasBlock): Biggest valid found learnblock.
            block (PandasBlock): User provided block.

        Returns:
            pandas.Dataframe:
                Subset which is not part of learnblock.

        """
        if learnblock is None:
            return block.df
        else:
            origin_block = set(block.indices())
            lb_index = set(learnblock.indices())
            halde_indices = list(origin_block.difference(lb_index))
            return block.new_block_from(halde_indices, index=True).df


class ClusterFinder:
    """Responsible for finding the optimal number of clusters within
    timestamps.

    Args:
        density_estimator (MachineLearningModel):
            Estimates the density of the timestamps.
        settings (BlockProcessingSettings):
            Defines the behavior of the cluster finding process.
        ckmeans (Callable):
            Interface to the ckmeans algorithm.

    """
    def __init__(self, density_estimator, settings, ckmeans):
        self.density_estimator = density_estimator
        self.settings = settings
        self.ckmeans = ckmeans

    def find(self, time_column):
        """Find the optimal number of cluster in the given timestamps.

        Args:
            time_column (list): List with timestamps as integers.

        Returns:
            list:
                List timestamp clusters.

        """
        density = self.density_estimator.density(time_column)
        changes = self.count_threshold_changes(density)
        n_changes = self.count_changes(changes)
        return self.ckmeans(time_column, n_changes)

    def find_valid_learnblock_cluster(self, time_column):
        """Find the optimal number of clusters in the given timestamps,
        but every cluster should contain enough timestamps to be classified
        as a valid learnblock.

        Args:
            time_column (list): List with timestamps as integers.

        Yields:
            list:
                Timestamps that form a valid learnblock.

        """
        density = self.density_estimator.density(time_column)
        changes = self.count_threshold_changes(density)
        n_changes = self.count_changes(changes)
        cluster = self.ckmeans(time_column, n_changes)
        for c in cluster:
            if (len(c)/len(time_column)) > self.settings.min_category_size:
                yield c

    def count_threshold_changes(self, density):
        """Counts how many times the density in a given time stamp
        exceeds the threshold value.

        Args:
            density (Iterable): Density estimation over the timestamps.

        Returns:
            List:
                List of booleans. True indicates the density exceeded the
                threshold otherwise False.

        """
        changes = list()
        max_dens = max(density)
        for index, dens in enumerate(density):
            if dens > max_dens*self.settings.sigma_zeta_cutoff:
                changes.append(True)
            else:
                changes.append(False)
        return changes

    def count_changes(self, changes):
        """Count the number of clusters to be found by ckmeans.

        Consecutive True, False or False, True indicates the beginning or
        end of a cluster.


        Args:
            changes (list): List of booleans.

        Returns:
            int:
                Number of clusters.

        """
        count_changes = 0
        for i, j in zip_longest(changes[0::1], changes[1::1]):
            if (i, j) == (True, False) or (i, j) == (False, True):
                count_changes += 1

        if count_changes == 0:
            return 1

        return count_changes+1
