import os

import yaml

from rainbowpy.colormap import ColorMap
from rainbowpy.file_utils import (file_existing_and_readable,
                                  get_path_of_user_dir,
                                  if_directory_not_existing_then_make)


def add_custom_cmaps():

    if_directory_not_existing_then_make(get_path_of_user_dir())

    user_maps_file = os.path.join(get_path_of_user_dir(), "custom_maps.yml")

    if file_existing_and_readable(user_maps_file):

        with open(user_maps_file, "r") as f:

            cmaps = yaml.load(f, Loader=yaml.SafeLoader)

        for map_name, colors in cmaps.items():

            ColorMap.from_hex(*colors, discrete=False, name=map_name)
