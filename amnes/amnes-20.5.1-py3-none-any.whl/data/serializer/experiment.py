"""This module contains the Serializer for the Experiment module.

Classes:
    ExperimentTemplateSerializer: Concrete Serializer for the ExperimentTemplate class.
    ConcreteExperimentSerializer: Concrete Serializer for the ConcreteExperiment class.
"""
import json
from typing import ItemsView, List, Optional, Sequence, Tuple, Type, Union

from ...core.amnes_object import AmnesObject
from ...core.experiment import (
    ConcreteExperiment,
    ExperimentAbstract,
    ExperimentState,
    ExperimentTemplate,
)
from ...core.experiment_node import ConcreteExperimentNode, ExperimentNodeTemplate
from ...core.experiment_stage import ExperimentStage
from ..models import (
    AmnesObjectModel,
    ConcreteExperimentModel,
    ExperimentSequenceModel,
    ExperimentTemplateModel,
)
from .amnes_object import AmnesObjectSerializer
from .base import Serializer
from .experiment_node import (
    ConcreteExperimentNodeSerializer,
    ExperimentNodeTemplateSerializer,
)
from .utils import (
    model_instance_exists_by_id,
    pull_out_amnes_object,
    pull_out_amnes_object_list_stored,
    pull_out_amnes_object_stored,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)

Experiment = Union[ExperimentTemplate, ConcreteExperiment]
ExperimentModel = Union[ExperimentTemplateModel, ConcreteExperimentModel]
ExperimentNodeSerializer = Union[
    ExperimentNodeTemplateSerializer, ConcreteExperimentNodeSerializer
]
ExperimentNode = Union[ExperimentNodeTemplate, ConcreteExperimentNode]
ExperimentIngredients = Tuple[
    AmnesObject, List[ExperimentStage], List[ExperimentNode], int, str
]


def _experiment_insert(
    instance: Experiment,
    experiment_model: Type[ExperimentModel],
    parent: Optional[ExperimentSequenceModel] = None,
) -> int:
    """Inserts an Experiment into the database.

    An Experiment instance is a Plain-Python-Object from the core module.
    This method will also create and insert its (Stages) and related AmnesObject.
    Moreover an optional parent can be passed, such that an ExperimentSequenceModel
    receives a backreference `experiments`. This applies only to
    ConcreteExperiments/ the ConcreteExperimentSerializer.

    Args:
        instance (Experiment): Non-Empty Experiment instance.
        experiment_model (Type[ExperimentModel]): Model used for
                                                  create-method.
        parent (Optional[ExperimentSequenceModel]): Parent model for reference.

    Returns:
        object_id (int): Index of entry in database.
    """
    amnes_object_model_id = pull_out_amnes_object_stored(instance)
    (repetitions, states,) = __pull_out_repetitions_states(instance)
    if parent:
        experiment_model_instance = experiment_model.create(
            states=states,
            repetitions=repetitions,
            amnes_object=amnes_object_model_id,
            experiment_sequence=parent,
        )
    else:
        experiment_model_instance = experiment_model.create(
            states=states, repetitions=repetitions, amnes_object=amnes_object_model_id,
        )
    __add_stages_to_experiment_model(experiment_model_instance, instance.stages)
    experiment_node_serializer = __get_serializer_by_experiment_model(
        experiment_model_instance
    )
    experiment_node_serializer.insert_bulk(
        instance.nodes, experiment_model_instance.get_id()
    )
    return experiment_model_instance.get_id()


def _experiments_insert_bulk(
    instances: Sequence[Experiment],
    experiment_model: Type[ExperimentModel],
    parent: Optional[ExperimentSequenceModel] = None,
) -> List[int]:
    """Inserts multiple Experiments into the database.

    Args:
        instances (Sequence[Experiment]): List of Non-Empty Experiment
                                          instances.
        experiment_model (Type[ExperimentModel]): Model used for
                                                           create-method.
        parent (Optional[ExperimentSequenceModel]): Optional parental reference.

    Returns:
        instances_ids (List[int]): Returns a list of id in the order they were
                                   inserted.
    """
    instances_ids: List[int] = []
    for instance in instances:
        instances_ids.append(_experiment_insert(instance, experiment_model, parent))
    return instances_ids


def _experiment_delete_by_id(
    object_id: int, experiment_model: Type[ExperimentModel],
) -> None:
    """Deletes an Experiment by id from the database.

    Args:
        object_id (int): Index of entry in database.
        experiment_model (Type[ExperimentModel]): Model used for
                                                  delete_instance-method.
    """
    experiment_model_instance = experiment_model.get_by_id(object_id)
    __delete_stages(experiment_model_instance)
    __delete_nodes(experiment_model_instance)
    AmnesObjectSerializer.delete_by_id(experiment_model_instance.amnes_object.id)
    experiment_model_instance.delete_instance()


