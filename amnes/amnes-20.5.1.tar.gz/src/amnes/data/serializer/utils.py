"""This module contains helper methods for serializer classes."""
from typing import Any, List, Sequence, Type

from ...core.amnes_object import AmnesObject
from ..models import BaseModel
from .amnes_object import AmnesObjectSerializer


def pull_out_amnes_object(instance: AmnesObject) -> AmnesObject:
    """Pulls out an AmnesObject of any instance of a subclass of AmnesObject class.

    Args:
        instance (AmnesObject): Any instance of a subclass of AmnesObject class.

    Returns:
        amnes_object (AmnesObject): Returns the generated AmnesObject
    """
    raise_if_incorrect_type(instance, AmnesObject)
    return AmnesObject(
        instance.slug, instance.name, instance.description, instance.labels,
    )


def pull_out_amnes_object_stored(instance: AmnesObject) -> int:
    """Pulls out AmnesObject of a given Core-PPO and saves it in the database.

    Args:
        instance (AmnesObject): Any instance of a subclass of AmnesObject class.

    Returns:
        object_id (int): Returns the unique id of the stored AmnesObjectModel instance.

    """
    amnes_object = pull_out_amnes_object(instance)
    return AmnesObjectSerializer.insert(amnes_object)


def pull_out_amnes_object_list_stored(instances: Sequence[AmnesObject]) -> List[int]:
    """Pulls out AmnesObjects of a given Core-PPOs and saves it in the database.

    Args:
        instances (List[AmnesObject]): List of instances of a subclass of
                                       AmnesObject class.

    Returns:
        object_ids (List[int]): Returns a list of unique id ofs the stored
                             AmnesObjectModel instances.

    """
    instances_ids: List[int] = []
    for instance in instances:
        amnes_object = pull_out_amnes_object(instance)
        instances_ids.append(AmnesObjectSerializer.insert(amnes_object))
    return instances_ids


def raise_if_invalid_object_id(object_id: int) -> None:
    """Checks if `object_id` is a valid id.

    A valid id is an integer, higher than 0.

    Args:
        object_id (int): Unique identifier, referencing to data-entry
                      inside the database.

    Raises:
        ValueError: If the `object_id` is not a valid id.
    """
    if object_id < 1:
        raise ValueError("The `object_id` must be 1 or higher.")


def raise_if_incorrect_type(instance: Any, compared_type: Type) -> None:
    """Raises TypeError if `instance` is not of type `compared_type`.

    Args:
        instance (Any): Instance of any class
        compared_type (Type): Type to compare `instance` to.

    Raises:
        TypeError: If `instance` is not of type `compared_type`.
    """
    if not isinstance(instance, compared_type):
        raise TypeError(
            f"Given `instance` is of type {instance.__class__.__name__} "
            f"instead of type {compared_type.__name__}."
        )


def model_instance_exists_by_id(object_id: int, model: Type[BaseModel]) -> bool:
    """Check if a given ExperimentNode by id exists in the database.

    Args:
        object_id (int): Index of entry in database.
        model (Type[BaseModel]): Model used for exists-query.

    Returns:
        bool: True if an instance of given model with the given `object_id` exists in
              the database, False if not.
    """
    query = model.select().where(model.id == object_id)
    return query.exists()
