"""Define the Enumeration for the datu_api.
"""

from enum import Enum


# TODO(phuc): move to a different files.
class RequestType(Enum):
    """Different request types.
    """
    GET = 1
    POST = 2


class RouteType(str, Enum):
    """Different route names handled by the backend.
    """
    CREATE_PROJECT = 'create_project'
    PROJECT_LOOKUP = 'project_lookup'
    LIST_PROJECTS = 'list_projects'
    SAMPLING = 'sampling'
    UPLOAD = 'upload'
    START_ANNOTATION = 'start_annotation'
    CREATE_TRAINER = 'create_trainer'
    LIST_TRAINER = 'list_trainer'
    START_TRAINING = 'start_training'


class SamplingStrategy(str, Enum):
    """Enumeration for task type"""
    RANDOM = 'random'
    ACTIVE = 'active'


class DataType(str, Enum):
    """Type of input."""
    IMAGE = 'image'
    VIDEO = 'video'


class TaskType(str, Enum):
    """Enumeration for task type"""
    DETECTION_2D = 'detection2d'
    DETECTION_3D = 'detection3d'
    SEGMENTATION_SEMANTIC = 'segmentation_semantic'
    SEGMENTATION_INSTANCE = 'segmentation_instance'
    TRACKING_2D = 'tracking2d'
    TRACKING_3D = 'tracking3d'

class ModelType(str, Enum):
    """Enumeration for model type"""
    DETECTRON2 = "detectron2"
    CUSTOM = "custom"