def _experiment_update_by_id(
    instance: Experiment, object_id: int, experiment_model: Type[ExperimentModel],
) -> None:
    """Updates a Experiment entry in the database.

    Args:
        instance (Experiment): Plain-Python-Object of ExperimentTemplate/
                               ConcreteExperiment, will be updated in the database.
        object_id (int): Unique identification of data-entry.
        experiment_model (Type[ExperimentModel]): Model used for get_by_id-method.
    """
    experiment_model_instance = experiment_model.get_by_id(object_id)
    __update_amnes_object(experiment_model_instance, instance)
    __update_stages(experiment_model_instance, instance)
    __update_nodes(experiment_model_instance, instance)
    (repetitions, states,) = __pull_out_repetitions_states(instance)
    query_update = experiment_model.update(
        {"repetitions": repetitions, "states": states}
    ).where(experiment_model.id == object_id)
    query_update.execute()


def _experiment_ingredients_get_by_id(
    object_id: int, experiment_model: Type[ExperimentModel]
) -> ExperimentIngredients:
    """Returns necessary objects to create a Plain-Python-Object Experiment.

    This method returns, the related AmnesObject, ExperimentStages, ExperimentNodes,
    repetitions and ExperimentStates to create either an ExperimentTemplate or a
    ConcreteExperiment.

    Args:
        object_id (int): Unique identifier, referencing to data-entry
                      inside the database.
        experiment_model (Type[ExperimentModel]): Model used for
                                                  get_by_id-method.

    Returns:
        ExperimentIngredients: Returns the related AmnesObject,
                               ExperimentStages, ExperimentNodes,
                               repetitions and ExperimentStates
    """
    experiment_model_instance = experiment_model.get_by_id(object_id)

    amnes_object = AmnesObjectSerializer.get_by_id(
        experiment_model_instance.amnes_object.id
    )
    stages = __experiment_get_stages(experiment_model_instance)
    nodes = __experiment_get_nodes(experiment_model_instance)
    repetitions = experiment_model_instance.repetitions
    states = experiment_model_instance.states
    return amnes_object, stages, nodes, repetitions, states


def __experiment_get_nodes(
    experiment_model_instance: ExperimentModel,
) -> List[ExperimentNode]:
    experiment_node_serializer = __get_serializer_by_experiment_model(
        experiment_model_instance
    )
    nodes: List[ExperimentNode] = [
        experiment_node_serializer.get_by_id(node.id)
        for node in experiment_model_instance.nodes
    ]
    return nodes


def __experiment_get_stages(
    experiment_model_instance: ExperimentModel,
) -> List[ExperimentStage]:
    stages: List[ExperimentStage] = []
    for stage in experiment_model_instance.stages:
        amnes_object = AmnesObjectSerializer.get_by_id(stage.id)
        stages.append(
            ExperimentStage(
                amnes_object.slug,
                amnes_object.name,
                amnes_object.description,
                amnes_object.labels,
            )
        )
    return stages


def __update_amnes_object(
    experiment_model_instance: ExperimentModel, instance: Experiment
) -> None:
    amnes_object_updated = pull_out_amnes_object(instance)
    AmnesObjectSerializer.update_by_id(
        amnes_object_updated, experiment_model_instance.amnes_object.id
    )


def __update_nodes(
    experiment_model_instance: ExperimentModel, instance: Experiment
) -> None:
    __delete_nodes(experiment_model_instance)
    experiment_node_serializer = __get_serializer_by_experiment_model(
        experiment_model_instance
    )
    experiment_node_serializer.insert_bulk(instance.nodes, experiment_model_instance)


def __update_stages(
    experiment_model_instance: ExperimentModel, instance: Experiment
) -> None:
    __delete_stages(experiment_model_instance)
    __add_stages_to_experiment_model(experiment_model_instance, instance.stages)


def __delete_stages(experiment_model_instance: ExperimentModel) -> None:
    for stage in experiment_model_instance.stages:
        AmnesObjectSerializer.delete_by_id(stage.id)
    experiment_model_instance.stages.clear()


def __delete_nodes(experiment_model_instance: ExperimentModel) -> None:
    experiment_node_serializer = __get_serializer_by_experiment_model(
        experiment_model_instance
    )
    for node in experiment_model_instance.nodes:
        experiment_node_serializer.delete_by_id(node.id)


def __get_serializer_by_experiment_model(
    experiment_model_instance: ExperimentModel,
) -> Type[ExperimentNodeSerializer]:
    experiment_node_serializer: Type[ExperimentNodeSerializer]
    if isinstance(experiment_model_instance, ExperimentTemplateModel):
        experiment_node_serializer = ExperimentNodeTemplateSerializer
    else:
        experiment_node_serializer = ConcreteExperimentNodeSerializer
    return experiment_node_serializer


