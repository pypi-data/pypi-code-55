from typing import Tuple, Union
from pydantic import BaseModel
import subprocess


STATS_CMD = "/sbin/zfs get -H -p compressratio,used,avail -o value {filesystem}"
class StatusModel(BaseModel):
    total_used_storage: float
    total_free_storage: float
    compression_ratio: float

def get_status(pool: str) -> Tuple[bool, Union[StatusModel,str]]:
   
    cp = subprocess.run(STATS_CMD.format(filesystem=pool).split(), capture_output=True)
    if cp.returncode != 0:
        return (False, "Command failed with error:{}".format(cp.stderr))
    data = cp.stdout.decode('utf-8').split()
    return (True, StatusModel(
        total_used_storage = int(data[1]),
        total_free_storage = int(data[2]),
        compression_ratio = float(data[0])
    ))

