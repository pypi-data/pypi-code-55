import logging
import numpy as np

from pathlib import Path
from imlib.general.system import get_num_processes, delete_temp
import nibabel as nb
from brainio import brainio


from neuro.atlas_tools.paths import Paths
from amap.register.brain_processor import BrainProcessor
from amap.register.brain_registration import BrainRegistration
from amap.register.volume import calculate_volumes
from amap.config.atlas import RegistrationAtlas
from amap.vis.boundaries import main as calc_boundaries
from amap.register.registration_params import RegistrationParams
from amap.register.tools import save_downsampled_image
from amap.utils.run import Run
from amap.utils.transformations import flip_multiple

flips = {
    "horizontal": (True, True, False),
    "coronal": (True, True, False),
    "sagittal": (False, True, False),
}

transpositions = {
    "horizontal": (1, 0, 2),
    "coronal": (2, 0, 1),
    "sagittal": (2, 1, 0),
}


def check_downsampled(registration_output_folder, name):
    return Path(registration_output_folder, f"downsampled_{name}.nii").exists()


def main(
    registration_config,
    target_brain_path,
    registration_output_folder,
    x_pixel_um=0.02,
    y_pixel_um=0.02,
    z_pixel_um=0.05,
    orientation="coronal",
    flip_x=False,
    flip_y=False,
    flip_z=False,
    rotation="x0y0z0",
    affine_n_steps=6,
    affine_use_n_steps=5,
    freeform_n_steps=6,
    freeform_use_n_steps=4,
    bending_energy_weight=0.95,
    grid_spacing=-10,
    smoothing_sigma_reference=-1.0,
    smoothing_sigma_floating=-1.0,
    histogram_n_bins_floating=128,
    histogram_n_bins_reference=128,
    n_free_cpus=2,
    sort_input_file=False,
    save_downsampled=True,
    additional_images_downsample=None,
    boundaries=True,
    debug=False,
):
    """
        The main function that will perform the library calls and
    register the atlas to the brain given on the CLI

    :param registration_config:
    :param target_brain_path:
    :param registration_output_folder:
    :param filtered_brain_path:
    :param x_pixel_um:
    :param y_pixel_um:
    :param z_pixel_um:
    :param orientation:
    :param flip_x:
    :param flip_y:
    :param flip_z:
    :param n_free_cpus:
    :param sort_input_file:
    :param save_downsampled:
    :param additional_images_downsample: dict of
    {image_name: image_to_be_downsampled}
    :return:
    """
    n_processes = get_num_processes(min_free_cpu_cores=n_free_cpus)
    load_parallel = n_processes > 1
    paths = Paths(registration_output_folder)
    atlas = RegistrationAtlas(
        registration_config, dest_folder=Path(registration_output_folder)
    )
    run = Run(paths, atlas, boundaries=boundaries, debug=debug)

    if run.preprocess:
        logging.info("Preprocessing data for registration")
        logging.info("Loading data")

        brain = BrainProcessor(
            atlas.pix_sizes,
            target_brain_path,
            registration_output_folder,
            x_pixel_um,
            y_pixel_um,
            z_pixel_um,
            original_orientation=orientation,
            load_parallel=load_parallel,
            sort_input_file=sort_input_file,
            n_free_cpus=n_free_cpus,
        )

        for element in ["atlas", "brain", "hemispheres"]:
            key = f"{element}_name"
            nii_img = atlas.get_nii_from_element(key)
            data = np.asanyarray(nii_img.dataobj)

            # reorients the atlas to the orientation of the sample
            data = np.transpose(
                data, transpositions[brain.original_orientation]
            )
            data = np.swapaxes(data, 0, 1)
            # reorients atlas to the nifti (origin is the most ventral, posterior,
            # left voxel) coordinate framework
            data = flip_multiple(data, flips[orientation])

            # flips if the input data doesnt match the nifti standard
            data = flip_multiple(data, [flip_x, flip_y, flip_z])

            ####################
            # axes = (0, 1)
            # k = 3
            # brain.rotate_atlas(axes, k)
            ####################
            new_img = nb.Nifti1Image(data, nii_img.affine, nii_img.header)
            brainio.to_nii(new_img, atlas.get_dest_path(key))

        if save_downsampled:
            brain.target_brain = brain.target_brain.astype(
                np.uint16, copy=False
            )
            logging.info("Saving downsampled image")
            brain.save(paths.downsampled_brain_path)

        brain.filter()
        logging.info("Saving filtered image")
        brain.save(paths.tmp__downsampled_filtered)

        del brain

    if additional_images_downsample:
        for name, image in additional_images_downsample.items():
            if not check_downsampled(registration_output_folder, name):
                save_downsampled_image(
                    image,
                    name,
                    registration_output_folder,
                    atlas,
                    x_pixel_um=x_pixel_um,
                    y_pixel_um=y_pixel_um,
                    z_pixel_um=z_pixel_um,
                    orientation=orientation,
                    n_free_cpus=n_free_cpus,
                    sort_input_file=sort_input_file,
                    load_parallel=load_parallel,
                )
            else:
                logging.info(f"Image: {name} already downsampled, skipping.")

    if run.register:
        logging.info("Registering")

    if any(
        [
            run.affine,
            run.freeform,
            run.segment,
            run.hemispheres,
            run.inverse_transform,
        ]
    ):
        registration_params = RegistrationParams(
            registration_config,
            affine_n_steps=affine_n_steps,
            affine_use_n_steps=affine_use_n_steps,
            freeform_n_steps=freeform_n_steps,
            freeform_use_n_steps=freeform_use_n_steps,
            bending_energy_weight=bending_energy_weight,
            grid_spacing=grid_spacing,
            smoothing_sigma_reference=smoothing_sigma_reference,
            smoothing_sigma_floating=smoothing_sigma_floating,
            histogram_n_bins_floating=histogram_n_bins_floating,
            histogram_n_bins_reference=histogram_n_bins_reference,
        )
        brain_reg = BrainRegistration(
            registration_config,
            paths,
            registration_params,
            n_processes=n_processes,
        )

    if run.affine:
        logging.info("Starting affine registration")
        brain_reg.register_affine()

    if run.freeform:
        logging.info("Starting freeform registration")
        brain_reg.register_freeform()

    if run.segment:
        logging.info("Starting segmentation")
        brain_reg.segment()

    if run.hemispheres:
        logging.info("Segmenting hemispheres")
        brain_reg.register_hemispheres()

    if run.inverse_transform:
        logging.info("Generating inverse (sample to atlas) transforms")
        brain_reg.generate_inverse_transforms()

    if run.volumes:
        logging.info("Calculating volumes of each brain area")
        calculate_volumes(
            paths.registered_atlas_path,
            paths.hemispheres_atlas_path,
            atlas.get_element_path("structures_name"),
            registration_config,
            paths.volume_csv_path,
            left_hemisphere_value=int(atlas["left_hemisphere_value"]),
            right_hemisphere_value=int(atlas["right_hemisphere_value"]),
        )

    if run.boundaries:
        logging.info("Generating boundary image")
        calc_boundaries(
            paths.registered_atlas_path,
            paths.boundaries_file_path,
            atlas_config=registration_config,
        )

    if run.delete_temp:
        logging.info("Removing registration temp files")
        delete_temp(paths.registration_output_folder, paths)

    logging.info(
        f"amap completed. Results can be found here: "
        f"{registration_output_folder}"
    )
