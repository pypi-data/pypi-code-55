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


"""Define the 'Complete' deconstruction.

"""


from conML.domain.deconstruction.abstract import Abstract
from conML.shared.logger import DeconstructionInfo


__all__ = (
    "CompleteDeconstructor",
)


class CompleteDeconstructor(Abstract):
    """Class performs the 'Complete' deconstruction process.

    Args:
        *args:
        cluster_finder (ClusterFinder): Find cluster within time stamps.
        general_settings (GeneralSettings): Controlls behavior of the
            deconstruction process.
        block_processing_settings (BlockProcessingSettings): Controlls
            the behavior of the deconstruction process.

    """
    RELATION = ("complete", )
    MIN_N_FEATURE = 2

    def __init__(self, *args, cluster_finder, general_settings,
                 block_processing_settings):
        super().__init__(*args)
        self.cluster_finder = cluster_finder
        self.general_settings = general_settings
        self.block_processing_settings = block_processing_settings

    def deconstruct(self, relative, log):
        """Run the 'Complete' deconstruction.

        Args:
            relative (PragmaticMachineLearningModel): Relative model.
            log (DeconstructionInfo): Logging information.

        Returns:
            DeconstructionInfo:
                Logging information.

        """
        if self.feature_constraint():
            meta = self.model_fusion(relative)
            learnblock = self.block.same_features_fusion(self.relative_block)
            return self.reconstructing(meta, learnblock, relative, log)

        elif self.time_stamp_constraint():
            if self.reliability_constraint():
                meta = self.model_fusion(relative)
                learnblock = self.build_block_from_diff_features()
                return self.reconstructing(meta, learnblock, relative, log)
            else:
                modification = self.model_disposal(self.pragmatic, relative)
                log.inserted.extend(modification.inserted)
                log.deleted.extend(modification.deleted)
                log.state = DeconstructionInfo.State.FAILED
                return log

        else:
            self.knowledge.insert(self.pragmatic)
            log.state = DeconstructionInfo.State.FAILED
            log.inserted.append(self.pragmatic)
            return log

    def feature_constraint(self):
        """Check if learnblocks of the recently reconstructed model and
        relative have enough identical features.

        Returns:
            bool:
                True, if learnblocks have enough identical features.

        """
        identical_features = len(
            set(self.block.columns(effective=True)).intersection(
                set(self.relative_block.columns(effective=True))
            )
        )
        return identical_features >= self.MIN_N_FEATURE

    def reconstructing(self, meta, learnblock, relative, log):
        """Reconstruct the new combined pragmatic machine learning model.

        Args:
            meta (MetaData): Meta data of combined pragmatic machine learning
                model.
            learnblock (PandasBlock): Valid learnblock.
            relative (PragmaticMachineLearningModel): Relative model.
            log (DeconstructionInfo): Logging information.

        Returns:
            DeconstructionInfo:
                Holds information about complete deconstruction.

        """
        if (len(learnblock.columns(effective=True)) < 2 or
                learnblock.n_rows() == 0):
            log.state = DeconstructionInfo.State.FAILED
            modification = self.model_disposal(self.pragmatic, relative)
            log.inserted.extend(modification.inserted)
            log.deleted.extend(modification.deleted)
            return log

        _, pragmatics, _ = self.reconstructor.reconstruct(
            self.level, learnblock, which_models=None,
            meta=meta, all_m=True)

        if pragmatics:
            winners = {m.accuracy: m for m in pragmatics}
            winner = winners[max(winners.keys())]
            log.reconstructed_info.append(winner)
            deleted = self.knowledge.remove_dependent(relative)
            self.knowledge.insert(winner)
            log.inserted.append(winner)
            log.deleted.extend(deleted)
            log.state = DeconstructionInfo.State.DECONSTRUCTED
            return log

        else:
            self.model_differentiation(learnblock, relative, log)

    def model_differentiation(self, block, relative_model, log):
        """Try to find sub models within the failed reconstructed model during
        complete deconstruction.

        Args:
            block (PandasBlock): Valid learnblock.
            relative_model (PragmaticMachineLearningModel): Relative model.
            log (DeconstructionInfo): Logging information.

        Returns:
            DeconstructionInfo

        """
        time_column = block.get_column("T")
        clusters = list(
            self.cluster_finder.find_valid_learnblock_cluster(
                time_column
             )
        )

        for time_values in clusters:
            learnblock = block.new_block_from(time_values, time_column=True)

            self.push_ids_to_reconstructor(
                len(self.reconstructor.ml_models) * len(clusters)
            )
            _, pragmatics, _ = self.reconstructor.reconstruct(
                self.level, learnblock, which_models=None,
                meta=None, all_m=True)
            if pragmatics:
                winners = {m.accuracy: m for m in pragmatics}
                winner = winners[max(winners.keys())]
                log.reconstructed_info.append(winner)
                log.inserted.append(winner)
                self.knowledge.insert(winner)

        if log.inserted:
            log.state = DeconstructionInfo.State.DECONSTRUCTED
            return log

        else:
            deleted = self.knowledge.remove_dependent(relative_model)
            log.deleted.extend(deleted)
            log.state = DeconstructionInfo.State.DECONSTRUCTED
            return log

    def time_stamp_constraint(self):
        """Check if recently reconstructed model has enough identical
        timestamps as his relative.

        Returns:
            bool:
                True, if the timestamp constraint is satisfied else False.

        """
        overlapped = self.block.get_overlapping_on_timestamps(
            self.relative_block)
        if (overlapped.n_rows() >=
                self.block_processing_settings.learn_block_minimum):
            return True

        else:
            return False

    def reliability_constraint(self):
        """Check if learnlock labels of recently reconstructed model satisfy
        the inter-reliability constaint with the relative.

        Returns:
            bool:
                True, if learnblocks labels of both models have high enough
                inter-reliability.

        """
        overlapped = self.block.get_overlapping_on_timestamps(self.relative_block)
        overlapped.drop_columns(
            list(set(overlapped.columns()).difference({"Z", "Z_other"}))
        )
        reliability = self.calculate_reliability(
            overlapped.get_column("Z"),
            overlapped.get_column("Z_other"))
        return reliability >= self.settings.min_reliability

    def build_block_from_diff_features(self):
        """Build learnblock on the basis of different features from
        recently reconstructed model and his relative.

        Returns:
            PandasBlock

        """
        overlapped = self.block.get_overlapping_on_timestamps(self.relative_block)
        if (overlapped.n_columns() == 0 or overlapped.n_rows() == 0 or
                len(overlapped.columns(effective=True)) < 2):
            return overlapped

        dont_drop = (
            set(self.block.columns(effective=True)).symmetric_difference(
                set(self.relative_block.columns(effective=True)))
        )

        if self.settings.deconst_strategy == "conservative":
            z_column = "Z"

        elif self.settings.deconst_strategy == "integrative":
            z_column = "Z_other"

        else:
            # self.settings.deconst_mode == "oppurtunistic":
            if self.block.n_rows() > self.relative_block.n_rows():
                z_column = "Z"
            else:
                z_column = "Z_other"

        overlapped.drop_columns(
            list(
                set(overlapped.columns()).difference(
                    set(dont_drop).union(
                        {"T", "Sigma", z_column}))
            )
        )
        overlapped.rename_column(z_column, "Z")
        overlapped.reorder_columns(list(dont_drop) + ["T", "Sigma", "Z"])
        overlapped.origin = tuple(set(self.block.origin + self.relative_block.origin))

        return overlapped
