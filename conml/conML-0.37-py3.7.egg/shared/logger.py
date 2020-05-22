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


"""Define the logging mechanism.


"""


import json
from os.path import join
from enum import Enum


class LogMeMixin:
    def log_me(self, logger, stdout, json_container):
        """Log the information gathered during the knowledge search process.

        Args:
            logger (logging.Logger):
            stdout (bool): Indicator if it should be logged to console.
            json_container (JsonContainer): Container for the logging
                information in JSON-Format.

        """
        json_container.log(self)

        if stdout:
            logger.protocol(self.banner())
            logger.protocol(str(self))


class BlockProcessInfo(LogMeMixin):
    """Holds logging information of the block pulling process.

    Args:
        n_rows (int): Number of rows the block contains.
        n_columns (int): Number of coloumns the block contains.

    Attributes:
         level (int): Level on which the block is pulled.

    """

    def __init__(self, n_rows, n_columns):
        self.level = 1
        self.n_rows = n_rows
        self.n_columns = n_columns

    def __str__(self):
        return "\n".join([
            "{: <20}{}".format("Rows", str(self.n_rows)),
            "{: <20}{}".format("Columns", str(self.n_columns))
        ])

    def banner(self):
        """Return banner that indicates the beginning of the learnblock
        identification.

        Returns:
            str

        """
        return "{:=^100}".format("BLOCKPROCESSING")


class LearnblockIdentificationInfo(LogMeMixin):
    """Holds logging information of the learnblock identification.

    Args:
        state (LearnblockIdentificationInfo.State):
        n_rows (int): Number of rows the learnblock has.
        n_columns (int): Number of columns the learnblock has.
        relationship (tuple): Which relationship was found to build
            the learnblock.

    Attributes:
         state (LearnblockIdentificationInfo.State): Indicator if the
            learnblock identification was successfull or not.

    """

    class State(Enum):
        IDENTIFIED = 1
        DISCARDED = 2

    def __init__(self, state, n_rows=None, n_columns=None, relationship=None):
        self.state = state
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.relationship = relationship

    def __str__(self):
        return "\n".join([
            "{: <20}{}".format("State", str(self.state)),
            "{: <20}{}".format("Relationship", str(self.relationship))
        ])

    def banner(self):
        """Return banner that indicates the beginning of the learnblock
        identification.

        Returns:
            str

        """
        return "{:=^100}".format("LEARNBLOCK")


class HighLevelLearnblockInfo(LogMeMixin):
    """Holds logging information about the learnblock pushed on the higher
    level.

    Args:
        lb (PandasBlock): Learnblock.
        level (int): Level on which the learnblock is pushed.

    Attributes:
         n_rows (int): Number of rows the learnbock has.
         n_columns (int): Number of columns the learnblock has.
         origin (tuple): Indicates who was the learnblock builder.

    """

    def __init__(self, lb, level):
        self.level = level
        self.n_rows = lb.n_rows()
        self.n_columns = lb.n_columns()
        self.origin = lb.origin

    def __str__(self):
        return "\n".join([
            "{: <20}{}".format("Level", str(self.level)),
            "{: <20}{}".format("Rows", str(self.n_rows)),
            "{: <20}{}".format("Columns", str(self.n_columns))
        ])

    def banner(self):
        """Return banner that indicates the beginning of the learnblock.

        Returns:
            str

        """
        return "{:=^100}".format("LEARNBLOCK")


