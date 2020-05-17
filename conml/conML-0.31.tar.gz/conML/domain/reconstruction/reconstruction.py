"""Defines the reconstruction process.

"""


from collections import namedtuple
from itertools import zip_longest
from multiprocessing import Manager

from conML.shared.logger import ReconstructionInfo
from conML.domain.reconstruction.selection import WinnerSelector


InterimPragmatic = namedtuple("InterimPragmatic", "model, predictions")


class Metadata:
    """Responsible for storing the meta data of a pragmatic machine
    learning model.

    Args:
        knowledge_domain (str): Name of the knowlede domain.
        knowledge_level (int): Level on which model is stored.
        identifier (int): Unique model identifier.
        learnblock_indices (list): Indices of used learnblock.
        learnblock_features (list): Name of features used in learnblock.
        learnblock_labels (list): List of labels used in the learnblock.
        t_min (int): The smallest timestamp in used in learnblock.
        t_max (int): The biggest timestamp in used in learnblock.
        subject (tuple): Contains abbreviations of supervised
            machine learning models.
        aim (tuple):
            Tuple of strings in format
            'knowledge_domain . knowledge_level . abbreviation of
            unsupervised machine learning model + found cluster' i.e. C.2.Kme02

    """
    def __init__(self, knowledge_domain, knowledge_level, identifier,
                 learnblock_indices, learnblock_features, learnblock_labels,
                 t_min, t_max, subject, aim):
        assert isinstance(subject, tuple)

        self.knowledge_domain = knowledge_domain
        self.knowledge_level = knowledge_level
        self.identifier = identifier
        self.learnblock_indices = learnblock_indices
        self.learnblock_features = learnblock_features
        self.learnblock_labels = learnblock_labels
        self.t_min = t_min
        self.t_max = t_max
        self.subject = subject
        self.aim = aim
        self.subjects = None

    def __str__(self):
        return "\n".join([
            "{:20}:{}".format("Knowledge Domain", self.knowledge_domain),
            "{:20}:{}".format("Knowledge Level", self.knowledge_level),
            "{:20}:{}".format("Identifier", self.identifier),
            "{:20}:{}".format("Learnblock Indices", self.learnblock_indices),
            "{:20}:{}".format("Learnblock Labels", self.learnblock_labels),
            "{:20}:{}".format("Learnblock Features", self.learnblock_features),
            "{:20}:{}".format("T Min", self.t_min),
            "{:20}:{}".format("T Max", self.t_max),
            "{:20}:{}".format("Subject", self.subject),
            "{:20}:{}".format("Aim", self.aim)
            ]
        )

    def __repr__(self):
        return ", ".format([
                "{}={}".format("knowledge_domain", self.knowledge_domain),
                "{}={}".format("knowledge_level", self.knowledge_level),
                "{}={}".format("identifier", self.identifier),
                "{}={}".format("learnblock_indices", self.learnblock_indices),
                "{}={}".format("learnblock_features", self.learnblock_features),
                "{}={}".format("learnblock_labels", self.learnblock_features),
                "{}={}".format("t_min", self.t_min),
                "{}={}".format("t_max", self.t_max),
                "{}={}".format("subject", self.subject),
                "{}={}".format("aim", self.aim),
            ]
        )

    def __hash__(self):
        return hash(
            ".".join([
                self.knowledge_domain,
                str(self.knowledge_level),
                str(self.identifier)
            ])
        )

    def __eq__(self, other):
        if isinstance(other, Metadata):
            return hash(self) == hash(other)

        else:
            raise NotImplemented


