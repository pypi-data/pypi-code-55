import dataclasses

from .tomlfile import TomlFile


@dataclasses.dataclass
class Package:

    name: str
    version: str = "0.1.0"

    @classmethod
    def from_path(cls, path):
        """
        Create package from path.

        This factory method is used to create a package instance
        from the given path. The path must represent a package file
        containing information about the package (i.e. pyproject.toml)
        """
        pkgfile = TomlFile(path)
        pkgfile.read()
        return cls(
            name=pkgfile.get_value("tool.poetry.name"),
            version=pkgfile.get_value("tool.poetry.version"),
        )

