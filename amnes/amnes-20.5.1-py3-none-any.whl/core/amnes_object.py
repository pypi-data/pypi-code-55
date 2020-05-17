"""This module contains all necessary definitions for the AMNES object class.

Classes:
    AmnesObject: AMNES object class, from which all AMNES core classes inherit.
"""


from typing import List


class AmnesObject:
    """Abstract amnes object class, from which all amnes core classes inherit.

    This class defines an AMNES object with three main attributes slug,
    name and description. All classes that form the model for network
    experiments should inherit from this class.

    Attributes:
        slug (str): Short identifier for the AMNES object,
                    which must be a valid, non-empty string.
        name (str): Full name for the AMNES object.
        description (str): Custom description for the AMNES object.
        labels (List[str]): List of assigned labels.
    """

    def __init__(
        self, slug: str, name: str, description: str, labels: List[str] = None
    ) -> None:
        """AMNES object class constructor method.

        Args:
            slug (str): Short identifier for the AMNES object,
                        which must be a valid, non-empty string.
            name (str): Full name for the AMNES object.
            description (str): Custom description for the AMNES object.
            labels (List[str]): Custom list of labels for the AMNES object.
        """
        self.slug = slug
        self.name = name
        self.description = description
        self.__labels: List[str] = []
        if labels:
            self.add_labels(labels)

    def __eq__(self, other: object) -> bool:
        """Check equality between current AmnesObject instance and an arbitrary object.

        Args:
            other (object): Arbitrary object to be checked for equality
                            with this AmnesObject instance.

        Returns:
            bool: True if `other` is equal to the current AmnesObject instance,
                  otherwise returns false.

        Raises:
            TypeError: If `other` is not of type AmnesObject.
        """
        if not isinstance(other, AmnesObject):
            raise TypeError("The object to be compared to is not of type AmnesObject.")
        return (
            (self.slug == other.slug)
            and (self.name == other.name)
            and (self.description == other.description)
            and (set(self.labels) == set(other.labels))
        )

    @property
    def slug(self) -> str:
        """str: Short identifier for the AMNES object.

        Returns:
            slug (str): Short identifier for the AMNES object,
                        which must be a valid, non-empty string.
        """
        return self.__slug

    @slug.setter
    def slug(self, object_slug: str) -> None:
        """AMNES object slug Setter function.

        Args:
            object_slug (str): Short identifier for the AMNES object to be set.

        Raises:
            TypeError: If `object_slug` is not of type str.
            ValueError: If `object_slug` string is empty or only consists of whitespace.
        """
        if not isinstance(object_slug, str):
            raise TypeError("Amnes object slug is not of type string.")
        if (not object_slug) or (object_slug.isspace()):
            raise ValueError("The specified object slug must not be empty.")
        self.__slug = object_slug

    @property
    def name(self) -> str:
        """str: Full name for the AMNES object.

        Returns:
            name (str): Full name for the AMNES object.
        """
        return self.__name

    @name.setter
    def name(self, object_name: str) -> None:
        """AMNES object name Setter function.

        Args:
            object_name (str): Full name for the AMNES object to be set.

        Raises:
            TypeError: If `object_name` is not of type str.
        """
        if not isinstance(object_name, str):
            raise TypeError("Amnes object name is not of type string.")
        self.__name = object_name

    @property
    def description(self) -> str:
        """Custom description for the AMNES object.

        Returns:
            description (str): Custom description for the AMNES object.
        """
        return self.__description

    @description.setter
    def description(self, object_description: str) -> None:
        """AMNES object description Setter function.

        Args:
            object_description (str): Custom description for the AMNES object to be set.

        Raises:
            TypeError: If `object_description` is not of type str.
        """
        if not isinstance(object_description, str):
            raise TypeError("Amnes object description is not of type string.")
        self.__description = object_description

    @property
    def labels(self) -> List[str]:
        """List of currently assigned labels.

        Returns:
            labels (List[str]): List of currently assigned labels.
        """
        return self.__labels.copy()

    def add_labels(self, labels: List[str]) -> None:
        """Add new labels to the labels list.

        The given labels must be valid, non empty strings.

        Args:
            labels (List[str]): List of labels to be assigned.

        Raises:
            TypeError: If `labels` is not of type List or a label
                       is not of type string.
            ValueError: If a label in `labels` is not a valid, non-empty string.
        """
        if not isinstance(labels, List):
            raise TypeError("Given object labels are not a list.")

        labels_set: List[str] = []
        for label in labels.copy():
            if not isinstance(label, str):
                raise TypeError("Object label is not of type string.")
            if (not label) or (label.isspace()):
                raise ValueError("The specified object labels must not be empty.")
            if label in self.__labels:
                continue
            if label not in labels_set:
                labels_set.append(label)

        self.__labels.extend(labels_set)

    def remove_labels(self, labels: List[str]) -> None:
        """Remove labels from the labels list.

        The given labels must be valid, non empty strings.

        Args:
            labels (List[str]): List of labels to be removed.

        Raises:
            TypeError: If `labels` is not of type List or a label
                       is not of type string.
            ValueError: If a label in `labels` is not a valid, non-empty string.
        """
        if not isinstance(labels, List):
            raise TypeError("Given object labels are not a list.")

        labels_set: List[str] = []
        for label in labels.copy():
            if not isinstance(label, str):
                raise TypeError("Object label is not of type string.")
            if (not label) or (label.isspace()):
                raise ValueError("The passed object labels must not be empty.")
            if label not in self.__labels:
                continue
            if label not in labels_set:
                labels_set.append(label)

        for label in labels_set:
            self.__labels.remove(label)
