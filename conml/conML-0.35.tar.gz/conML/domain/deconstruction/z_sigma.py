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


"""Define the Z-Sigma deconstruction.

"""


from conML.domain.deconstruction.abstract import Abstract
from conML.shared.logger import DeconstructionInfo


__all__ = (
    "ZSigmaDeconstructor",
)


class ZSigmaDeconstructor(Abstract):
    """

    Notes:
        Please see help(Abstract) for more info.

    """
    RELATION = ("Sigma", "Z")
    MIN_N_FEATURE = 2

    def __init__(self, *args):
        super().__init__(*args)

    def deconstruct(self, relative, log):
        """Run the ZSigma deconstruction.

        Args:
            relative (PragmaticMachineLearningModel): Relative of the currently
                deconstructed model.
            log (DeconstructionInfo): Container holding information
                of the deconstruction process.

        Returns:
            DeconstructionInfo:
                Logging information.

        """
        if self.time_constraint(relative):
            overlapping = self.identify_overlapping_features()
            if self.column_constraint(overlapping):
                meta_model = self.model_fusion(relative)

                if self.settings.force_time_expansion:
                    return self.reconstructor.get_pml(meta_model,
                                                      overlapping,
                                                      self.pragmatic.model)
                else:
                    return self.reconstructing(overlapping,
                                               meta_model,
                                               relative,
                                               log)

        return self.deconstruction_failed(relative, log)

    def time_constraint(self, relative):
        """Check if the relative is satisfying the time constraint.

        Args:
            relative (PragmaticMachineLearningModel): Relative model.

        Returns:
            bool:
                True, if the time contraint is fullfilled.

        """
        if self.settings.deconst_max_distance_t == 0.0:
            return self.overlapping_time(self.pragmatic, relative)

        elif 0.0 < self.settings.deconst_max_distance_t < 1.0:
            return self.enclosing_time(self.pragmatic, relative)

        elif self.settings.deconst_max_distance_t == 1.0:
            return True

    def overlapping_time(self, prag_model, relative_model):
        """Check if the time values between two pragmtic machine learning
        models overlap.

        Args:
            prag_model (PragmaticMachineLearningModel): Model to deconstruct.
            relative_model (PragmaticMachineLearningModel): Relative.

        Returns:
            bool:
                True, if time stamps overlapping else False.

        """
        return (relative_model.min_timestamp >= prag_model.max_timestamp or
                prag_model.min_timestamp >= relative_model.max_timestamp)

    def enclosing_time(self, prag_model, relative_model):
        """Check if the time values of the deconstructing model enclose
        the relative model.


        Args:
            prag_model (PragmaticMachineLearningModel): Model to deconstruct.
            relative_model (PragmaticMachineLearningModel): Relative.

        Returns:
            bool:
                True, if time stamps of deconstructed model enclose
                the relative time stamps.

        """
        m_dash_max_time = max(prag_model.max_timestamp,
                              relative_model.max_timestamp)
        m_dash_min_time = min(prag_model.min_timestamp,
                              relative_model.min_timestamp)
        relative_m_dash_time = self.settings.deconst_max_distance_t*(
                m_dash_max_time-m_dash_min_time)

        return (
            (relative_model.min_timestamp - prag_model.max_timestamp) <
            relative_m_dash_time or
            (prag_model.min_timestamp - relative_model.max_timestamp) <
            relative_m_dash_time
        )

    def identify_overlapping_features(self):
        """Build learnblock on basis of the feature intersection of two other
        learnblocks.

        Returns:
            PandasBlock:
                Learnblock

        """
        return self.block.same_features_fusion(self.relative_block)

    def column_constraint(self, overlapped_block):
        """Check if the new learnblock has enough features.

        Args:
            overlapped_block (PandasBlock): Learnblock.

        Returns:
            bool:
                Learnblock with more than 2 features.

        """
        return overlapped_block.n_columns(effective=True) >= self.MIN_N_FEATURE

    def reconstructing(self, overlapped_block, meta_model, relative, log):
        """Reconstruct the new combined pragmatic machine learning
        model.

        Args:
            overlapped_block (PandasBlock): Learnblock with more than 2
                Features.
            meta_model (MetaData): Meta data of combined pragmatic machine
                learning.
            relative (PragmaticMachineLearningModel): Relative.
            log (DeconstructionInfo): Logging information.

        Returns:
            DeconstructionInfo:
                Holds information about T Sigma deconstruction.

        """
        _, pragmatics, _ = self.reconstructor.reconstruct(
            self.level, overlapped_block, which_models=None,
            meta=meta_model, all_m=True)

        if pragmatics:
            winners = {m.accuracy: m for m in pragmatics}
            winner = winners[max(winners.keys())]
            deleted = self.knowledge.remove_dependent(relative)
            self.knowledge.insert(winner)
            log.reconstructed_info.append(winner)
            log.inserted.append(winner)
            log.deleted.extend(deleted)
            log.state = DeconstructionInfo.State.DECONSTRUCTED
            return log

        else:
            return self.deconstruction_failed(relative, log)

    def deconstruction_failed(self, relative, log):
        """Fill the DeconstrucionInfo object if the T Sigma deconstruction
        failed.

        Args:
            relative (PragmaticMachineLearningModel): Relative.
            log (DeconstructionInfo): Logging info.

        Returns:
            DeconstructionInfo

        """
        modification = self.model_disposal(
            self.pragmatic,
            relative,
        )
        log.inserted.extend(modification.inserted)
        log.deleted.extend(modification.deleted)
        log.state = DeconstructionInfo.State.FAILED
        return log