class ConstructionInfo(LogMeMixin):
    """Holds logging information about the construction process.

    Args:
        state (ConstructionInfo.State): Indicates if the construction
            process was successfull or not.
        learnblock (PandasBlock): Constructed learnblock.
        subject (tuple): Name of the unsupervised machine learning model.
        n_cluster (int): Number of cluster the constructed learnblock has.

    Attributes:
        rows (int): Number of rows the learnblock has.
        columns (int): Number columns the learnblock has.
        min_t (int): Minimum timestamp the T features has.
        max_t (int): Maximum timestamp the T features has.
        origin (tuple): Indicates who was the learnblock builder.
        relationship (tuple): Indicates which relationship if any was
            used to buld the learnblock.

    """

    class State(Enum):
        DISCARDED = 1
        CONSTRUCTED = 2
        PASSED = 3

    def __init__(self, state, learnblock=None, subject="", n_cluster=""):
        self.state = state
        self.subject = subject
        self.n_cluster = n_cluster

        # learnblock information
        if learnblock:
            self.rows = str(learnblock.n_rows())
            self.columns = str(learnblock.n_columns())
            self.min_t = str(learnblock.min_timestamp())
            self.max_t = str(learnblock.max_timestamp())
            self.origin = str(learnblock.origin)
            self.relationship = str(learnblock.relationship)
            self.lb_subject = learnblock.subject if learnblock.subject else ""

    def __str__(self):
        if self.state == self.State.PASSED:
            return "\n".join([
                    "{: <20}{}".format("State:", "PASSED"),
                    self.learnblock_info()
                ]
            )

        elif self.state == self.State.DISCARDED:
            return "\n".join([
                "{: <20}{}".format("State:", "DISCARDED"),
                "{: <20}{}".format("Subject:", self.subject),
                "{: <20}{}".format("Cluster:", self.n_cluster)
                ]
            )

        elif self.state == self.State.CONSTRUCTED:
            return "\n".join([
                    "{: <20}{}".format("State:", "CONSTRUCTED"),
                    self.learnblock_info()
                ]
            )

    def learnblock_info(self):
        return "\n".join([
            "{: <20}{}".format("Rows", self.rows),
            "{: <20}{}".format("Columns", self.columns),
            "{: <20}{}".format("Cluster", self.n_cluster),
            "{: <20}{}".format("MinT", self.min_t),
            "{: <20}{}".format("MaxT", self.max_t),
            "{: <20}{}".format("Origin", self.origin),
            "{: <20}{}".format("Relationship", self.relationship),
            "{: <20}{}".format("Subject", self.lb_subject)
            ]
        )

    def banner(self):
        """Return banner that indicates the beginning of the construction.

        Returns:
            str

        """
        return "{:=^100}".format("CONSTRUCTION")


class SelectionInfo(LogMeMixin):
    """Hold logging information of the feature selection process.

    Args:
        state (SelectionInfo.State): Indicates the state of the feature
            selection process.
        learnblock (PandasBlock): Learnblock.

    Attributes:
         n_rows (int): Number of learnblock rows.
         n_columns (int): Number of learnblock columns.

    """
    class State(Enum):
        REDUCIBLE = 1
        NON_REDUCIBLE = 2

    def __init__(self, state, learnblock):
        self.state = state
        self.n_rows = learnblock.n_rows()
        self.n_columns = learnblock.n_columns(effective=True)

    def __str__(self):
        return "\n".join([
            "{: <20}{}".format("State", str(self.state)),
            "{: <20}{}".format("Rows", str(self.n_rows)),
            "{: <20}{}".format("Columns", str(self.n_columns))
            ]
        )

    def banner(self):
        """Return banner that indicates the beginning of the feature selection
        process.

        Returns:
            str

        """
        return "{:=^100}".format("SELECTION")


