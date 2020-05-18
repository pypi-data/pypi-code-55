import os
import gdown
from deep_t2i.constants import AnimeHeads

url = AnimeHeads.url
data_dir = AnimeHeads.data_dir
tmp_dir = data_dir/'tmp'

os.system(f"mkdir -p {tmp_dir}")
gdown.download(url, str(tmp_dir/'data.zip'), True)
os.system(f"7z x {tmp_dir/'data.zip'} -o{tmp_dir}")

os.system(f"mv {tmp_dir/'extra_data/images'} {data_dir/'imgs'}")
os.system(f"mv {tmp_dir/'extra_data/tags.csv'} {data_dir}")
os.system(f"rm -rf {tmp_dir}")