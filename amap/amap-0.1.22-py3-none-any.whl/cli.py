import os
import logging
import tempfile
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from fancylog import fancylog
from pathlib import Path
from shutil import copyfile

from micrometa.micrometa import SUPPORTED_METADATA_TYPES
from imlib.general.system import ensure_directory_exists
from imlib.general.numerical import check_positive_int, check_positive_float
from imlib.image.metadata import define_pixel_sizes
from imlib.general.config import get_config_obj
from imlib.source import source_files

from amap.download.cli import atlas_parser, download_directory_parser
from amap.main import main as register
from amap.download.cli import atlas_download
from amap.download.download import amend_cfg
import amap as program_for_log


temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = temp_dir.name


def register_cli_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser = cli_parse(parser)
    parser = visualisation_parser(parser)
    parser = registration_parse(parser)
    parser = pixel_parser(parser)
    parser = geometry_parser(parser)
    parser = misc_parse(parser)
    parser = atlas_parser(parser)
    parser = download_directory_parser(parser)

    return parser


def cli_parse(parser):
    cli_parser = parser.add_argument_group("amap registration options")

    cli_parser.add_argument(
        dest="image_paths",
        type=str,
        help="Path to the directory of the image files. Can also be a text"
        "file pointing to the files.",
    )

    cli_parser.add_argument(
        dest="registration_output_folder",
        type=str,
        help="Directory to save the cubes into",
    )

    cli_parser.add_argument(
        "-d",
        "--downsample",
        dest="downsample_images",
        type=str,
        nargs="+",
        help="Paths to N additional channels to downsample to the same "
        "coordinate space. ",
    )
    return parser


def misc_parse(parser):
    misc_parser = parser.add_argument_group("Misc options")
    misc_parser.add_argument(
        "--n-free-cpus",
        dest="n_free_cpus",
        type=check_positive_int,
        default=4,
        help="The number of CPU cores on the machine to leave "
        "unused by the program to spare resources.",
    )

    misc_parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Debug mode. Will increase verbosity of logging and save all "
        "intermediate files for diagnosis of software issues.",
    )
    misc_parser.add_argument(
        "--metadata",
        dest="metadata",
        type=Path,
        help="Path to the metadata file. Supported formats are '{}'.".format(
            SUPPORTED_METADATA_TYPES
        ),
    )
    return parser


def pixel_parser(parser):
    pixel_opt_parser = parser.add_argument_group(
        "Options to define pixel sizes of raw data"
    )
    pixel_opt_parser.add_argument(
        "-x",
        "--x-pixel-um",
        dest="x_pixel_um",
        type=check_positive_float,
        help="Pixel spacing of the data in the first "
        "dimension, specified in um.",
    )
    pixel_opt_parser.add_argument(
        "-y",
        "--y-pixel-um",
        dest="y_pixel_um",
        type=check_positive_float,
        help="Pixel spacing of the data in the second "
        "dimension, specified in um.",
    )
    pixel_opt_parser.add_argument(
        "-z",
        "--z-pixel-um",
        dest="z_pixel_um",
        type=check_positive_float,
        help="Pixel spacing of the data in the third "
        "dimension, specified in um.",
    )
    return parser


def geometry_parser(parser):
    geometry_opt_parser = parser.add_argument_group(
        "Options to define size/shape/orientation of data"
    )
    geometry_opt_parser.add_argument(
        "--orientation",
        type=str,
        choices=("coronal", "sagittal", "horizontal"),
        default="coronal",
        help="The orientation of the sample brain. "
        "This is used to transpose the atlas "
        "into the same orientation as the brain.",
    )

    # Warning: atlas reference
    geometry_opt_parser.add_argument(
        "--flip-x",
        dest="flip_x",
        action="store_true",
        help="If the supplied data does not match the NifTI standard "
        "orientation (origin is the most ventral, posterior, left voxel),"
        "then the atlas will be flipped to match the input data",
    )
    geometry_opt_parser.add_argument(
        "--flip-y",
        dest="flip_y",
        action="store_true",
        help="If the supplied data does not match the NifTI standard "
        "orientation (origin is the most ventral, posterior, left voxel),"
        "then the atlas will be flipped to match the input data",
    )
    geometry_opt_parser.add_argument(
        "--flip-z",
        dest="flip_z",
        action="store_true",
        help="If the supplied data does not match the NifTI standard "
        "orientation (origin is the most ventral, posterior, left voxel),"
        "then the atlas will be flipped to match the input data",
    )

    geometry_opt_parser.add_argument(
        "--rotation",
        dest="rotation",
        default="x0y0z0",
        help="How to rotate the atlas to match the raw data. In the format "
        "'xIyJzK', where x, y & z are the axes to rotate around, and "
        "I, J & K are the number of 90 degree rotations for the "
        "respective axes.",
    )

    return parser


