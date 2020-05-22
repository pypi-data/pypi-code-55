import argparse
import os
from os.path import abspath, basename, dirname, isfile, splitext
from time import sleep
import warnings

import numpy as np
import pyconrad

try:
    import procbridge
except Exception:
    pass


_ = pyconrad.ClassGetter()


def start_pyconrad(*args, **kwargs):
    pyconrad.setup_pyconrad()
    pyconrad.start_reconstruction_pipeline_gui()


def start_conrad_imagej(*args, **kwargs):

    parser = argparse.ArgumentParser(
        'Starts an instance of ImageJ with CONRAD\'s extensions')
    parser.add_argument('filenames', nargs='*', help='Files to open')
    parser.add_argument('--single-instance-mode', action='store_true',
                        help='Experimental single instance mode. Causes JVM to crash on some machines')
    parser.add_argument('--max_memory', type=int, default=8,
                        help='Maximum memory for Java heap space in gigabytes')
    args = parser.parse_args()

    if not args.single_instance_mode:

        import pyconrad
        pyconrad.setup_pyconrad(max_ram=f'{args.max_memory:d}G')
        pyconrad.start_gui()

        # def request_handler(api, args):
        # for f in args['filenames']:
        for f in args.filenames:
            try:
                filename = basename(f)
                if isfile(f):
                    f = abspath(f)
                    if str.lower(f).endswith('.vtk') or str.lower(f).endswith('.vti'):
                        _.NumericGrid.from_vtk(f).show(filename)
                    elif str.lower(f).endswith('.vdb'):
                        import volume2mesh
                        grids, spacings, origins = volume2mesh.read_vdb(f, return_spacing_origin=True)
                        for name, grid in grids.items():
                            if grid.ndim == 4:
                                grid = np.linalg.norm(grid, axis=3)
                                name += ' (Magnitude)'
                            pyconrad.imshow(grid, name, spacing=spacings[name], origin=origins[name])
                    elif str.lower(f).endswith('.nii'):
                        try:
                            import nibabel
                            dataset = nibabel.load(f)
                            pyconrad.imshow(dataset.get_data(), filename)
                        except ImportError:
                            warnings.warn("Install nibabel")

                    elif str.lower(f).endswith('.npy'):
                        numpy_array = np.load(f)
                        _.NumericGrid.from_numpy(numpy_array).show(filename)
                    elif str.lower(f).endswith('.np') or str.lower(f).endswith('.npz'):
                        file_object = np.load(f)
                        for key in file_object.keys():
                            numpy_array = file_object[key]
                            _.NumericGrid.from_numpy(numpy_array).show(key)
                    else:
                        try:
                            import pydicom
                            _base, ext = splitext(f)
                            if ext.lower() in ['.dcm', '.ima']:
                                dc = pydicom.read_file(f)
                                if dc.SliceThickness:
                                    import pyconrad.dicom_utils
                                    #
                                    vol, spacing, origin, _orientation = pyconrad.dicom_utils.dicomdir2vol(
                                        dirname(f), str(dc.ImageType))
                                    pyconrad.imshow(vol, str(dc.ImageType)
                                                    .replace('[', '')
                                                    .replace(']', '')
                                                    .replace("'", '') + ' – ' + basename(f),
                                                    spacing=spacing,
                                                    origin=origin)
                                return
                        except Exception:
                            pass

                        pyconrad.ij().IJ.openImage(f).show(basename(f))

            except Exception as e:
                print(e)
    else:

        host = '127.0.0.1'
        port = 8077

        try:
            client = procbridge.procbridge.ProcBridge(host, port)
            args.filenames = [os.path.abspath(f) for f in args.filenames]

            client.request('open', {'filenames': args.filenames})
            print('conrad_imagej already running. Delegating opening of files')
            exit(0)
        except ConnectionRefusedError:
            # conrad_imagej not started yet
            pass
        except Exception as e:
            print(e)

        pyconrad.setup_pyconrad(max_ram=f'{args.max_memory:d}G')
        pyconrad.start_gui()

        def request_handler(api, args):
            for f in args['filenames']:
                try:
                    filename = basename(f)
                    if isfile(f):
                        f = abspath(f)
                        if str.lower(f).endswith('.vtk') or str.lower(f).endswith('.vti'):
                            _.NumericGrid.from_vtk(f).show(filename)
                        elif str.lower(f).endswith('.npy'):
                            numpy_array = np.load(f)
                            _.NumericGrid.from_numpy(
                                numpy_array).show(filename)
                        elif str.lower(f).endswith('.np') or str.lower(f).endswith('.npz'):
                            file_object = np.load(f)
                            for key in file_object.keys():
                                numpy_array = file_object[key]
                                _.NumericGrid.from_numpy(numpy_array).show(key)

                        else:
                            pyconrad.ij().IJ.openImage(
                                f).show(basename(f))

                except Exception as e:
                    print(e)

        request_handler('open', {'filenames': args.filenames})

        server = procbridge.procbridge.ProcBridgeServer(
            host, port, request_handler)
        server.start()


if __name__ == "__main__":
    start_pyconrad()