class ReconstructionInfo(LogMeMixin):
    """Holds infomration of the reconstruction process.

    Args:
        state (ReconstructionInfo.State): Indicates if the reconstruction
            process was successfull.
        uid (str): Unique identifier of PragmaticMachineLearningModel.
        aim (str): Aim in the context of conML.
        accuracy (float): Accuracy of the supersived machine learnign model.
        subject (tuple): Abbreviations of the supervised machine learning
            model.s
        reliability (float): Inter-reliability between supervised machine
            learning models.

    """

    class State(Enum):
        DISCARDED = 1
        RECONSTRUCTED = 2

    def __init__(self, state=None, uid=None, aim=None, accuracy=None,
                 subject=None, reliability=0.0):
        self.state = state
        self.uid = uid
        self.aim = aim
        self.accuracy = accuracy
        self.subject = subject
        self.reliability = reliability

    def __str__(self):
        if self.state == ReconstructionInfo.State.RECONSTRUCTED:
            return "\n".join([
                    "{: <20}{}".format("State", str(self.state)),
                    "{: <20}{}".format("Pragmatic:", str(self.uid)),
                    "{: <20}{}".format("Subject:", str(self.subject)),
                    "{: <20}{}".format("Accuracy:", str(self.accuracy)),
                    "{: <20}{}".format("Reliability:", str(self.reliability)),
                    "\n"
                ]
            )

        elif self.state == ReconstructionInfo.State.DISCARDED:
            return "\n".join([
                "{: <20}{}".format("State", str(self.state)),
                "{: <20}{}".format("Subject:", str(self.subject)),
                "{: <20}{}".format("Accuracy:", str(self.accuracy)),
                "\n"
                ]
            )

    def banner(self):
        """Return banner that indicates the beginning reconstruction process.

        Returns:
            str

        """
        return "{:=^100}".format("RECONSTRUCTION")


class WinnerSelectionInfo(LogMeMixin):
    """Holds the information about the winner selection process.

    Args:
        state (WinnerSelectionInfo.State): Indicates the status of the
            winner selection process.
        uid (str): Unique identifier of the PragmaticMachineLearningModel.
        subject (tuple): Abbreviations of supervised machine learning
            models.
        accuracy (float): Accuracy of supervised machine learnign model.
        reliability (float): Inter-reliability between supervised machine
            leanring models.

    """

    class State(Enum):
        SELECTED = 1
        FAILED = 2

    def __init__(self, state, uid=None, subject=None, accuracy=None,
                 reliability=None):
        self.state = state
        self.uid = uid
        self.subject = subject
        self.accuracy = accuracy
        self.reliability = reliability

    def __str__(self):
        state_info = "{: <20}{}".format("State", str(self.state))
        if self.state == self.State.SELECTED:
            winner_info = "\n".join([
                "{: <20}{}".format("Reconstructed:", str(self.uid)),
                "{: <20}{: <15}{}".format("", "Subject:", str(self.subject)),
                "{: <20}{: <15}{}".format("", "Accuracy:", str(self.accuracy)),
                "{: <20}{: <15}{}".format("", "Reliability:",
                                          str(self.reliability))
                ]
            )
        else:
            winner_info = ""

        return state_info+"\n"+winner_info

    def banner(self):
        """Return the banner that indicates the beginning of the winner
        selection process.

        Returns:
            str

        """
        return "{:=^100}".format("WINNER SELECTION")


