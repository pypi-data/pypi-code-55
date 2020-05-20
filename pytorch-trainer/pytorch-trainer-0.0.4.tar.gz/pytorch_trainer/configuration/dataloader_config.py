from dataclasses import dataclass

@dataclass
class DataloaderConfig:
    batch_size: int = 250
    num_workers: int = 5
