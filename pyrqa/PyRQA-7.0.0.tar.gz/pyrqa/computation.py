#!/usr/bin/env python

"""
Factories for creating recurrence analysis computations.
"""

from pyrqa.analysis_type import Joint
from pyrqa.exceptions import UnsupportedNeighbourhoodException, \
    UnsupportedAnalysisTypeException
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor, \
    Unthresholded

from pyrqa.variants.rp.radius.engine import Engine as RPRadiusEngine
from pyrqa.variants.rp.unthresholded.engine import Engine as RPUnthresholdedEngine
from pyrqa.variants.rqa.radius.engine import Engine as RQAEngine
from pyrqa.variants.jrp.radius.engine import Engine as JRPEngine
from pyrqa.variants.jrqa.radius.engine import Engine as JRQAEngine

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPComputation(object):
    """
    Factory for creating recurrence plot computations.
    """
    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create RP computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """
        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RPRadiusEngine(settings,
                                  **kwargs)
        elif isinstance(settings.neighbourhood, Unthresholded):
            return RPUnthresholdedEngine(settings,
                                         **kwargs)
        else:
            raise UnsupportedNeighbourhoodException(
                "Neighbourhood '%s' is not supported regarding recurrence plot computations!" % settings.neighbourhood.__class__.__name__)


class JRPComputation(object):
    """
    Factory for creating joint recurrence plot computations.
    """
    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create JRP computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """
        if settings.analysis_type is Joint:
            if not isinstance(settings.settings_1.neighbourhood, Unthresholded) and not isinstance(settings.settings_2.neighbourhood, Unthresholded):
                return JRPEngine(settings,
                                 **kwargs)
            else:
                raise UnsupportedNeighbourhoodException(
                    "Combination of neighbourhoods '%s' and '%s' is not supported regarding joint recurrence plot computations!" % (settings.settings_1.neighbourhood.__class__.__name__,
                                                                                                                                    settings.settings_2.neighbourhood.__class__.__name__))
        else:
            raise UnsupportedAnalysisTypeException(
                "Analysis type '%s' is not supported regarding JRP computations." % settings.analysis_type)


class RQAComputation(object):
    """
    Factory for creating recurrence quantification analysis computations.
    """
    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create recurrence plot computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """

        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RQAEngine(settings,
                             **kwargs)
        else:
            raise UnsupportedNeighbourhoodException(
                "Neighbourhood '%s' is not supported regarding recurrence quantification analysis computations!" % settings.neighbourhood.__class__.__name__)


class JRQAComputation(object):
    """
    Factory for creating joint recurrence quantification analysis computations.
    """
    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create JRQA computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """
        if settings.analysis_type is Joint:
            if not isinstance(settings.settings_1.neighbourhood, Unthresholded) and not isinstance(settings.settings_2.neighbourhood, Unthresholded):
                return JRQAEngine(settings,
                                  **kwargs)
            else:
                raise UnsupportedNeighbourhoodException(
                    "Combination of neighbourhoods '%s' and '%s' is not supported regarding joint recurrence quantification analysis computations!" % (settings.settings_1.neighbourhood.__class__.__name__,
                                                                                                                                                       settings.settings_2.neighbourhood.__class__.__name__))
        else:
            raise UnsupportedAnalysisTypeException(
                "Analysis type '%s' is not supported regarding JRP computations." % settings.analysis_type)
