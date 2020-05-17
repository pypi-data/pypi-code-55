"""This module contains the Serializer for the AmnesObject class.

Classes:
    AmnesObjectSerilizer: Concrete Serializer for the AmnesObject class.
"""
from typing import Any, List, Optional

from ...core.amnes_object import AmnesObject
from ..models import AmnesObjectModel, AnnotationModel, LabelModel
from .base import Serializer


class AmnesObjectSerializer(Serializer):
    """Map data between AmnesObject instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given AmnesObject exists in the database.

        Args:
            object_id (int): Index of entry in database

        Returns:
            bool: True if an exact representation of AmnesObject exists in
                  database, False if not.
        """
        query = AmnesObjectModel.select().where(AmnesObjectModel.id == object_id)
        if not query.exists():
            return False
        return True

    @staticmethod
    def insert(instance: AmnesObject, parent: Optional[Any] = None) -> int:
        """Insert Plain-Python-Object AmnesObject into the database.

        Args:
            instance (AmnesObject): Non-Empty Plain-Python-Object AmnesObject instance.
            parent (Optional[Any]): This serializer does not need a parental reference.
                                    This parameter will be ignored.

        Returns:
            object_id (int): Index of entry in database

        Raises:
            TypeError: If `ìnstance` is not of type `AmnesObject`.
        """
        if not isinstance(instance, AmnesObject):
            raise TypeError("The given `instance` is not of type AmnesObject.")

        annotation_instance = AnnotationModel.create(description=instance.description)
        AmnesObjectSerializer.__insert_labels(instance.labels, annotation_instance)
        amnes_object = AmnesObjectModel.create(
            slug=instance.slug, name=instance.name, annotation=annotation_instance
        )
        return amnes_object.get_id()

    @staticmethod
    def __insert_labels(
        label_list: List[str], annotation_model: Optional[AnnotationModel] = None
    ) -> List[int]:
        """Inserts a list of labels into the database.

        Args:
            label_list (List[str]): The labels which will be inserted
                                    into the database.
            annotation_model (Optional[AnnotationModel]): Reference for labels.
                                                         This method will add label
                                                         references to given
                                                         AnnotationModel.

        Returns:
            label_references (List[int]): A reference-list of labels.
        """
        label_instances: List[int] = []
        for label in label_list:
            label_instance, _ = LabelModel.get_or_create(name=label)
            label_instances.append(label_instance)

        if annotation_model:
            annotation_model.labels.add(label_instances)
        return label_instances

    @staticmethod
    def insert_bulk(
        instances: List[AmnesObject], parent: Optional[Any] = None
    ) -> List[int]:
        """Insert multiple AmnesObjects into the database.

        Args:
            instances (List[AmnesObject]): List of Non-Empty AmnesObject instances.
            parent (Optional[Any]): This serializer does not need a parental reference.
                                    This parameter will be ignored.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for instance in instances:
            instances_ids.append(AmnesObjectSerializer.insert(instance))
        return instances_ids

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Delete an AmnesObject by id from the database.

        Args:
            object_id (int): Index of entry in database

        Raises:
            ValueError: If `instance` does not exist in the database.
        """
        if not AmnesObjectSerializer.exists_by_id(object_id):
            raise ValueError(
                "Given index of an AmnesObject does not exist in database."
            )
        amnes_object_model_instance: AmnesObjectModel = AmnesObjectModel.get_by_id(
            object_id
        )
        AmnesObjectSerializer.__delete_labels(amnes_object_model_instance)
        amnes_object_model_instance.annotation.labels.clear()
        amnes_object_model_instance.annotation.delete_instance()
        AmnesObjectModel.delete_by_id(object_id)

    @staticmethod
    def __delete_labels(aom_instance: AmnesObjectModel) -> None:
        """Deletes all safely deletable labels of given AmnesObjectModel instance.

        Args:
            aom_instance (AmnesObjectModel): Selected AmnesObjectModel instance.
        """
        selected_annotation = aom_instance.annotation
        labels = AmnesObjectSerializer.__get_deletable_labels(selected_annotation)
        for label in labels:
            label.delete_instance()

    @staticmethod
    def __get_deletable_labels(root_annotation: AnnotationModel,) -> List[LabelModel]:
        """Returns a list of safely deletable labels of given AnnotationModel instance.

        Args:
            root_annotation (AnnotationModel): Root annotation, used to define
                                               the scope of label deletion.

        Returns:
            deletable_labels (List[LabelModel]): Returns a list of labels, which can
                                                 safely be deleted.
        """
        deletable_labels: List[LabelModel] = []
        for label in root_annotation.labels:
            other_annotation_exists = False
            for annotation in label.annotations:
                if annotation.id != root_annotation.id:
                    other_annotation_exists = True
            if not other_annotation_exists:
                deletable_labels.append(label)
        return deletable_labels

    @staticmethod
    def update_by_id(instance: AmnesObject, object_id: int) -> None:
        """Update a AmnesObject in the database.

        Args:
            instance (AmnesObject): Plain-Python-Object AmnesObject,
                                    will be updated in the database. AmnesObject is
                                    identified by a slug.
            object_id (int): Unique identification of data-entry

        Raises:
            ValueError: If `instance` does not exist in the database.
        """
        if not AmnesObjectSerializer.exists_by_id(object_id):
            raise ValueError("Given AmnesObject does not exist in database.")

        update_query = AmnesObjectModel.update(
            {AmnesObjectModel.slug: instance.slug, AmnesObjectModel.name: instance.name}
        ).where(AmnesObjectModel.id == object_id)
        update_query.execute()

        ao_model_instance = AmnesObjectModel.get_by_id(object_id)

        update_query = AnnotationModel.update(
            {AnnotationModel.description: instance.description}
        ).where(AnnotationModel.id == ao_model_instance.annotation.id)
        update_query.execute()

        AmnesObjectSerializer.__delete_labels(ao_model_instance)
        annotation_instance = AnnotationModel.get_by_id(ao_model_instance.annotation.id)
        annotation_instance.labels.clear()
        AmnesObjectSerializer.__insert_labels(instance.labels, annotation_instance)

    @staticmethod
    def get_by_id(object_id: int) -> AmnesObject:
        """Insert Plain-Python-Object AmnesObject into the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (AmnesObject): Non-Empty Plain-Python-Object AmnesObject instance.
        """
        amnes_object_model = AmnesObjectModel.get_by_id(object_id)
        label_list = [label.name for label in amnes_object_model.annotation.labels]
        return AmnesObject(
            slug=amnes_object_model.slug,
            name=amnes_object_model.name,
            description=amnes_object_model.annotation.description,
            labels=label_list,
        )