def visualisation_parser(parser):
    vis_parser = parser.add_argument_group(
        "Options relating to registration visualisation"
    )

    vis_parser.add_argument(
        "--no-boundaries",
        dest="no_boundaries",
        action="store_true",
        help="Do not precompute the outline images (if you don't want to"
        " use amap_vis",
    )
    return parser


def registration_parse(parser):
    registration_opt_parser = parser.add_argument_group("Registration options")
    registration_opt_parser.add_argument(
        "--registration-config",
        dest="registration_config",
        type=str,
        default=source_files.source_custom_config_amap(),
        help="To supply your own, custom registration configuration file.",
    )
    registration_opt_parser.add_argument(
        "--sort-input-file",
        dest="sort_input_file",
        action="store_true",
        help="If set to true, the input text file will be sorted using "
        "natural sorting. This means that the file paths will be "
        "sorted as would be expected by a human and "
        "not purely alphabetically",
    )

    registration_opt_parser.add_argument(
        "--no-save-downsampled",
        dest="no_save_downsampled",
        action="store_true",
        help="Dont save the downsampled brain before filtering.",
    )

    registration_opt_parser.add_argument(
        "--affine-n-steps",
        dest="affine_n_steps",
        type=check_positive_int,
        default=6,
        help="Registration starts with further downsampled versions of the "
        "original data to optimize the global fit of the result and "
        "prevent 'getting stuck' in local minima of the similarity "
        "function. This parameter determines how many downsampling "
        "steps are being performed, with each step halving the data "
        "size along each dimension.",
    )
    registration_opt_parser.add_argument(
        "--affine-use-n-steps",
        dest="affine_use_n_steps",
        type=check_positive_int,
        default=5,
        help=" Determines how many of the downsampling steps defined by "
        "-affine-n-steps will have their registration computed. "
        "The combination --affine-n-steps 3 --affine-use-n-steps 2 "
        "will e.g. calculate 3 downsampled steps, each of which is "
        "half the size of the previous one but only perform the "
        "registration on the 2 smallest resampling steps, skipping the "
        "full resolution data. Can be used to save time if running the "
        "full resolution doesn't result in noticeable improvements.",
    )
    registration_opt_parser.add_argument(
        "--freeform-n-steps",
        dest="freeform_n_steps",
        type=check_positive_int,
        default=6,
        help=" Registration starts with further downsampled versions of the "
        "original data to optimize the global fit of the result and "
        "prevent 'getting stuck' in local minima of the similarity "
        "function. This parameter determines how many downsampling "
        "steps are being performed, with each step halving the data "
        "size along each dimension.",
    )
    registration_opt_parser.add_argument(
        "--freeform-use-n-steps",
        dest="freeform_use_n_steps",
        type=check_positive_int,
        default=4,
        help="Determines how many of the downsampling steps defined by "
        "--freeform-n-steps will have their registration computed. "
        "The combination --freeform-n-steps 3 --freeform-use-n-steps "
        "2 will e.g. calculate 3 downsampled steps, each of which is "
        "half the size of the previous one but only perform the "
        "registration on the 2 smallest resampling steps, skipping the "
        "full resolution data. Can be used to save time if running the "
        "full resolution doesn't result in noticeable improvements.",
    )
    registration_opt_parser.add_argument(
        "--bending-energy-weight",
        dest="bending_energy_weight",
        type=check_positive_float,
        default=0.95,
        help="Sets the bending energy, which is the coefficient of the "
        "penalty term, preventing the freeform registration from "
        "over-fitting. The range is between 0 and 1 (exclusive) "
        "with higher values leading to more restriction of the "
        "registration.",
    )
    registration_opt_parser.add_argument(
        "--grid-spacing",
        dest="grid_spacing",
        type=int,
        default=-10,
        help="Sets the control point grid spacing in x, y & z. Positive "
        "values are interpreted as real values in mm, negative values "
        "are interpreted as the (positive) distances in voxels. Smaller "
        "grid spacing allows for more local deformations but increases "
        "the risk of over-fitting.",
    )
    registration_opt_parser.add_argument(
        "--smoothing-sigma-reference",
        dest="smoothing_sigma_reference",
        type=float,
        default=-1.0,
        help="Adds a Gaussian smoothing to the reference (the one being "
        "registered to) image, with the sigma defined by the number. "
        "Positive values are interpreted as real values in mm, "
        "negative values are interpreted as distance in voxels.",
    )
    registration_opt_parser.add_argument(
        "--smoothing-sigma-floating",
        dest="smoothing_sigma_floating",
        type=float,
        default=-1.0,
        help="Adds a Gaussian smoothing to the floating image (the one being "
        "registered), with the sigma defined by the number. Positive "
        "values are interpreted as real values in mm, negative values "
        "are interpreted as distance in voxels.",
    )
    registration_opt_parser.add_argument(
        "--histogram-n-bins-floating",
        dest="histogram_n_bins_floating",
        type=check_positive_int,
        default=128,
        help="Number of bins used for the generation of the histograms used "
        "for the calculation of Normalized Mutual Information on "
        "the floating image.",
    )
    registration_opt_parser.add_argument(
        "--histogram-n-bins-reference",
        dest="histogram_n_bins_reference",
        type=check_positive_int,
        default=128,
        help="Number of bins used for the generation of the histograms used "
        "for the calculation of Normalized Mutual Information on the "
        "reference image",
    )
    return parser


