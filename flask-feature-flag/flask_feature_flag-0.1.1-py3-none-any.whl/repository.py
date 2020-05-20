from .models import FeatureFlag


class FeatureRepository:
    """Class for search in the model :class:`FeatureFlag`"""

    @staticmethod
    def find_all(**kwargs) -> list:
        """Search :obj:`FeatureFlag`.

        Args:
            kwargs

        Returns:
            list[FeatureFlag]
        """
        return FeatureFlag.objects(**kwargs)

    @staticmethod
    def find_one(**kwargs) -> FeatureFlag:
        """Search a :obj:`FeatureFlag`.

        Args:
            kwargs

        Returns:
            FeatureFlag: o None
        """
        return FeatureFlag.objects(**kwargs).first()
