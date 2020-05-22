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


"""Define the deconstruction process.

"""

from collections import deque
from multiprocessing import Event, Manager
from queue import Empty

from conML.shared.logger import DeconstructionInfo
from conML.domain.deconstruction.z_sigma import ZSigmaDeconstructor
from conML.domain.deconstruction.complete import CompleteDeconstructor
from conML.domain.deconstruction.t_sigma import (
    TSigmaDeconstructor,
    Start,
    Apply,
    Upgrade,
    Clean,
    Exit
)


__all__ = (
    "Deconstructor",
)


class AbstractDeconstructor:
    """Responsible for defining basis functions that are used in the
    most deconstructions.

    Args:
        general_settings (GeneralSettings): Controlls the behavior of
            the deconstructions.
        block_processing_settings (BlockProcessingSettings): Controlls the
            behavior of deconstruction.
        deconstruction_settings (DeconstructionSettings): Controlls the
            behavior of deconstruction.
        reconstructor (Reconstructor): Reconstructor.
        learnblock_constructor (Callable): Build learnblocks.
        cluster_finder (ClusterFinder): Find cluster within time stamps.


    """
    def __init__(self, general_settings, block_processing_settings,
                 deconstruction_settings, reconstructor,
                 learnblock_constructor, cluster_finder):
        self.general_settings = general_settings
        self.block_processing_settings = block_processing_settings
        self.settings = deconstruction_settings
        self.reconstructor = reconstructor
        self.learnblock_constructor = learnblock_constructor
        self.cluster_finder = cluster_finder
        self.tsigma_beamer = deque()

    def __str__(self):
        return "\n".join([
                str(self.settings),
                str(self.reconstructor)
            ]
        )

    def __repr__(self):
        return ", ".join([
                "{}".format(repr(self.settings)),
                "{}".format(repr(self.reconstructor))
            ]
        )

    def to_dict(self):
        return {
            "general_settings": self.general_settings,
            "block_processing_settings": self.block_processing_settings,
            "deconstruction_settings": self.settings,
            "reconstructor": self.reconstructor,
            "learnblock_constructor": self.learnblock_constructor,
            "cluster_finder": self.cluster_finder
        }

    def deconstruct(self, *args, **kwargs):
        raise NotImplementedError

    def find_relatives(self, database, pragmatic):
        """Find all relatives of the given model in knowledge database.

        Args:
            database (KnowledgeDatabase): Database for
                PragmaticMachineLearningModels.
            pragmatic (PragmaticMachineLearningModel): From which the relatives
                to find.

        Yields:
            PragmaticMachineLearningModel:
                Relative.

        """
        relative_finder = database.observer[0]

        complete_relatives = relative_finder.find(
            tuple(["complete", ]), pragmatic,
            self.settings.deconst_full_tolerance)

        t_sigma_relatives = relative_finder.find(
            tuple(["T", "Sigma"]), pragmatic,
            self.settings.deconst_full_tolerance)

        sigma_z_relatives = relative_finder.find(
            tuple(["Sigma", "Z"]), pragmatic,
            self.settings.deconst_full_tolerance)

        yield complete_relatives

        t_sigma_relatives = [m for m in t_sigma_relatives
                             if m in relative_finder]

        yield t_sigma_relatives

        sigma_z_relatives = [m for m in sigma_z_relatives
                             if m in relative_finder]
        yield sigma_z_relatives

    def clean_ts_queue(self, deleted):
        """Remove invalid models from  T-Sigma queue.

        Args:
            deleted (list): List of deleted PragmaticMachineLearningModels
                in complete deconstructino process.

        """
        queue_copy = self.tsigma_beamer.copy()
        for level, lb in queue_copy:
            for model in deleted:
                if model in lb.origin:
                    self.tsigma_beamer.remove((level, lb))


