import os
import shutil
import subprocess

from red_dead.items import path_originals, base_dir


submod_path = base_dir / 'RDR2CollectorsMap'
os.chdir(submod_path)
subprocess.check_call(['git', 'pull', 'origin', 'master'])

for cached_path, submod_path in path_originals.items():
    shutil.copy(submod_path, cached_path)
