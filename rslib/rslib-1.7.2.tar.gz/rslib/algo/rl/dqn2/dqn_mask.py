import ray

from ray.rllib.models import ModelCatalog
from ray.rllib.models.model import Model
from ray.rllib.utils.annotations import override
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env
from rslib.algo.rl.dqn2.dqn import DQNTrainer
# from ray.rllib.agents.dqn import DQNTrainer

from rslib.algo.rl.dqn2.fcnet import FullyConnectedNetwork

ray.init()

# ray.init(memory= 1000000000, object_store_memory =500000000)

def get_dqn_mask(env, config):
    # ModelCatalog.register_custom_model("pre_model", FullyConnectedNetwork)
    trainer = DQNTrainer(
        env=env,
        config={
            **config,
        }
    )
    return trainer
