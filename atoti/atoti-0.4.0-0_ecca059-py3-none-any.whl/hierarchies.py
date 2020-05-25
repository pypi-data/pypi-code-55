"""Hierarchies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping, Sequence, Union

from ._mappings import DelegateMutableMapping
from ._repr_utils import convert_repr_json_to_html, repr_json_hierarchies
from .hierarchy import Hierarchy
from .level import Level

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .cube import Cube
    from .store import Column


DEFAULT_DIMENSION_NAME = "Hierarchies"


def _retrieve_hierarchies(java_api: JavaApi, cube: Cube) -> Mapping[str, Hierarchy]:
    """Retrieve the hierarchies from the cube.

    Args:
        java_api: the Java API
        cube: the cube

    """
    return java_api.retrieve_hierarchies(cube)


if TYPE_CHECKING:
    # We import Column in TYPE_CHECKING so no problem here
    LevelOrColumn = Union[Level, Column]  # pylint: disable=used-before-assignment


@dataclass(frozen=True)
class Hierarchies(DelegateMutableMapping[str, Hierarchy]):
    """Manage the hierarchies."""

    _java_api: JavaApi = field(repr=False)
    _cube: Cube = field(repr=False)

    def _get_underlying(self) -> Mapping[str, Hierarchy]:
        """Fetch the hierarchies from the JVM each time they are needed."""
        return _retrieve_hierarchies(self._java_api, self._cube)

    def __getitem__(self, key: str) -> Hierarchy:
        """Return the hierarchy with the given name."""
        hierarchy = self._java_api.retrieve_hierarchy(self._cube, key)
        if not hierarchy:
            raise KeyError(f"Unknown hierarchy: {key}")
        return hierarchy

    def __setitem__(
        self,
        key: str,
        value: Union[Sequence[LevelOrColumn], Mapping[str, LevelOrColumn]],
    ):
        """Add the passed hierarchy or edit the existing one.

        Args:
            key: The name of the hierarchy to add
            value: The levels of the hierarchy. Either a list of levels or store columns, or
                a mapping from level name to level value or a store column.
        """
        if isinstance(value, Sequence):
            value = {column.name: column for column in value}
        elif not isinstance(value, Mapping):
            raise ValueError(
                f"Levels argument is expected to be a sequence or a mapping but is "
                f"{str(type(value).__name__)}"
            )
        # convert to Level
        levels: Mapping[str, Level] = {
            levelName: levelOrColumn
            if isinstance(levelOrColumn, Level)
            else Level(levelName, levelOrColumn.name, "object")
            for (levelName, levelOrColumn) in value.items()
        }

        hierarchy = self._java_api.retrieve_hierarchy(self._cube, key)
        if hierarchy:
            # Edit the existing hierarchy if there is one
            hierarchy.levels = levels
        else:
            # Create the new hierarchy
            self._java_api.create_or_update_hierarchy(
                self._cube, DEFAULT_DIMENSION_NAME, key, levels
            )
            self._java_api.refresh_pivot()

    def __delitem__(self, key: str):
        """Delete the hierarchy.

        Args:
            key: the name of the hierarchy to delete.

        """
        try:
            hierarchy: Hierarchy = self[key]
            self._java_api.drop_hierarchy(
                self._cube, hierarchy.dimension, hierarchy.name
            )
            self._java_api.refresh_pivot()
        except KeyError:
            raise KeyError(f"{key} is not an existing hierarchy.")

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchies(self)