def check_atlas_install(cfg_file_path=None):
    """
    Checks whether the atlas directory exists, and whether it's empty or not.
    :return: Whether the directory exists, and whether the files also exist
    """
    dir_exists = False
    files_exist = False
    if cfg_file_path is None:
        cfg_file_path = source_files.source_custom_config_amap()
    else:
        pass
    if os.path.exists(cfg_file_path):
        config_obj = get_config_obj(cfg_file_path)
        atlas_conf = config_obj["atlas"]
        atlas_directory = atlas_conf["base_folder"]
        if os.path.exists(atlas_directory):
            dir_exists = True
            if not os.listdir(atlas_directory) == []:
                files_exist = True

    return dir_exists, files_exist


def copy_registration_config(registration_config, output_directory):
    destination = Path(output_directory, "config.conf")
    copyfile(registration_config, destination)


def prep_registration(args):
    """ If an atlas is not available, download it.
    """
    logging.info("Checking whether the atlas exists")
    _, atlas_files_exist = check_atlas_install(args.registration_config)

    if not atlas_files_exist:
        logging.warning("Atlas does not exist, downloading.")
        atlas_download(args.atlas, args.install_path, args.download_path)
        amend_cfg(
            new_atlas_folder=args.install_path, atlas=args.atlas,
        )

    logging.debug("Making registration directory")
    ensure_directory_exists(args.registration_output_folder)

    logging.debug("Copying registration config to output directory")
    copy_registration_config(
        args.registration_config, args.registration_output_folder
    )

    additional_images_downsample = {}
    if args.downsample_images:
        for idx, images in enumerate(args.downsample_images):
            name = Path(images).name
            additional_images_downsample[name] = images

    return args, additional_images_downsample


def make_paths_absolute(args):
    args.image_paths = os.path.abspath(args.image_paths)
    args.registration_output_folder = os.path.abspath(
        args.registration_output_folder
    )
    args.registration_config = os.path.abspath(args.registration_config)
    return args


def run():
    start_time = datetime.now()
    args = register_cli_parser().parse_args()
    args = define_pixel_sizes(args)

    args, additional_images_downsample = prep_registration(args)
    args = make_paths_absolute(args)

    fancylog.start_logging(
        args.registration_output_folder,
        program_for_log,
        variables=[args],
        verbose=args.debug,
        log_header="AMAP LOG",
        multiprocessing_aware=False,
    )

    logging.info("Starting registration")
    register(
        args.registration_config,
        args.image_paths,
        args.registration_output_folder,
        x_pixel_um=args.x_pixel_um,
        y_pixel_um=args.y_pixel_um,
        z_pixel_um=args.z_pixel_um,
        orientation=args.orientation,
        flip_x=args.flip_x,
        flip_y=args.flip_y,
        flip_z=args.flip_z,
        rotation=args.rotation,
        affine_n_steps=args.affine_n_steps,
        affine_use_n_steps=args.affine_use_n_steps,
        freeform_n_steps=args.freeform_n_steps,
        freeform_use_n_steps=args.freeform_use_n_steps,
        bending_energy_weight=args.bending_energy_weight,
        grid_spacing=args.grid_spacing,
        smoothing_sigma_reference=args.smoothing_sigma_reference,
        smoothing_sigma_floating=args.smoothing_sigma_floating,
        histogram_n_bins_floating=args.histogram_n_bins_floating,
        histogram_n_bins_reference=args.histogram_n_bins_reference,
        sort_input_file=args.sort_input_file,
        n_free_cpus=args.n_free_cpus,
        save_downsampled=not (args.no_save_downsampled),
        boundaries=not (args.no_boundaries),
        additional_images_downsample=additional_images_downsample,
        debug=args.debug,
    )

    logging.info("Finished. Total time taken: %s", datetime.now() - start_time)


def gui():
    from gooey import Gooey

    @Gooey(
        program_name="amap",
        default_size=(1000, 1000),
        required_cols=1,
        optional_cols=3,
    )
    def run_gui():
        run()

    run_gui()


def main():
    run()


if __name__ == "__main__":
    run()
