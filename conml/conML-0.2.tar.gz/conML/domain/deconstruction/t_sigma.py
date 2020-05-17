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


"""Define the T-Sigma deconstruction.

"""


import sys
from dataclasses import dataclass
from queue import Empty
from multiprocessing import Process

from conML.shared.logger import DeconstructionInfo
from conML.domain.deconstruction.abstract import Abstract


__all__ = (
    "TSigmaDeconstructor",
    "Start",
    "Upgrade",
    "Apply",
    "Clean",
    "Exit"
)


@dataclass
class Start:
    """Serializable command, indicating to start the deconstruction. """
    level: int
    relatives: list
    pragmatic: object


@dataclass
class Upgrade:
    """Serializable command, indicating to upgrade the deconstructed models. """
    deletes: set


@dataclass
class Apply:
    """Serializable command, indicating to write down the changes. """
    pass


@dataclass
class Clean:
    """Serializable command, indicating to clean the temporary
    deconstruction changes.

    """
    pass


@dataclass
class Exit:
    """Serializable command, indicating to exit the deconstruction. """
    pass


class TSigmaDeconstructor(Abstract, Process):
    """Class performs the T Sigma deconstruction process.

    Args:
        build_new_learnblock (Callable):
            Function for building new PandasBlocks.
        krippendorf (Callable):
            Function for calculating krippendorff-alpha.
        knowledge (KnowledgeDatabase):
            Deconstruction changes writting to this database.
        settings (DeconstructionSettings):
            Controlls the behavior of the deconstruction.
        general_setitngs (GeneralSettings):
            Controlls the behavior of the general framework.
        inputs (Queue):
            Contains the inputs for the background deconstruction.
        outputs (Queue):
            Contained the outputs of the background deconstruction.
        upgrade_event (Event):
            Signals that the upgrades on the temporary changes are
            performed.
        apply_event (Event):
            Signals that the deconstructed objects are pushed to the
            output queue.
        clear_event (Event):
            Signals that the input and output queue is empty.

    """
    RELATION = ("Sigma", "T")

    def __init__(self, build_new_learnblock, krippendorf, knowledge, settings,
                 general_setitngs, inputs=None, outputs=None,
                 upgrade_event=None, apply_event=None, clear_event=None):
        super(Process, self).__init__(name="TSigmaBackgroundProcess")

        self.build_new_learnblock = build_new_learnblock
        self.krippendorf = krippendorf
        self.knowledge = knowledge
        self.settings = settings
        self.general_settings = general_setitngs
        self.temp_changes = []
        self.block = None
        self.relative_block = None

        # Used during parallelism
        self.inputs = inputs
        self.outputs = outputs
        self.upgrade_event = upgrade_event
        self.apply_event = apply_event
        self.clear_event = clear_event

    def run(self):
        """Performs T Sigma deconstruction in the background.

        """
        while True:
            command = self.inputs.get()

            if isinstance(command, Start):
                if not self.block:
                    self.block = command.pragmatic.trained_with(self.knowledge)

                for relative in command.relatives:
                    self.relative_block = relative.trained_with(self.knowledge)
                    log = self.log_info(relative, command.pragmatic)
                    self.deconstruct(command.level, relative, command.pragmatic,
                                     log)

            elif isinstance(command, Upgrade):
                self.upgrade(command.deletes)
                self.upgrade_event.set()

            elif isinstance(command, Apply):
                self.apply()
                self.apply_event.set()

            elif isinstance(command, Clean):
                self.clean()
                self.clear_event.set()

            elif isinstance(command, Exit):
                sys.exit(0)

    def run_serial(self, level, relatives, pragmatic, result_deque):
        """Performs the T Sigma deconstruction.

        Args:
            level (int):
                Level specification on which the deconstruction is performed.
            relatives (PragmaticMachineLearningModel):
                Relative of the model, which should be deconstructed.
            pragmatic (PragmaticMachineLearningModel):
                Model which should be deconstructed.
            result_deque (deque):
                Used as a container for all generated DeconstructionInfo.

        """
        self.block = pragmatic.trained_with(self.knowledge)

        for relative in relatives:
            self.relative_block = relative.trained_with(self.knowledge)
            log = self.log_info(relative, pragmatic)
            self.deconstruct(level, relative, pragmatic, log)

        for log, level, lb in self.temp_changes:
            ####################################################################
            self.knowledge.insert(pragmatic)
            log.inserted.append(pragmatic)
            ####################################################################

            result_deque.append((log, level, lb))

            if (log.state == DeconstructionInfo.State.DECONSTRUCTED
                    and self.settings.deconst_mode == "minimal"):
                self.temp_changes.clear()
                break

    def upgrade(self, deletions):
        """Remove invalid demporary deconstructions.

        Args:
            deletions (Iterable): List wich models, which have been
                removed during the complete deconstruction.

        """
        to_delete = []
        for log, level, learnblock in self.temp_changes:
            if set(deletions).intersection(set(learnblock.origin)):
                to_delete.append((log, level, learnblock))

        for pair in to_delete:
            self.temp_changes.remove(pair)

    def apply(self):
        """Push temporary deconstruction to the output queue.

        """
        for log, level, lb in self.temp_changes:
            self.outputs.put((log, level, lb))
            if (log.state == DeconstructionInfo.State.DECONSTRUCTED
                    and self.settings.deconst_mode == "minimal"):
                break

    def clean(self):
        """Clean the temporary changes from invalid changes.

        """
        self.temp_changes.clear()
        while not self.inputs.empty():
            try:
                self.inputs.get(block=False, timeout=None)
            except Empty:
                continue

        while not self.outputs.empty():
            try:
                self.outputs.get(block=False, timeout=None)
            except Empty:
                continue

    def deconstruct(self, level, relative, pragmatic, log):
        """Run the TSigma deconstruction.

        Args:
            level (int): Level on which deconstruction is performed.
            relative (PragmaticMachineLearningModel): Relative model.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            log (DeconstructionInfo): Logging information.

        """
        if self.level_constraint(level):
            overlapping = self.identify_overlapping_block(self.block)
            if self.row_and_reliability_contraints(overlapping):
                block = self.prepare_higher_block(pragmatic, relative, overlapping)
                log.state = DeconstructionInfo.State.DECONSTRUCTED
                log.new_learnblock = block
                self.temp_changes.append((log, level + 1, block))

    def level_constraint(self, level):
        """Check if learnblock is not pushed over the maximal level.

        Args:
            level (int): Level where to push the learnblock.

        Returns:
            bool:
                True, if the maximal level is not reached else False.

        """
        return level < self.general_settings.highest_level

    def identify_overlapping_block(self, block):
        """Build learnblock on basis of overlapping timestamps.

        Args:
            block (PandasBlock): Learnblock on which the deconstructing model
                was trained.

        Returns:
            PandasBlock:
                Learnblock with overlapping time stamps.

        """
        overlapped_block = block.get_overlapping_on_timestamps(
            self.relative_block
        )
        return overlapped_block

    def row_and_reliability_contraints(self, block):
        """Check if all contrainsts are satisfied to push the learnblock
        to the next level.

        Args:
            block (PandasBlock): Learnblock on which the deconstructed model
                was trained.

        Returns:
            bool:
                True, if alle contraints are satisfied.

        """
        return self.row_constraint(block) and self.reliability_constraint(block)

    def row_constraint(self, block):
        """Check if the block has enough samples.

        Args:
            block (PandasBlock): Possible learnblock.

        Returns:
            bool:
                True if the block has enough samples to be considered a
                learnblock else False.

        """
        return len(block) >= self.settings.learn_block_minimum

    def reliability_constraint(self, block):
        """Check if the labels of the block satisfy the minimum
        inter-reliability.

        Args:
            block (PandasBlock): Possible learnblock.

        Returns:

        """
        predictions = [
            [int(i) for i in block.get_column("Z")],
            [int(i) for i in block.get_column("Z_other")]
        ]
        alpha = self.krippendorf(predictions)
        alpha_systematic = alpha < 0
        alpha_weak_reliability = (0 <= alpha < self.settings.min_reliability)
        return (self.settings.allow_weak_reliability and
                alpha_weak_reliability) or alpha_systematic

    def prepare_higher_block(self, pragmatic, relative, overlapping):
        """Build learnblock for the next level.

        Args:
            pragmatic (PragmaticMachineLearnignModel): Model to deconstruct.
            relative (PragmaticMachineLearningModel): Relative model.
            overlapping (PandasBlock): Learnblock that is valid to be pushed
                to the next level.

        Returns:
            PandasBlock

        """
        overblock = self.build_new_learnblock(
            values=list(zip(
                overlapping.get_column("Z"),
                overlapping.get_column("Z_other"),
                overlapping.get_column("T"),
                ("\"\"" for _ in range(overlapping.n_rows())),
                ("\"\"" for _ in range(overlapping.n_rows())))),
            columns=(pragmatic.uid, relative.uid, "T", "Sigma", "Z"),
            index=[i for i in range(overlapping.n_rows())],
            origin=(pragmatic.uid, relative.uid))
        return overblock