class SerialDeconstructor(AbstractDeconstructor):
    """Encapsulates the logic for the seriel deconstruction.

    Note:
        Please see help(AbstractDeconstructor) for more info!

    """
    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()

    def deconstruct(self, level, pragmatic, database):
        """Start the deconstruction process.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Recently reconstructed
                model.
            database (KnowledgeDatabase): Database to store models.

        Yield:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        relatives = iter(self.find_relatives(database, pragmatic))

        yield self.run_complete_deconstruction(
            level, pragmatic, database, next(relatives)
        )

        yield self.run_t_sigma_deconstruction(
            level, pragmatic, database, next(relatives)
        )

        yield self.run_sigma_z_deconstruction(
            level, pragmatic, database, next(relatives)
        )

    def run_complete_deconstruction(self, level, pragmatic, database, relatives):
        """Perform complete deconstruction.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            database (KnowledgeDatabase): Database to store models.
            relatives (list): List of 'complete' relatives.

        Yield:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        if relatives:
            result_deque = deque()
            CompleteDeconstructor(
                level, database, self.settings, self.reconstructor, pragmatic,
                relatives, result_deque, cluster_finder=self.cluster_finder,
                general_settings=self.general_settings,
                block_processing_settings=self.block_processing_settings
            ).run()

            for log in result_deque:
                self.clean_ts_queue(log.deleted)
                yield log

    def run_t_sigma_deconstruction(self, level, pragmatic, database, relatives):
        """Perform T Sigma deconstruction.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            database (KnowledgeDatabase): Database to store models.
            relatives (list): List of 'T Sigma' relatives.

        Yield:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        if relatives:
            result_deque = deque()
            TSigmaDeconstructor(
                self.learnblock_constructor,
                self.reconstructor.krippendorff_alpha, database, self.settings,
                self.general_settings
            ).run_serial(level, relatives, pragmatic, result_deque)

            for log, level_, learnblock in result_deque:
                self.tsigma_beamer.append((level_, learnblock))
                yield log

    def run_sigma_z_deconstruction(self, level, pragmatic, database, relatives):
        """Perform Sigma Z deconstruction.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            database (KnowledgeDatabase): Database to store model.
            relatives (list): List of Sigma Z relatives.

        Yield:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        if relatives:
            result_deque = deque()
            ZSigmaDeconstructor(
                level, database, self.settings, self.reconstructor, pragmatic,
                relatives, result_deque
            ).run()

            for log in result_deque:
                self.clean_ts_queue(log.deleted)
                yield log


