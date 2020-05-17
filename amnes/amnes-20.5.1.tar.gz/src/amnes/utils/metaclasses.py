"""This module contains metaclasses for AMNES.

Classes:
    SingletonABCMeta: Abstract Singleton Metaclass.
    SingletonMeta: Singleton Metaclass.
"""
from __future__ import annotations

from abc import ABCMeta
from typing import Any, Dict, Mapping, Sequence, Type


class SingletonABCMeta(ABCMeta):
    """Abstract Singleton Metaclass.

    All classes inheriting from this class can be instantiated once.
    """

    _instances: Dict[SingletonABCMeta, Type[SingletonABCMeta]] = {}

    def __call__(
        cls, *args: Sequence[Any], **kwargs: Mapping[Any, Any]
    ) -> Type[SingletonABCMeta]:
        """Returns the instance of the class.

        Args:
            cls (SingletonABCMeta): Class which is defined by inheritance.
            *args (Sequence[Any]): Arguments for class.__call__.
            **kwargs (Mapping[Any, Any]): Keyword arguments for class.__call__.

        Returns:
            Type[SingletonABCMeta]: Instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonMeta(type):
    """Singleton Metaclass.

    All classes inheriting from SingletonMeta can be instantiated once.
    """

    _instances: Dict[SingletonMeta, Type[SingletonMeta]] = {}

    def __call__(
        cls, *args: Sequence[Any], **kwargs: Mapping[Any, Any]
    ) -> Type[SingletonMeta]:
        """Returns the instance of the class.

        Creates an instance of a class if it does not exist yet.

        Args:
            cls (SingletonMeta): Class which is defined by inheritance.
            *args (Sequence[Any]): Arguments for class.__call__.
            **kwargs (Mapping[Any, Any]): Keyword arguments for class.__call__.

        Returns:
            Type[SingletonMeta]: Instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