def __pull_out_repetitions_states(
    instance: ExperimentAbstract,
) -> Tuple[Optional[int], Optional[str]]:
    """Pulls repetitions and states from ConcreteExperiment.

    Args:
        instance (ExperimentAbstract): Given Experiment

    Returns:
        repetitions, states: (None, None) if `instance` is of type
                             ExperimentTemplate.
                             If `instance` is of type ConcreteExperiment,
                             (repetitions, states) will be returned. Where the
                             `repetitions` is of type int and `states` str. The
                             `states` is a json-dumped list of dicts with the name
                             of the state as key and the repetition as value.
    """
    states: Optional[str] = None
    repetitions: Optional[int] = None
    if isinstance(instance, ConcreteExperiment):
        states = json.dumps(
            [(state.name, repetition) for repetition, state in instance.states]
        )
        repetitions = len(instance.states)
    return repetitions, states


def __add_stages_to_experiment_model(
    experiment_model_instance: ExperimentModel, stages: List[ExperimentStage]
) -> None:
    """Insert a list of ExperimentStages to an Experiment.

    A list of ExperimentStage Plain-Python-Objects will be inserted into the
    database and referenced, using the Many-To-Many field in the given
    ExperimentModel.

    Args:
        experiment_model_instance (ExperimentModel): Database entry of ExperimentModel
        stages (List[ExperimentStage]): A list of ExperimentStages
    """
    stage_ids: List[int] = pull_out_amnes_object_list_stored(stages)
    for stage_id in stage_ids:
        experiment_model_instance.stages.add(AmnesObjectModel.get_by_id(stage_id))


def _add_states_to_experiment_instance(
    experiment_instance: ConcreteExperiment, states: List[Tuple[str, int]]
) -> None:
    """Add to a ConcreteExperiment instance a list of states.

    Args:
        experiment_instance (ConcreteExperiment): The instance, where the states
                                                  will be added.
        states (List[Tuple[str, int]]): A list of states, formatted as such, that
                                        the first item in the tuple is defined by
                                        the name/ doc of the `ExperimentState` and
                                        the second item in tuple defines the value,
                                        used by the Enum class.
    """
    for repetition, (state_name, value) in enumerate(states):
        experiment_state = (
            ExperimentState.__dict__[state_name]  # type: ignore
            if state_name in ExperimentState.__dict__.keys()  # type: ignore
            else ExperimentState(value, state_name)
        )
        experiment_instance.set_state(repetition + 1, experiment_state)


