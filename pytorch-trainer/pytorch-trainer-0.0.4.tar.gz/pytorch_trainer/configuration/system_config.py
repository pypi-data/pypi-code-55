from dataclasses import  dataclass



@dataclass
class SystemConfig:
    seed: int = 42
    cudnn_benchmark_enabled: bool = False
    cudnn_deterministic: bool = False