class DeconstructionInfo(LogMeMixin):
    """Holds the informatino about the deconstruction process.

    Args:
        state (DeconstructionInfo.State): Indicates if the deconstruction
            process was successful or not.
        relationship (tuple): Type of deconstruction.
        relative (PragmaticMachineLearningModel): Relative of the
            deconstructed.
        pragmatic (PragmaticMachineLearningModel): The deconstructed..
        reconstructed_info (list): Contains reconstructed
            PragmaticMachineLearningModels.
        deleted (list): Contains deleted PragmaticMachineLearningModel.
        inserted (list): Contains inserted into database
            PragmaticMachineLearningModels.
        new_learnblock (PandasBlock): Learnblock pushed on the next
            level after successfully TSigma deconstruction.

    """
    class State(Enum):
        DECONSTRUCTED = 1
        FAILED = 2

    def __init__(self, state=None, relationship=None, relative=None,
                 pragmatic=None, reconstructed_info=None, deleted=None,
                 inserted=None, new_learnblock=None):
        self.state = state
        self.relationship = relationship
        self.relative = relative
        self.pragmatic = pragmatic
        self.reconstructed_info = reconstructed_info if reconstructed_info else []
        self.deleted = deleted if deleted else []
        self.inserted = inserted if inserted else []
        self.new_learnblock = new_learnblock

    def __str__(self):
        msg = ""
        if self.relationship:
            msg = "\n".join([
                    msg,
                    "{: <20}{}".format("State:", str(self.state)),
                    "{:+^100}".format(str(self.relationship)),
                    "{: <20}{}".format("Pragmatic:", str(self.pragmatic.uid)),
                    "{: <20}{}".format("Relative:", str(self.relative.uid)),
                    ]
                )

        if self.relationship == ("Sigma", "T"):
            return "\n".join([
                msg,
                "{: <20}[{:^5}{:^5}]".format(
                    "Dimension: ", str(self.new_learnblock.n_rows()),
                                   str(self.new_learnblock.n_columns())),
                "{: <20}{}".format("Min T: ",
                                   self.new_learnblock.min_timestamp()),
                "{: <20}{}".format("Max T: ",
                                   self.new_learnblock.max_timestamp()),
                "{: <20}{}".format("Origin: ",
                                   str(self.new_learnblock.origin)),
                ]
            )

        return "\n".join([
                msg,
                self.reconstructed_info_str(),
                "{: <20}{}".format(
                    "Inserted:", [", ".join([str(i.uid) for i in self.inserted
                                             if i is not None])]),
                "{: <20}{}".format(
                    "Deleted:", [", ".join([str(i.uid) for i in self.deleted
                                            if i is not None])])
            ]
        )

    def reconstructed_info_str(self):
        """Convert the PragmaticMachineLearningModels that were reconstructed
        during a deconstruction process into a string representation.

        Returns:
            str

        """
        msg = ""
        for m in self.reconstructed_info:
            msg = "\n".join([
                    msg,
                    "{: <20}{}".format("Reconstructed:", str(m.uid)),
                    "{: <20}{: <15} {}".format("", "Subject:", str(m.subject)),
                    "{: <20}{: <15} {}".format("", "Accuracy:", str(m.accuracy)),
                    "{: <20}{: <15} {}".format("", "Reliability:", str(m.reliability))
                ]
            )
        return msg

    def banner(self):
        """Return the banner that indicates the beginning of deconstruction
        process.

        Returns:
            str

        """
        return "{:=^100}".format("DECONSTRUCTION")


