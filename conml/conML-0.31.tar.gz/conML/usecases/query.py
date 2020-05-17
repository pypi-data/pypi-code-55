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


"""Defines the queries for the framework.

"""


from copy import copy, deepcopy
from collections import defaultdict, namedtuple
from datetime import datetime
from logging import getLogger, FileHandler, StreamHandler
import multiprocessing
from queue import Empty
import os


from conML.domain.knowledge import KnowledgeDatabase, RelativeFinder
from conML.domain.preprocessing import Source, LearnblockIdentifier
from conML.shared.errors import ModeError
from conML.shared.logger import JsonContainer, HighLevelLearnblockInfo
from conML.shared.parameter import PROTOCOL_LEVEL
from conML.usecases.usecase import Usecase


class ParallelRunner:
    """Responsible for performing a single construction and reconstruction
    in a separate process.

    Args:
        constructor (Constructor): Constructs the learnblock.
        selector (FeatureSelector): Selects the most important features.
        reconstructor (Reconstructor): Reconstructs the learnblock.
        log_queue (Queue): Stores the logging information of the
            performed construction, selection and reconstrution process.

    """

    def __init__(self, constructor, selector, reconstructor, log_queue):
        self.constructor = constructor
        self.selector = selector
        self.reconstructor = reconstructor
        self.log_queue = log_queue
        self.result = defaultdict(list)

    def run(self, level, block):
        """Run the construction and reconstruction on the given block.

        Args:
            level (int):
                Level on which the construction and reconstruction should be
                performed.
            block (PandasBlock): Learnblock.

        Returns:
            defaultdict:
                Maps the reliability to PragmaticMachineLearningModel.

        """
        it = iter(self.constructor.construct(block))
        con_info, labeled_lb = next(it)
        self.log_queue.put(con_info)

        if not labeled_lb:
            return

        sel_info, reduced_lb = self.selector.select(labeled_lb)
        self.log_queue.put(sel_info)

        if not reduced_lb:
            return

        reliability, pragmatics, rec_info = self.reconstructor.reconstruct(
            level, reduced_lb, which_models=None, meta=None)
        self.log_queue.put(rec_info)

        self.result[reliability].extend(pragmatics)
        return self.result


def map_onto(args):
    """Executed by every pool worker.

    Args:
        args (tuple):

    Returns:

    """
    parallel_runner, level, block = args
    return parallel_runner.run(level, block)