class PragmaticMachineLearningModel:
    """Responsible of holding information about the pragmatic machine
    learning model.

    Args:
        meta (MetaData):
            Holds meta data of pragmatic machine laerning model.
        model (MachineLearningModel): Supervised machine learning model.
        learnblock (PandasBlock):
            Learnblock used for training the supervised machine learning model.

    """
    def __init__(self, meta, model, learnblock):
        if learnblock.constructed_from_models():
            self.__learnblock = learnblock
        else:
            self.__learnblock = None

        if meta.learnblock_labels is not None:
            assert meta.learnblock_labels[0] != ""

        self.meta = meta
        self.model = model
        self.origin = learnblock.origin

    def __str__(self):
        return "\n".join([
                str(self.meta),
                "{:20}: {}".format("Origin", str(self.origin))
            ]
        )

    def __repr__(self):
        return ", ".format([
                repr(self.meta),
                "{}={}".format("Origin", str(self.origin)),
                "{}=[{}]".format("model", repr(self.model))
            ]
        )

    def __hash__(self):
        return hash(self.meta)

    def __eq__(self, other):
        if isinstance(other, PragmaticMachineLearningModel):
            return hash(self.meta) == hash(other.meta)

        if isinstance(other, str):
            return hash(self) == hash(other)

        raise NotImplementedError

    @property
    def subjects(self):
        return self.meta.subjects

    @property
    def domain(self):
        return self.meta.knowledge_domain

    @property
    def level(self):
        return self.meta.knowledge_level

    @property
    def identifier(self):
        return self.meta.identifier

    @property
    def uid(self):
        return "." .join([self.domain, str(self.level), str(self.identifier)])

    @identifier.setter
    def identifier(self, value):
        self.meta.identifier = value

    @property
    def min_timestamp(self):
        return self.meta.t_min

    @property
    def max_timestamp(self):
        return self.meta.t_max

    @property
    def learnblock_features(self):
        return self.meta.learnblock_features

    @property
    def learnblock_indices(self):
        return self.meta.learnblock_indices

    @property
    def learnblock_labels(self):
        return self.meta.learnblock_labels

    @property
    def subject(self):
        return self.meta.subject

    @property
    def aim(self):
        return self.meta.aim

    @property
    def accuracy(self):
        return self.model.accuracy

    @property
    def reliability(self):
        return self.model.reliability

    @reliability.setter
    def reliability(self, value):
        self.model.reliability = value

    def fusion(self, model, knowledge_level, new_identifier):
        """Combine the meta data with the meta data  of another model.

        Args:
            model (PragmaticMachineLearningModel): With whome the fusion will
                kbe done.
            knowledge_level (int): Level on which the combination is performed.
            new_identifier (int): The new identifier for the combined model.

        Returns:
            MetaData:
                Combined medatdata.

        """
        meta_data = Metadata(knowledge_domain=self.meta.knowledge_domain,
                             knowledge_level=knowledge_level,
                             identifier=new_identifier,
                             learnblock_indices=None,
                             learnblock_features=None,
                             learnblock_labels=None,
                             t_min=min(self.meta.t_min, model.min_timestamp),
                             t_max=max(self.meta.t_max, model.max_timestamp),
                             subject=tuple(set(self.subject+model.subject)),
                             aim=tuple(set(self.meta.aim+model.aim)))
        meta_data.subjects = tuple(set(self.subjects + model.subjects))
        return meta_data

    def trained_with(self, knowledge):
        """Rebuild the learnblock on which the model was trained.

        Args:
            knowledge (KnowledgeDatabase): Database that stored the learnblockk.

        Returns:
            PandasBlock:
                Learnblock used for training the PragmaticMachineLearningModel.

        """
        if self.__learnblock:
            return self.__learnblock

        learnblock = knowledge.get_block(self.learnblock_indices)
        preserved_features = self.learnblock_features + ["T", "Sigma", "Z"]
        for feature in learnblock.columns():
            if feature not in preserved_features:
                learnblock.drop_columns([feature])
        learnblock.set_column("Z", self.learnblock_labels)

        learnblock.subject = self.subject
        learnblock.origin = self.origin
        return learnblock

    def set_subjects(self, subjects):
        """Assign to meta data all subjects.

        Args:
            subjects (list): List of abbreviations of supervised machine
                learning models.

        """
        self.meta.subjects = tuple(subjects)