class JsonContainer:
    """Responsible for holding logging information about the knowledge
    search process in a JSON-FORMAT.

    Attributes:
        journal (dict): Container for the logging information.
        current_n_block (int): Currently processed block number.
        current_level (int): Level on which the currently learnblock
            is processed.
        current_lb (int): Currently processed learnblock.
        current_construction_subject (tuple): Currently used
            unsupervised machine learning model.
        dispatch_table (dict): Redirect the log object to the method
            responsible for storing his information into the journal.

    """
    def __init__(self):
        self.journal = {}
        self.current_n_block = 0
        self.current_level = 1
        self.current_lb = 0
        self.current_construction_subject = None

        self.dispatch_table = {
            BlockProcessInfo: self.log_process_block,
            LearnblockIdentificationInfo: self.log_lb_identification,
            HighLevelLearnblockInfo: self.log_higher_level_blocks,
            ConstructionInfo: self.log_construction,
            SelectionInfo: self.log_feature_selection,
            ReconstructionInfo: self.log_reconstruction,
            WinnerSelectionInfo: self.log_winner,
            DeconstructionInfo: self.log_deconstruction

        }

    def write_down(self, log_destination):
        """Write down the journal into the given destination.

        Args:
            log_destination (str): Logging destination.

        """
        file = join(log_destination, "log.json")
        with open(file, "w") as fp:
            json.dump(self.journal, fp)

    def log(self, info):
        """Call the responsible method for logging the given log object.

        Args:
            info: Log object.

        """
        self.dispatch_table[type(info)](info)

    def log_process_block(self, info):
        """Store the block processing logs into journal.

        Args:
            info (BlockProcessInfo): Holds block processing information.

        """
        self.current_n_block += 1
        self.journal[self.current_n_block] = {}
        self.journal[self.current_n_block]["BLOCK"] = {
                "rows": str(info.n_rows),
                "columns": str(info.n_columns),
                "LEVEL": {}
        }

    def log_lb_identification(self, info):
        """Store the learnblock identification logs into journal.

        Args:
            info (LearnblockIdentificationInfo): Holds learnblock identification
                information.

        """
        self.current_level = info.level
        level = self.journal[self.current_n_block]["BLOCK"]["LEVEL"]
        current_level = level[self.current_level] = {}

        current_level["LEARNBLOCKS"] = []
        current_level["LEARNBLOCKS"].append(
            {
                "rows": str(info.n_rows),
                "columns": str(info.n_columns),
                "relationship": str(info.relationship),
                "CONSTRUCTION": {},
                "WINNER": {},
                "DECONSTRUCTION": {
                    "COMPLETE": [],
                    "T SIGMA": [],
                    "Z SIGMA": []
                }
            }
        )
        self.current_lb = len(current_level["LEARNBLOCKS"]) - 1

    def log_higher_level_blocks(self, info):
        """Store learnblock logs that is considered for higher levels into
        journal.

        Args:
            info (HighLevelLearnblockInfo): Holds learnblock identification
                information.

        """
        self.current_level = info.level
        level = self.journal[self.current_n_block]["BLOCK"]["LEVEL"]

        if self.current_level not in level.keys():
            level[self.current_level] = {}

        current_level = level[self.current_level]
        if "LEARNBLOCKS" not in current_level.keys():
            current_level["LEARNBLOCKS"] = []

        current_level["LEARNBLOCKS"].append(
            {
                "rows": str(info.n_rows),
                "columns": str(info.n_columns),
                "origin": str(info.origin),
                "CONSTRUCTION": {},
                "WINNER": {},
                "DECONSTRUCTION": {
                    "COMPLETE": [],
                    "T SIGMA": [],
                    "Z SIGMA": []
                }
            }
        )
        self.current_lb = len(current_level["LEARNBLOCKS"]) - 1

    def log_construction(self, info):
        """Store construction log into journal.

        Args:
            info (ConstructionInfo): Construction logs.

        """
        self.current_construction_subject = str(info.subject)+str(info.n_cluster)
        key = (self.journal[self.current_n_block]
                           ["BLOCK"]
                           ["LEVEL"]
                           [self.current_level]
                           ["LEARNBLOCKS"]
                           [self.current_lb]
                           ["CONSTRUCTION"])
        key[self.current_construction_subject] = {"status": str(info.state)}

    def log_feature_selection(self, info):
        """Store features selection log into journal.

        Args:
            info (SelectionInfo): Feature selection logs.

        """
        key = (self.journal[self.current_n_block]
                           ["BLOCK"]
                           ["LEVEL"]
                           [self.current_level]
                           ["LEARNBLOCKS"]
                           [self.current_lb]
                           ["CONSTRUCTION"]
                           [self.current_construction_subject])

        key["SELECTION"] = {
            "rows": str(info.n_rows),
            "columns": str(info.n_columns)
        }

    def log_reconstruction(self, info):
        """Store reconstruction log into journal.

        Args:
            info (ReconstructionInfo): Reconstruction logs.

        """
        key = (self.journal[self.current_n_block]
                           ["BLOCK"]
                           ["LEVEL"]
                           [self.current_level]
                           ["LEARNBLOCKS"]
                           [self.current_lb]
                           ["CONSTRUCTION"]
                           [self.current_construction_subject])

        if "RECONSTRUCTION" not in key.keys():
            key["RECONSTRUCTION"] = []

        else:
            if info.state == ReconstructionInfo.State.RECONSTRUCTED:
                key["RECONSTRUCTION"].append(
                    {
                        "state": str(info.state),
                        "uid": str(info.uid),
                        "subject": str(info.subject),
                        "aim": str(info.aim),
                        "accuracy": str(info.accuracy),
                        "reliability": str(info.reliability)
                    }
                )

            else:
                key["RECONSTRUCTION"].append(
                    {
                        "state": str(info.state),
                        "subject": str(info.subject),
                        "accuracy": str(info.accuracy),
                        "reliability": str(info.reliability)
                    }
                )

    def log_winner(self, info):
        """Store winner selection log into journal.

        Args:
            info (WinnerSelectionInfo): Winner selection log.

        """
        key = (self.journal[self.current_n_block]
                           ["BLOCK"]
                           ["LEVEL"]
                           [self.current_level]
                           ["LEARNBLOCKS"]
                           [self.current_lb])

        if info.state == WinnerSelectionInfo.State.SELECTED:
            key["WINNER"] = {
                "state": str(info.state),
                "uid": str(info.uid),
                "subject": str(info.subject),
                "accuracy": str(info.accuracy),
                "reliability": str(info.reliability),
            }

        else:
            key["WINNER"] = {
                "state": str(info.state),
            }

    def log_deconstruction(self, info):
        """Store deconstruction log into journal.

        Args:
            info (DeconstructionInfo): Deconstruction log.

        """
        key = (self.journal[self.current_n_block]
                           ["BLOCK"]
                           ["LEVEL"]
                           [self.current_level]
                           ["LEARNBLOCKS"]
                           [self.current_lb]
                           ["DECONSTRUCTION"])

        if info.relationship == ("complete",):
            self.log_complete_deconstruction(info)

        elif info.relationship == ("Sigma", "T"):
            self.log_t_sigma_deconstruction(info)

        elif info.relationship == ("Sigma", "Z"):
            self.log_z_sigma_deconstruction(info)

        else:
            key["failed"] = {
                "inserted": [str(i.uid) for i in info.inserted],
                "deleted": [str(i.uid) for i in info.deleted]
            }

    def log_complete_deconstruction(self, info):
        """Store complete deconstruction log into journal.

        Args:
            info (DeconstructionInfo): Deconstruction log.

        """
        complete = (self.journal[self.current_n_block]
                                ["BLOCK"]
                                ["LEVEL"]
                                [self.current_level]
                                ["LEARNBLOCKS"]
                                [self.current_lb]
                                ["DECONSTRUCTION"]
                                ["COMPLETE"])

        complete.append({
            "state": str(info.state),
            "relative": str(info.relative.uid),
            "inserted": [str(i.uid) for i in info.inserted],
            "deleted": [str(i.uid) for i in info.deleted],
            "RECONSTRUCTED": []
        })

        pos = len(complete) - 1
        for recon_info in info.reconstructed_info:
            complete[pos]["RECONSTRUCTED"].append(
                {
                    "uid": str(recon_info.uid),
                    "subject": str(recon_info.subject),
                    "accuracy": str(recon_info.accuracy),
                    "reliability": str(recon_info.reliability)
                }
            )

    def log_t_sigma_deconstruction(self, info):
        """Store T Sigma deconstruction log into journal.

        Args:
            info (DeconstructionInfo): Deconstruction log.

        """
        t_sigma = (self.journal[self.current_n_block]
                              ["BLOCK"]
                              ["LEVEL"]
                              [self.current_level]
                              ["LEARNBLOCKS"]
                              [self.current_lb]
                              ["DECONSTRUCTION"]
                              ["T SIGMA"])

        t_sigma.append({
            "state": str(info.state),
            "relative": str(info.relative.uid),
            "LEARNBLOCK": {
                "rows": str(info.new_learnblock.n_rows()),
                "columns": str(info.new_learnblock.n_columns()),
                "min T": str(info.new_learnblock.min_timestamp()),
                "max T": str(info.new_learnblock.max_timestamp()),
                "origin": str(info.new_learnblock.origin)
            }
        })

    def log_z_sigma_deconstruction(self, info):
        """Store Z Sigma deconstruction log into journal.

        Args:
            info (DeconstructionInfo): Deconstruction log.

        """
        z_sigma = (self.journal[self.current_n_block]
                               ["BLOCK"]
                               ["LEVEL"]
                               [self.current_level]
                               ["LEARNBLOCKS"]
                               [self.current_lb]
                               ["DECONSTRUCTION"]
                               ["Z SIGMA"])

        z_sigma.append({
            "state": str(info.state),
            "relative": str(info.relative.uid),
            "inserted": [str(m.uid) for m in info.inserted if m is not None],
            "deleted": [str(m.uid) for m in info.deleted if m is not None]
        })