class KnowledgeSearcher:
    """Responsible for coordinating the construction, reconstruction and
    deconstruction.

    Args:
        source (Source): Converts given pandas.DataFrames to PandasBlocks.
        identifier (LearnblockIdentifier): Identifies learnblocks within
            PandasBlocks.
        constructor (Constructor): Construct the learnblocks.
        reconstructor (Reconstructor): Reconstructs the learnblocks.
        selector (FeatureSelctor): Selects subset of learnblock features.
        deconstructor (Deconstructor): Deconstruct the reconstructed
            PragmaticMachineLearningModel.
        knowledge_database (KnowledgeDatabase): Database to store models.
        stdout (bool): Indicator if the process should logged to stdout.
        parallel (bool): Indicator if the learning process should utilize
            many processes.
        n_procs (int): Number of processes to utilize.

    """
    def __init__(self,
                 source,
                 identifier,
                 constructor,
                 reconstructor,
                 selector,
                 deconstructor,
                 knowledge_database,
                 stdout,
                 n_procs):
        self.source = source
        self.identifier = identifier
        self.constructor = constructor
        self.reconstructor = reconstructor
        self.selector = selector
        self.deconstructor = deconstructor
        self.knowledge_database = knowledge_database
        self.stdout = stdout
        self.n_procs = n_procs

        self.pool = None
        self.logger = None
        self.json_container = None
        self.log_destination = None
        self.tsigma_beamer = deconstructor.tsigma_beamer

    def __enter__(self):
        self.log_destination = self.__get_log_destination()
        self.logger = self.__get_logger()
        self.json_container = JsonContainer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.json_container.write_down(self.log_destination)

        del self.logger
        del self.json_container
        del self.log_destination
        del self.tsigma_beamer

    def __get_log_destination(self):
        """Create folder to store logs.

        Returns:
            str:
                Logging destination.

        """
        home_folder_path = os.path.expanduser("~")
        cml_folder = ".conML"
        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        log_dir = os.path.join(home_folder_path, cml_folder, current_time)
        os.mkdir(log_dir)
        return log_dir

    def search(self, block):
        """Start the knowledge search process.

        Args:
            block (pandas.DataFrame): Raw block.

        Returns:
            tuple:
                KnowledgeDatabase, pandas.DataFrame

        """
        if self.n_procs > 1:
            try:
                n_procs = self.n_procs
                self.pool = multiprocessing.Pool(n_procs, maxtasksperchild=1)
                return self.search_parallel(block)

            finally:
                if self.pool:
                    self.pool.close()
                    self.pool.join()
                    del self.pool

        else:
            return self.search_serial(block)

    def search_parallel(self, block):
        """Perform the knowledge search process with the help of many processes.

        Args:
            block (pandas.DataFrame): Raw data block.

        Returns:
            tuple:
                KnowledgeDatabase, pandas.DataFrame

        """
        halde = None
        for gen in self._generate_learnblock(block):
            if halde is None:
                halde = gen.halde

            if gen.lb is None:
                break

            candidates = defaultdict(list)

            level = gen.level
            lb = gen.lb

            log_queues_list, runner_list = self.get_parallel_runner(level)
            args = [(runner, level, lb) for runner in runner_list]

            reliability_dicts = self.pool.map(map_onto, args)

            self.log_parallel_version(log_queues_list)
            for rel_dict in reliability_dicts:
                if rel_dict is not None:
                    reliability, pragmatics = rel_dict.popitem()
                    if reliability == 0.0:
                        continue

                    candidates[reliability].extend(pragmatics)

            win_info, winner = self.reconstructor.select_winner(candidates)
            self.log(win_info)

            if winner:
                for dec_infs in self.deconstructor.deconstruct(
                        gen.level, winner, self.knowledge_database):
                    self.log(dec_infs)

        return deepcopy(self.knowledge_database), halde

    def get_parallel_runner(self, level):
        """Build n ParallelRunners.

        n = number of unsupervised algorithms * cluster specification

        Args:
            level (int): Level on which the ParallelRunner should
                perform the construction and reconstruction.

        Returns:
            tuple:
                Queue, ParallelRunner

        """
        runners = []
        log_queues = []
        manager = multiprocessing.Manager()
        identifier_queue = manager.Queue()

        for constructor in self.constructor.serial_constructor_per_combination():
            reconstructor = copy(self.reconstructor)
            reconstructor.identifier_queue = identifier_queue

            selector = self.selector

            log_queue = manager.Queue()
            log_queues.append(log_queue)

            runner = ParallelRunner(
                constructor,
                selector,
                reconstructor,
                log_queue,
            )
            runners.append(runner)

        n_ids = len(runners) * len(self.reconstructor.ml_models)
        for _ in range(n_ids):
            identifier = self.knowledge_database.get_next_identifier(level)
            identifier_queue.put(identifier)

        return log_queues, runners

    def log_parallel_version(self, log_queues):
        """Empty the log queues and protocol the information that was
        stored in logs.

        Args:
            log_queues (list): Log queues of the ParallelRunners.

        """
        for log_queue in log_queues:
            while not log_queue.empty():
                try:
                    info = log_queue.get(False)
                    self.log(info)
                except Empty:
                    continue

    def search_serial(self, block):
        """Perform the the knowledge search process.

        Args:
            block (pandas.DataFrame): Raw block.

        Returns:
            tuple:
                KnowledgeDataFrame, pandas.DataFrame

        """
        halde = None
        for gen in self._generate_learnblock(block):
            if halde is None:
                halde = gen.halde

            if gen.lb is None:
                break

            candidates = defaultdict(list)

            for con_info, labeled_lb in self.constructor.construct(gen.lb):
                self.log(con_info)

                if labeled_lb is None:
                    continue

                sel_info, reduced_lb = self.selector.select(labeled_lb)
                self.log(sel_info)

                if reduced_lb is None:
                    continue

                self.calculate_needed_ids(gen.level, self.reconstructor)
                rel, interims, rec_infs = self.reconstructor.reconstruct(
                    gen.level, reduced_lb, which_models=None, meta=None
                )
                self.log(rec_infs)

                if rel == 0.0:
                    continue

                candidates[rel].extend(interims)

            win_inf, winner = self.reconstructor.select_winner(candidates)
            self.log(win_inf)

            if winner:
                for dec_infs in self.deconstructor.deconstruct(
                        gen.level, winner, self.knowledge_database):
                    self.log(dec_infs)

        return deepcopy(self.knowledge_database), halde

    def log(self, log_info):
        """Log the information that happened during the knowledge search
        process.

        Args:
            log_info (LogMeMixin): Holds logging information.

        """
        try:
            for info in log_info:
                info.log_me(self.logger, self.stdout, self.json_container)

        except TypeError:
            log_info.log_me(self.logger, self.stdout, self.json_container)

    def _generate_learnblock(self, block):
        """Yield learnblocks for the knowledge search process.

        Args:
            block (pandas.DataFrame): Raw block.

        Yield:
            PandasBlock:
                Valid learnblock.

        """
        level = 1
        Generated = namedtuple("Generated", ("level", "lb", "halde"))

        proc_info, pandas_block = self.source.process(block)
        proc_info.level = level
        self.log(proc_info)

        idn_info, learnblock, halde = self.identifier.identify(pandas_block)
        idn_info.level = level
        self.log(idn_info)
        if learnblock is None:
            yield Generated(level, None, halde)

        self.source.append_to_knowledge(learnblock)
        yield Generated(level, learnblock, halde)

        while self.tsigma_beamer:
            level, learnblock = self.tsigma_beamer.pop()
            if level and learnblock:
                self.log(HighLevelLearnblockInfo(learnblock, level))
                yield Generated(level, learnblock, None)

    def calculate_needed_ids(self, level, reconstructor):
        """Push enough new identifier into identifier_queue of the given
        reconstructor.

        Args:
            level (int): Level of KnowledgeDatabase.
            reconstructor (Reconstructor): Where to push the identifiers.

        """
        n_ids = len(reconstructor.ml_models)
        for _ in range(n_ids):
            identifier = self.knowledge_database.get_next_identifier(level)
            reconstructor.identifier_queue.put(identifier)

    def __get_logger(self):
        """Return the logger object.

        Returns:
            logging.RootLogger

        """
        iteration_log_file = os.path.join(self.log_destination, "iteration.log")
        iteration_handler = FileHandler(iteration_log_file)
        iteration_handler.level = PROTOCOL_LEVEL
        iteration_logger = getLogger("iterationLogger")

        # Remove loggers from other sessions
        if iteration_logger.handlers:
            iteration_logger.handlers.clear()
        iteration_logger.addHandler(iteration_handler)

        if self.stdout:
            iteration_stdout_handler = StreamHandler()
            iteration_stdout_handler.level = PROTOCOL_LEVEL
            iteration_logger.addHandler(iteration_stdout_handler)

        return iteration_logger


