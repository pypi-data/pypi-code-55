from dataclasses import  dataclass

@dataclass
class TrainerConfig:
    model_str: str = "checkpoints"
    model_save_frequency: int = 1
    device: str = "cpu"
    epoch_num: int = 50
    progress_bar: bool = True