class Reconstructor:
    """Responsible for reconstructing learnblocks.

    Notes:
        Only conceptual mode is currently supported.

    Args:
        mode (str): Either 'conceptual' or 'procedural'
        ml_models (list):
            List of supervised machine learning models.
        settings (ReconstrucionSettings):
            Instantiated object controlls the behavior of the Constructor.
        krippendorff_alpha (Callable):
            Wrapper for calculating interreability.

    Attributes:
        identifier_queue (Queue):
            Holds identifier for new reconstructed models.

    """
    CONCEPTUAL_KNOWLEDGE_ABBREVIATION = "C"
    PROCEDURAL_KNOWLEDGE_ABBREVIATION = "P"

    def __init__(self, mode, ml_models, settings, krippendorff_alpha):
        self.mode = mode
        self.ml_models = ml_models
        self.settings = settings
        self.identifier_queue = Manager().Queue()
        self.krippendorff_alpha = krippendorff_alpha

    def __str__(self):
        return "\n" .join([
            "{:20}: {}".format("Mode", str(self.mode)),
            "{:20}: {}".format("ML Models", [
                str(m) for m in self.ml_models]),
            str(self.settings)
        ]
        )

    def __repr__(self):
        return ", ".join([
            "{}={}".format("mode", str(self.mode)),
            "{}".format(repr(self.settings)),
            "{}={}".format("ml_models", repr(self.ml_models))
            ]
        )

    def select_winner(self, reliability_dict):
        return WinnerSelector().determine_winner(
            reliability_dict,
            self.ml_models
        )

    def reconstruct(self, level, lb, which_models, meta, *args, **kwargs):
        """Main method for reconstructing the given learnblock.

        Args:
            level (int): Level on which the reconstruction is performed.
            lb (PandasBlock): Learnblock.
            meta (Metadata): MetaData to use for the pragmatic machine learning
                model.

        Returns:
            tuple:
                Calculated inter-reliability as float.
                List with InterimPragmatics.
                List with logging information.

        """
        interims, logs = self.build_interim_pragmatics(
            level, lb, which_models, meta, *args, **kwargs
        )

        if len(interims) < self.settings.min_build_models:
            return 0.0, [], logs

        reliability = self.calc_intersubject_reliability(interims)

        for interim, log in zip_longest(interims, logs):
            if interim is not None:
                interim.model.reliability = reliability

            if log is not None:
                log.reliability = reliability

        if reliability < self.settings.min_reliability:
            return 0.0, [], logs

        reduced_interims = [i.model for i in interims]

        return reliability, reduced_interims, logs

    def build_interim_pragmatics(self,
                                 level,
                                 learnblock,
                                 which_models=None,
                                 meta=None,
                                 *args,
                                 **kwargs):
        """Train all supervised machine learning algorithms on the learnblock.


        Args:
            level (int): Level on which the reconstrucion is performed.
            learnblock (PandasBlock): Learnblock.
            which_models :
            meta (Metadata): MetaData to use for the pragmatic machine learning
                model.

        Returns:
            tuple:
                List with PragmaticMachineLearningModels.
                List with logging information.

        """
        train, test = split(learnblock, self.settings.reliability_sample)
        train_x = train.as_numpy_array()
        train_y = [label for label in train.get_column("Z")]
        test_x = test.as_numpy_array()
        test_y = [label for label in test.get_column("Z")]

        logs, models, subjects = [], [], []

        for model in self.machine_learning_models(which_models):
            trained_model = model.train(train_x, train_y)
            trained_model.accuracy = model.score(test_x, test_y)

            if valid_reconstructed(trained_model, self.mode, self.settings):
                predictions = trained_model.predict(test_x)
                metadata = self.build_meta(level, learnblock, trained_model, meta)
                pragmatic = PragmaticMachineLearningModel(metadata,
                                                          trained_model,
                                                          learnblock)

                models.append(InterimPragmatic(pragmatic, predictions))
                logs.append(log_info(
                    ReconstructionInfo.State.RECONSTRUCTED,
                    trained_model,
                    pragmatic))

                subjects.append(pragmatic.model.subject)

            else:
                logs.append(log_info(ReconstructionInfo.State.DISCARDED,
                                     trained_model))

        for m in models:
            m.model.set_subjects(subjects)

        return models, logs

    def machine_learning_models(self, which_models):
        """Yield unsupervised machine learning models.

        Args:
            which_models (list): List of unsupervised machine learning model
                abbreviations.

        Yields:
              MachineLearningModel

        """
        if not which_models:
            for model in self.ml_models:
                yield model
        else:
            for model in self.ml_models:
                if model.subject in which_models:
                    yield model

    def calc_intersubject_reliability(self, interims):
        """Calculate the interreabililty between labels of unsupervised
        machine learning models.

        Args:
            interims (list): List with InterimPragmatics

        Returns:
            float:
                Inter-reliability value between labels.

        """
        predictions = [interim.predictions for interim in interims]
        if len(predictions) == 1:
            return 0.0

        reliability_alpha = self.krippendorff_alpha(predictions)
        return reliability_alpha

    def build_meta(self, level, learnblock, model, meta):
        """Build meta data for the reconstructed model.

        Args:
            level (int): Level on which the reconstrucion is performed.
            learnblock (PandasBlock): Learnblock.
            model (MachineLearningModel): Supervised machine learnign model.
            meta (Metadata): Use it a basis for the new meta data.

        Returns:
            MetaData

        """
        if not meta:
            zeta = self.build_aim(level, learnblock)
            identifier = self.identifier_queue.get()

            return Metadata(
                knowledge_domain=self.CONCEPTUAL_KNOWLEDGE_ABBREVIATION,
                knowledge_level=level,
                identifier=identifier,
                learnblock_indices=learnblock.indices(),
                learnblock_features=learnblock.columns(),
                learnblock_labels=learnblock.get_column("Z"),
                t_min=learnblock.min_timestamp(),
                t_max=learnblock.max_timestamp(),
                subject=(model.subject,),
                aim=(zeta, ))

        else:
            meta.learnblock_indices = learnblock.indices()
            meta.learnblock_features = learnblock.columns()
            meta.learnblock_labels = learnblock.get_column("Z")
            return meta

    def build_aim(self, level, learnblock):
        """Build the aim of the new reconstruced learnblock.

        Args:
            level (int): Knwoledge domain level.
            learnblock (PandasBlock): Used learnblock.

        Returns:
            str:
                Aim for PragmaticMachineLearningModel: C.2.Kme02

        """
        return ".".join([self.CONCEPTUAL_KNOWLEDGE_ABBREVIATION, str(level),
                         str(learnblock.subject)])

    def get_pml(self, meta, block, ml_model):
        """Build PragmaticMachineLearningModel without reconstrucing
        it but with just the given meta data.

        Args:
            meta (Metadata): Meta data.
            block (PandasBlock): Learnblock.
            ml_model (List): List of supervised machine learning models.

        Returns:
            PragmaticMachineLearningModels

        """
        meta.learnblock_indicies = block.indices()
        meta.learnblock_features = block.columns()
        meta.learnblock_labels = block.get_column("Z")
        return PragmaticMachineLearningModel(meta, ml_model, block)

    @property
    def min_test_accuracy(self):
        return self.settings.min_test_accuracy

    @min_test_accuracy.setter
    def min_test_accuracy(self, value):
        self.settings.min_test_accuracy = value

    @property
    def reliability_sample(self):
        return self.settings.reliability_sample

    @reliability_sample.setter
    def reliability_sample(self, value):
        self.settings.reliability_sample = value

    @property
    def min_reliability(self):
        return self.settings.min_reliability

    @min_reliability.setter
    def min_reliability(self, value):
        self.settings.min_reliability = value


