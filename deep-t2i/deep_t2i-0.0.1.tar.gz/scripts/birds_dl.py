import os
from deep_t2i.constants import Birds

img_url = Birds.img_url
cap_url = Birds.cap_url
data_dir = Birds.data_dir
tmp_dir = data_dir/'tmp'
imgs_dir = data_dir/'imgs'
caps_dir = data_dir/'caps'

os.system(f"mkdir -p {tmp_dir}")

# Birds images
os.system(f"curl {img_url} --output {tmp_dir/'CUB_200_2011.tgz'}")

os.system(f"7z x -tgzip -so {tmp_dir/'CUB_200_2011.tgz'} | 7z x -si -ttar -o{tmp_dir}")
os.system(f"mv {tmp_dir/'CUB_200_2011/images'} {imgs_dir}")
os.system(f"mv {tmp_dir/'CUB_200_2011/images.txt'} {data_dir}")
os.system(f"mv {tmp_dir/'CUB_200_2011/train_test_split.txt'} {data_dir}")
os.system(f"mv {tmp_dir/'CUB_200_2011/bounding_boxes.txt'} {data_dir}")

# Birds Captions
os.system(f"curl -L '{cap_url}' --output {tmp_dir/'birds.zip'}")

os.system(f"7z x {tmp_dir/'birds.zip'} -o{tmp_dir}")
os.system(f"7z x {tmp_dir/'birds/text.zip'} -o{tmp_dir/'birds/'}")
os.system(f"mv {tmp_dir/'birds/text'} {caps_dir}")

# Clean
os.system(f"rm -rf {tmp_dir}")
