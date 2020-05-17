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


"""Define the base class for all deconstuction types.

"""


from collections import namedtuple

from conML.shared.logger import DeconstructionInfo


class Abstract:
    """Baseclass for all other deconstruction classes.

    Args:
        level (int):
            Level specifiction on which the deconstruction is performed.
        knowledge (KnowledgeDatabase):
            Deconstruction changes writting to this database.
        settings (DeconstructionSettings):
            Controlls the behavior of the deconstruction.
        reconstructor (Reconstructor):
            Performs the reconstruction step within the deconstruction.
        pragmatic (PragmaticMachineLearningModel):
            Model which should be deconstructed.
        relatives (list): List of all relatives of pragmatic.
        result_queue (deque):
            Used as a container for all generated DeconstructionInfo.

    """
    def __init__(self, level, knowledge, settings, reconstructor, pragmatic,
                 relatives, result_queue):
        self.level = level
        self.knowledge = knowledge
        self.settings = settings
        self.reconstructor = reconstructor
        self.pragmatic = pragmatic
        self.relatives = relatives
        self.result_queue = result_queue
        self.block = pragmatic.trained_with(knowledge)

        self.relative_block = None

    def run(self):
        """Start the deconstruction.

        """
        for relative in self.relatives:
            if relative in self.knowledge:
                self.relative_block = relative.trained_with(self.knowledge)

                log = self.log_info(relative, self.pragmatic)
                self.deconstruct(relative, log)
                self.result_queue.append(log)

                if (log.state == DeconstructionInfo.State.DECONSTRUCTED
                        and self.settings.deconst_mode == "minimal"):
                    return

    def deconstruct(self, *args, **kwargs):
        raise NotImplementedError

    def log_info(self, relative, pragmatic):
        """Build a container for holding important information during
        deconstruction.

        Args:
            relative (PragmaticMachineLearningModel):
                Relative of the model, which should be deconstructed.
            pragmatic (PragmaticMachineLearningModel):
                Model, which should be deconstructed.

        Returns:
            DeconstructionInfo

        """
        try:
            relationship = self.RELATION
        except AttributeError:
            relationship = None

        return DeconstructionInfo(
            relative=relative,
            pragmatic=pragmatic,
            relationship=relationship
        )

    def push_ids_to_reconstructor(self, n_ids):
        """Push valid identifier to the reconstructor.

        Args:
            n_ids (int): Amount of how many valid identifier should be
                generated.

        """
        for _ in range(n_ids):
            identifier = self.knowledge.get_next_identifier(self.level)
            self.reconstructor.identifier_queue.put(identifier)

    def model_disposal(self, pragmatic, relative):
        """Remove models depending on the chosen deconstructon strategy.

        Args:
            pragmatic (PragmaticMachineLearningModel):
                Model, which should be deconstructed.
            relative (PragmaticMachineLearningModel):
                Relative of the model, which should be deconstructed.

        Returns:
            namedtuple:
                Contained which models are deleted and inserted.

        """
        Disposal = namedtuple("Disposal", "inserted, deleted")
        if self.settings.deconst_strategy == "conservative":
            if pragmatic != self.pragmatic:
                deleted = self.knowledge.remove_dependent(pragmatic)
            else:
                deleted = [pragmatic]

            return Disposal(deleted=deleted, inserted=[])

        elif self.settings.deconst_strategy == "integrative":
            self.knowledge.insert(pragmatic)
            return Disposal(inserted=[pragmatic], deleted=[])

        elif self.settings.deconst_strategy == "oppurtunistic":
            if self.block.n_rows() > self.relative_block.n_rows():
                deleted = self.knowledge.remove_dependent(relative)
                self.knowledge.insert(pragmatic)
                return Disposal(inserted=[pragmatic], deleted=deleted)

            else:
                if pragmatic != self.pragmatic:
                    deleted = self.knowledge.remove_dependent(pragmatic)
                else:
                    deleted = [pragmatic]
                self.knowledge.insert(relative)
                return Disposal(inserted=[relative], deleted=deleted)

    def calculate_reliability(self, predicts_a, predicts_b):
        """Calculate the reliability between two voters.

        Args:
            predicts_a (Iterable): Containing the first votes.
            predicts_b (Iterable): Containing the second votes.

        Returns:
            float:
                Calculated reliability value, between -1 and 1.

        """
        predicts_b = [int(i) for i in predicts_b]
        predicts_a = [int(i) for i in predicts_a]
        predictions = [predicts_b, predicts_a]
        return self.reconstructor.krippendorff_alpha(predictions)

    def model_fusion(self, relative):
        """Combine the PragmaticMachineLearningModel, which is currently
        in deconstruction with one of this relatives.

        Args:
            relative (PragmaticMachineLearningModel):
                Relative of the model, which should be deconstructed.

        Returns:
            MetaData:
                Combined meta data of two PragmaticMachineLearningModels.

        """
        self.push_ids_to_reconstructor(n_ids=1)
        return self.pragmatic.fusion(
            relative,
            self.level,
            self.reconstructor.identifier_queue.get()
        )
