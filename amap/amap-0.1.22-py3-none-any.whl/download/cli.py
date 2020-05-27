import tempfile
from pathlib import Path

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from amap.download.download import amend_cfg, download


home = Path.home()
DEFAULT_DOWNLOAD_DIRECTORY = home / ".amap"
temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = Path(temp_dir.name)


# allen_2017 (default) and allen_2017_10um are the same
atlas_urls = {
    "allen_2017_10um": "https://gin.g-node.org/cellfinder/atlas/raw/master/allen_2017_10um.tar.gz",
    "allen_2017_100um": "https://gin.g-node.org/cellfinder/atlas/raw/master/allen_2017_100um.tar.gz",
}

download_requirements_gb = {
    "allen_2017_10um": 1.8,
    "allen_2017_100um": 0.003,
}

extract_requirements_gb = {
    "allen_2017_10um": 11.5,
    "allen_2017_100um": 0.015,
}


def atlas_download(atlas, atlas_dir, download_path):
    # Check if all the 4 .nii files are in the directory, else download again:
    atlas_dir = atlas_dir / "atlas"
    if len(list((atlas_dir / atlas).glob("*.nii"))) < 4:
        atlas_dir.mkdir(exist_ok=True, parents=True)
        download(
            download_path,
            atlas_urls[atlas],
            install_path=atlas_dir,
            download_requires=download_requirements_gb[atlas],
            extract_requires=extract_requirements_gb[atlas],
        )

    else:
        print(
            f"Complete atlas already exists at "
            f"{atlas_dir}."
            f" Skipping download"
        )


def download_directory_parser(parser):
    parser.add_argument(
        "--install-path",
        dest="install_path",
        type=Path,
        default=DEFAULT_DOWNLOAD_DIRECTORY,
        help="The path to install files to.",
    )
    parser.add_argument(
        "--download-path",
        dest="download_path",
        type=Path,
        default=temp_dir_path,
        help="The path to download files into.",
    )
    parser.add_argument(
        "--no-amend-config",
        dest="no_amend_config",
        action="store_true",
        help="Don't amend the config file",
    )
    return parser


def atlas_parser(parser):
    parser.add_argument(
        "--no-atlas",
        dest="no_atlas",
        action="store_true",
        help="Don't download the atlas",
    )
    parser.add_argument(
        "--atlas",
        dest="atlas",
        type=str,
        default="allen_2017_10um",
        help="The atlas to use",
    )
    return parser


def download_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser = atlas_parser(parser)
    parser = download_directory_parser(parser)
    return parser


def main():
    args = download_parser().parse_args()
    if not args.no_atlas:
        atlas_download(args.atlas, args.install_path, args.download_path)
    if not args.no_amend_config:
        print(f"install: {args.install_path}")
        amend_cfg(
            new_atlas_folder=args.install_path, atlas=args.atlas,
        )


if __name__ == "__main__":
    main()