def split(learnblock, reliability_sample):
    indices = learnblock.indices()
    eval_size = int(learnblock.n_rows() * reliability_sample)
    eval_idx, train_idx = indices[:eval_size], indices[eval_size:]
    return (
        learnblock.new_block_from(train_idx, index=True),
        learnblock.new_block_from(eval_idx, index=True)
    )


def valid_reconstructed(model, knowledge_domain, settings):
    """Test if the trained supersived model fullfills the accuracy criteria.

    Args:
        model (MachineLearningModel):
        knowledge_domain (str): Either 'conceptual' or 'procedural'.
        settings (ReconstructionSettings): Contains the minimum accuracy.

    Returns:
        bool:
            True if accuracy criteria is fullfilled else False.

    """
    if knowledge_domain == "conceptual":
        return model.accuracy >= settings.min_test_accuracy


def log_info(state, trained_model, pragmatic=None):
    """Build logging object for the reconstruction process.

    Args:
        state (Enum): Indicates the state of the reconstruction.
            If it was successfull or not.
        trained_model (MachineLearningModel): Supervised model.

    Returns:
        ReconstructionInfo
            Holds information about the finished reconstruction process.

    """
    uid = pragmatic.uid if pragmatic else ""
    aim = pragmatic.aim if pragmatic else ""

    return ReconstructionInfo(
        state=state,
        uid=uid,
        aim=aim,
        accuracy=trained_model.accuracy,
        subject=trained_model.subject
    )