class ParallelDeconstructor(AbstractDeconstructor):
    """Encapsulates the logic for the parallel deconstruction.

    Note:
        Please help(AbstractDeconstructor) for more info!

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Used if parallelization is on
        self.tsigma_process = None
        self.tsigma_inputs = None
        self.tsigma_outputs = None
        self.upgrade_event = None
        self.apply_event = None
        self.clear_event = None

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()

    def deconstruct(self, level, pragmatic, database):
        """Start the deconstruction process.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Recently reconstructed
                model.
            database (KnowledgeDatabase): Database to store models.

        Yields:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        relatives = iter(self.find_relatives(database, pragmatic))
        complete_relatives = next(relatives)
        t_sigma_relavites = next(relatives)

        if t_sigma_relavites:
            self.start_background_tsigma(database)
            self.tsigma_inputs.put(Start(level=level,
                                         relatives=t_sigma_relavites,
                                         pragmatic=pragmatic))
        if complete_relatives:
            yield self.run_complete_deconstruction(
                level, pragmatic, database, complete_relatives
            )

        if t_sigma_relavites:
            yield self.run_t_sigma_deconstruction(database, pragmatic)

        yield self.run_sigma_z_deconstruction(
            level, pragmatic, database, next(relatives)
        )

    def start_background_tsigma(self, database):
        """Start the T Sigma deconstruction in a separate process.

        Args:
            database (KnowledgeDatabase): Database to store models.

        """
        if not self.tsigma_process:
            m = Manager()
            self.tsigma_inputs = m.Queue()
            self.tsigma_outputs = m.Queue()
            self.upgrade_event = Event()
            self.apply_event = Event()
            self.clear_event = Event()
            self.tsigma_process = TSigmaDeconstructor(
                self.learnblock_constructor,
                self.reconstructor.krippendorff_alpha, database, self.settings,
                self.general_settings, self.tsigma_inputs, self.tsigma_outputs,
                self.upgrade_event, self.apply_event, self.clear_event)

            self.tsigma_process.daemon = True
            self.tsigma_process.start()

    def run_complete_deconstruction(self, level, pragmatic, database, relatives):
        """Perform complete deconstruction.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            database (KnowledgeDatabase):  Database to store models.
            relatives (list): List of 'complete' relatives.

        Yields:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        result_deque = deque()
        CompleteDeconstructor(
            level, database, self.settings, self.reconstructor, pragmatic,
            relatives, result_deque, cluster_finder=self.cluster_finder,
            general_settings=self.general_settings,
            block_processing_settings=self.block_processing_settings
        ).run()

        for log_info in result_deque:
            if self.tsigma_process:
                self.tsigma_inputs.put(Upgrade(deletes=log_info.deleted))
            yield log_info

    def run_t_sigma_deconstruction(self, knowledge, pragmatic):
        """Perform T Sigma deconstruction.

        Args:
            knowledge (KnowledgeDatabase): Database to store models.
            pragmatic (PragmaticMachineLearningModels): Model to deconstruct.

        Yields:
            DeconstructionInfo:
                Logging information about the deconstruction process.

        """
        self.tsigma_inputs.put(Apply())
        self.apply_event.wait()

        while not self.tsigma_outputs.empty():
            try:
                log_info, level, lb = self.tsigma_outputs.get(False)
                self.tsigma_beamer.append((level, lb))
                knowledge.insert(pragmatic)
                log_info.inserted.append(pragmatic)
                yield log_info

            except Empty:
                continue

    def run_sigma_z_deconstruction(self, level, pragmatic, database, relatives):
        """Perform Sigma Z deconstruction.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Model to deconstruct.
            database (KnowledgeDatabase): Databases to store model.
            relatives (list): List of Sigma Z relatives.

        """
        if relatives:
            result_deque = deque()
            ZSigmaDeconstructor(
                level, database, self.settings, self.reconstructor, pragmatic,
                relatives, result_deque
            ).run()

            for log_info in result_deque:
                self.clean_ts_queue(log_info.deleted)
                yield log_info


class Deconstructor:
    """Responsible for holding either SerialDeconstructor or
    ParallelDeconstructor.

    Args:
        mode:
        general_settings (GeneralSettings): Controlls the behavior of the
            deconstruction.
        block_processing_settings (BlockProcessingSettings): Controlls the
            behavior of deconstruction.
        deconstruction_settings (DeconstructionSettings): Controlls the
            behavior of deconstruction.
        reconstructor (Reconstructor): Reconstructor.
        learnblock_constructor (Callable): Build learnblocks.
        cluster_finder (ClusterFinder): Find cluster within time stamps.

    """
    def __init__(self, general_settings, block_processing_settings,
                 deconstruction_settings, reconstructor, learnblock_constructor,
                 cluster_finder):

        self.state = SerialDeconstructor(
            general_settings, block_processing_settings,
            deconstruction_settings, reconstructor,
            learnblock_constructor, cluster_finder)

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return repr(self.state)

    def transit(self):
        """Change the state to SerialDeconstructor or ParallelDeconstructor.

        """
        if type(self.state) == SerialDeconstructor:
            self.state = ParallelDeconstructor(**self.state.to_dict())

        else:
            self.state = SerialDeconstructor(**self.state.to_dict())

    def deconstruct(self, level, pragmatic, database):
        """Start the deconstruction process.

        Args:
            level (int): Level on which the deconstruction is performed.
            pragmatic (PragmaticMachineLearningModel): Recently reconstructed
                model.
            database (KnowledgeDatabase): Database to store models.

        Yields:
            DeconstructionInfo:
                Logging information about the deconstruction.

        """
        try:
            changes_done_status = []
            for decon_type in self.state.deconstruct(level, pragmatic, database):
                for log in decon_type:
                    changes_done_status.append(log.state)
                    yield log

                    # First deconstruction successfully ended and deconst mode
                    # says, end the deconstruction.
                    if (log.state == DeconstructionInfo.State.DECONSTRUCTED and
                            self.deconst_mode == "minimal"):
                        return

                    # The new reconstructed pragmatic model was deleted, so end the
                    # whole deconstruction process.
                    elif pragmatic in log.deleted:
                        return

            if not changes_done_status or all(
                    map(
                        lambda x: x == DeconstructionInfo.State.FAILED,
                        changes_done_status
                    )
            ):
                database.insert(pragmatic)
                yield DeconstructionInfo(pragmatic=pragmatic,
                                         inserted=[pragmatic])
        finally:
            if (isinstance(self.state, ParallelDeconstructor) and
                    self.state.tsigma_process):
                self.state.tsigma_inputs.put(Clean())
                self.state.clear_event.wait()
                self.state.tsigma_inputs.put(Exit())
                self.state.tsigma_process = None

    @property
    def tsigma_beamer(self):
        return self.state.tsigma_beamer

    @property
    def deconst_mode(self):
        return self.state.settings.deconst_mode

    @deconst_mode.setter
    def deconst_mode(self, value):
        self.state.settings.deconst_mode = value

    @property
    def deconst_strategy(self):
        return self.state.settings.deconst_strategy

    @deconst_strategy.setter
    def deconst_strategy(self, value):
        self.state.settings.deconst_strategy = value

    @property
    def deconst_max_distance_t(self):
        return self.state.settings.deconst_max_distance_t

    @deconst_max_distance_t.setter
    def deconst_max_distance_t(self, value):
        self.state.settings.deconst_max_distance_t = value

    @property
    def deconst_full_tolerance(self):
        return self.state.settings.deconst_full_tolerance

    @deconst_full_tolerance.setter
    def deconst_full_tolerance(self, value):
        self.state.settings.deconst_full_tolerance = value

    @property
    def force_time_expansion(self):
        return self.state.settings.force_time_expansion

    @force_time_expansion.setter
    def force_time_expansion(self, value):
        self.state.settings.force_time_expansion = value

    @property
    def allow_weak_reliability(self):
        return self.state.settings.allow_weak_reliability

    @allow_weak_reliability.setter
    def allow_weak_reliability(self, value):
        self.state.settings.allow_weak_reliability = value

    @property
    def learn_block_minimum(self):
        return self.state.settings.learn_block_minimum

    @learn_block_minimum.setter
    def learn_block_minimum(self, value):
        self.state.settings.learn_block_minimum = value

    @property
    def min_reliability(self):
        return self.state.settings.min_reliability

    @min_reliability.setter
    def min_reliability(self, value):
        self.state.settings.min_reliability = value