class KnowledgeSearcherUsecase(Usecase):
    def process(self, request):
        """Process the request to create a KnowledgeSearcher.

        Args:
            request (KnowledgeSearchingRequest): Namedtuple with all essential
                ingredients.

        Raises:
            ModeError:
                Inconsistent Reconstructor and Constructor modes.

        Returns:
            KnowledgeSearcher

        """
        if not self.valid_modes(request):
            raise ModeError(
                "Inconsistent constructor and reconstructor modes."
                "Returns KnowledgeSearcher object by consistent modes."
                "Make sure the modes of constructor and reconstructor are the "
                "same."
            )

        return KnowledgeSearcher(**self.build_parts(request))

    def valid_modes(self, request):
        """Check if the given Constructor and Reconstructor as well as
        Deconstructor have the same mode.

        Args:
            request (KnowledgeSearchingRequest): Namedtuple with all essential
                ingredients.

        Returns:
            bool:
                True, if all mode are consistent.

        """
        return request.constructor.mode == request.reconstructor.mode

    def build_parts(self, request):
        """Build all essential components for the knowledge search process.


        Args:
            request (KnowledgeSearchingRequest): Namedtuple with all essential
                ingredients.

        Returns:
            dict:
                Map attribute name to the acctually attribute.

        """
        knowledge = self.create_database(request)
        identifier = LearnblockIdentifier(
            request.block_processing_settings,
            request.density_estimator,
            request.ckmeans
        )
        source = Source(knowledge, request.df_converter)
        return {
            "source": source,
            "identifier": identifier,
            "constructor": request.constructor,
            "selector": request.feature_selector,
            "reconstructor": request.reconstructor,
            "deconstructor": request.deconstructor,
            "knowledge_database": knowledge,
            "stdout": request.stdout,
            "n_procs": request.n_procs
        }

    def create_database(self, request):
        """Create a new KnowledgeDatabase if the given request does not
        contain any database.

        Args:
            request (KnowledgeSearchingRequest): Namedtuple with all essential
                ingredients.

        Returns:
            KnowledgeDatabase

        """
        if request.knowledge is not None:
            knowledge = request.knowledge

        else:
            knowledge = KnowledgeDatabase(
                request.general_settings.highest_level,
                request.build_block_from_rows
            )
            knowledge.observer.append(
                RelativeFinder(request.general_settings.highest_level)
            )

        return knowledge