class ExperimentTemplateSerializer(Serializer):
    """Maps data between ExperimentTemplate instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given ExperimentTemplate exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if an ExperimentTemplate with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, ExperimentTemplateModel)

    @staticmethod
    def insert(
        instance: ExperimentTemplate, parent: Optional[ExperimentSequenceModel] = None
    ) -> int:
        """Insert Plain-Python-Object ExperimentTemplate into the database.

        Args:
            instance (ExperimentTemplate): Non-Empty Plain-Python-Object
                                           ExperimentTemplate instance.
            parent (Optional[ExperimentSequenceModel]): Parent in ExperimentTemplate
                                                        will be ignored. Parental
                                                        reference can only be used in
                                                        ConcreteExperiment.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, ExperimentTemplate)
        return _experiment_insert(instance, ExperimentTemplateModel)

    @staticmethod
    def insert_bulk(
        instances: Sequence[ExperimentTemplate],
        parent: Optional[ExperimentSequenceModel] = None,
    ) -> List[int]:
        """Insert multiple Experiment into the database.

        Args:
            instances (List[ExperimentAbstract]): List of Non-Empty Experiment
                                                  instances.
            parent (Optional[ExperimentSequenceModel]): Parent in ExperimentTemplate
                                                        will be ignored. Parental
                                                        reference can only be used in
                                                        ConcreteExperiment.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        return _experiments_insert_bulk(instances, ExperimentTemplateModel)

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes an ExperimentTemplate by id from the database.

        Args:
            object_id (int): Index of entry in database

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentTemplate database-entry was not found.")
        _experiment_delete_by_id(object_id, ExperimentTemplateModel)

    @staticmethod
    def update_by_id(instance: ExperimentTemplate, object_id: int) -> None:
        """Updates a ExperimentTemplate entry in the database.

        Args:
            instance (ExperimentTemplate): Plain-Python-Object of
                                           ExperimentTemplate, will be updated
                                           in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        raise_if_incorrect_type(instance, ExperimentTemplate)
        if not ExperimentTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentTemplate database-entry was not found.")
        _experiment_update_by_id(instance, object_id, ExperimentTemplateModel)

    @staticmethod
    def get_by_id(object_id: int) -> ExperimentTemplate:
        """Returns Plain-Python-Object ExperimentTemplate from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ExperimentTemplate): Non-Empty Plain-Python-Object
                                           `ExperimentTemplate` instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentTemplate database-entry was not found.")
        amnes_object, stages, nodes, _, _ = _experiment_ingredients_get_by_id(
            object_id, ExperimentTemplateModel
        )
        experiment_instance = ExperimentTemplate(
            amnes_object.slug, amnes_object.name, amnes_object.description, stages,
        )
        experiment_instance.add_nodes(nodes)  # type: ignore
        experiment_instance.add_labels(amnes_object.labels)

        return experiment_instance


class ConcreteExperimentSerializer(Serializer):
    """Map data between ConcreteExperiment instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given ConcreteExperiment exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if a ConcreteExperiment with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, ConcreteExperimentModel)

    @staticmethod
    def insert(
        instance: ConcreteExperiment, parent: Optional[ExperimentSequenceModel] = None
    ) -> int:
        """Insert Plain-Python-Object ConcreteExperiment into the database.

        Args:
            instance (ConcreteExperiment): Non-Empty Plain-Python-Object
                                           ConcreteExperiment instance.
            parent (Optional[ExperimentSequenceModel]): Parental reference.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, ConcreteExperiment)
        return _experiment_insert(instance, ConcreteExperimentModel, parent)

    @staticmethod
    def insert_bulk(
        instances: Sequence[ConcreteExperiment],
        parent: Optional[ExperimentSequenceModel] = None,
    ) -> List[int]:
        """Insert multiple ConcreteExperiments into the database.

        Args:
            instances (List[ConcreteExperiment]): List of Non-Empty ConcreteExperiment
                                                  instances.
            parent (Optional[ExperimentSequenceModel]): Parental reference for all
                                                        ConcreteExperiments.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        return _experiments_insert_bulk(instances, ConcreteExperimentModel, parent)

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes a ConcreteExperiment by id from the database.

        Args:
            object_id (int): Index of entry in database

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperiment database-entry was not found.")
        _experiment_delete_by_id(object_id, ConcreteExperimentModel)

    @staticmethod
    def update_by_id(instance: ConcreteExperiment, object_id: int) -> None:
        """Updates a ConcreteExperiment entry in the database.

        Args:
            instance (ConcreteExperiment): Plain-Python-Object of
                                           ConcreteExperiment, will be updated
                                           in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        raise_if_incorrect_type(instance, ConcreteExperiment)
        if not ConcreteExperimentSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperiment database-entry was not found.")
        _experiment_update_by_id(instance, object_id, ConcreteExperimentModel)

    @staticmethod
    def update_states_by_id(
        states_items: ItemsView[int, ExperimentState], object_id: int
    ) -> None:
        """Updates ExperimentStates of a ConcreteExperiment entry in the database.

        This methods updates all states defined in `states_items` with the existing
        states, stored in the database. Existing state in the database, which is not
        covered by given `states_items` will not be deleted, rather stay unchanged!

        Args:
            states_items (ItemsView[int, ExperimentState]): ItemsView of dict
                    with all states which will update the states in the database.
                    The key is a positive number, which describes the repetition of
                    specified ExperimentState. The value describes the relative
                    ExperimentState.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        for repetition, state in states_items:
            raise_if_incorrect_type(repetition, int)
            raise_if_incorrect_type(state, ExperimentState)
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperiment database-entry was not found.")

        experiment_model: ConcreteExperimentModel = ConcreteExperimentModel.get_by_id(
            object_id
        )
        state_dict_old = {
            repetition: state_name
            for state_name, repetition in json.loads(experiment_model.states)
        }
        for repetition, state in states_items:
            state_dict_old[repetition] = state.name
        states_str: str = json.dumps(
            [(state, repetition) for repetition, state in state_dict_old.items()]
        )
        query_update = experiment_model.update(
            {"repetitions": len(state_dict_old), "states": states_str}
        ).where(ConcreteExperimentModel.id == object_id)
        query_update.execute()

    @staticmethod
    def get_by_id(object_id: int) -> ConcreteExperiment:
        """Returns Plain-Python-Object ConcreteExperiment from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ConcreteExperiment): Non-Empty Plain-Python-Object
                                           `ConcreteExperiment` instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperiment database-entry was not found.")

        (
            amnes_object,
            stages,
            nodes,
            repetitions,
            states,
        ) = _experiment_ingredients_get_by_id(object_id, ConcreteExperimentModel)
        experiment_instance = ConcreteExperiment(
            amnes_object.slug,
            amnes_object.name,
            amnes_object.description,
            stages,
            repetitions,
        )
        _add_states_to_experiment_instance(experiment_instance, json.loads(states))

        experiment_instance.add_nodes(nodes)  # type: ignore
        experiment_instance.add_labels(amnes_object.labels)
        return experiment_instance
