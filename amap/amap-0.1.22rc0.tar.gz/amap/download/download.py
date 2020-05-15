import shutil
import tarfile
import urllib.request

from imlib.general.system import disk_free_gb
from imlib.general.config import get_config_obj
from imlib.source import source_files


class DownloadError(Exception):
    pass


def download_file(destination_path, file_url):
    direct_download = True
    file_url = file_url.format(int(direct_download))
    print("Downloading...")
    with urllib.request.urlopen(file_url) as response:
        with open(destination_path, "wb") as outfile:
            shutil.copyfileobj(response, outfile)


def extract_file(tar_file_path, destination_path):
    tar = tarfile.open(tar_file_path)
    tar.extractall(path=destination_path)
    tar.close()


# TODO: check that intermediate folders exist
def download(
    download_dir_path,
    url,
    install_path=None,
    download_requires=None,
    extract_requires=None,
):
    COMPRESSED_FILENAME = "atlas.tar.gz"

    if not download_dir_path.exists():
        raise DownloadError(f"Could not find directory '{download_dir_path}' ")

    if (download_requires is not None) and (
        disk_free_gb(download_dir_path) < download_requires
    ):
        raise DownloadError(
            f"Insufficient disk space in {download_dir_path} to"
        )

    if install_path is not None:
        if not install_path.exists():
            raise DownloadError(f"Could not find directory '{install_path}' ")

        if (extract_requires is not None) and (
            disk_free_gb(install_path) < extract_requires
        ):
            raise DownloadError(f"Insufficient disk space in {install_path}")
            raise DownloadError(
                f"Insufficient disk space in {install_path} to install atlas"
            )

    # Create full filename...
    download_filename = download_dir_path / COMPRESSED_FILENAME
    # ..download...
    download_file(download_filename, url)
    if install_path is not None:
        extract_file(download_filename, install_path)
        download_filename.unlink()


def amend_cfg(new_atlas_folder=None, atlas=None):
    """
    Updates the registration config file to point to the correct atlas path
    :param new_atlas_folder:
    """
    print("Ensuring custom config file is correct")

    original_config = source_files.source_config_amap()
    new_config = source_files.source_custom_config_amap()
    if new_atlas_folder is not None:
        write_atlas_to_cfg(
            new_atlas_folder, atlas, original_config, new_config
        )


def write_atlas_to_cfg(atlas_folder, atlas, orig_config, custom_config):
    """ Write configuration of an atlas over a preexisting config file
    :param atlas_folder:
    :param atlas:
    :param orig_config:
    :param custom_config:
    :return:
    """
    config_obj = get_config_obj(orig_config)
    atlas_conf = config_obj["atlas"]
    orig_base_directory = atlas_conf["base_folder"]

    with open(orig_config, "r") as in_conf:
        data = in_conf.readlines()
    for i, line in enumerate(data):
        data[i] = line.replace(
            f"base_folder = '{orig_base_directory}",
            f"base_folder = '{atlas_folder / atlas}",
        )
    with open(custom_config, "w") as out_conf:
        out_conf.writelines(data)
