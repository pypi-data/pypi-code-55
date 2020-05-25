from enum import Enum


class PipelineStatusTypes(Enum):
    NotStarted = 1
    Failed = 2
    Succeeded = 3
    Running = 4


class MetricStatusTypes(Enum):
    Incomplete = 1
    Completed = 2
    AwaitingActualCost = 3
    Failed = 4


class GoogleServices(Enum):
    BigQuery = 1
    GCAIP = 2
    Kubeflow = 3
    Storage = 4
    Dataflow = 5
