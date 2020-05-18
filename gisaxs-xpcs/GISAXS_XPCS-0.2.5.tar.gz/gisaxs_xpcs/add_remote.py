import os
import logging

import h5py
from tqdm import tqdm
import numpy as np

from .connection import Connection
from .manage_h5_data import h5_manager
from .common_tools import save_create, save_create_dset
from .read_edf import read_edf_gz
from .gisaxs_parameters import GisaxsParameters


class AddRemote(object):

    log = logging.getLogger(__name__)

    def __init__(self, h5file: str = 'data.h5'):
        self.path = h5file
        self._connection = Connection()
        if not os.path.exists(self.path):
            with h5py.File(self.path, 'w'):
                pass
        h5_manager.set_path(h5file)

    @property
    def _sftp(self):
        return self._connection.sftp

    def connect(self, user: str, password: str):
        self._connection.set_auth(username=user, password=password)
        self._connection.connect()
        self._sftp.cwd('..')
        self._sftp.cwd('groupshare/OMBD/xray/beamtimes/2018_ESRF_SC4813_coherence/id10/data')

    def iter_pen_folders(self):
        yield from filter(lambda s: s.startswith('PEN'), self._sftp.listdir())

    def iter_zaptime(self, num: int, copy: bool = False, delta: int = 1):
        zaptime_name = '_'.join(['zaptime', str(num)])
        for pen_folder in self.iter_pen_folders():
            zaptime_names = self._sftp.listdir(pen_folder)
            if zaptime_name in zaptime_names:
                current_path = f'{pen_folder}/{zaptime_name}'
                files = self._sftp.listdir(current_path)
                files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
                if delta > 1:
                    files = [files[i * delta] for i in range(len(files) // delta)]
                for file in tqdm(files):
                    if copy:
                        yield self._connection.save_file(f'{current_path}/{file}')
                    else:
                        yield f'{current_path}/{file}'
        else:
            yield

    def add_folder(self, zaptime_number: int, delta: int = 1, *, save_axes: bool = True,
                   rewrite: bool = False):
        gp = GisaxsParameters.init_from_folder_number(zaptime_number)
        if save_axes:
            x_axis, y_axis = gp.get_angle_vectors(units='deg', flip=False)
        else:
            x_axis = y_axis = None

        with h5py.File(self.path, 'a') as f:
            raw_data_group = save_create(f, 'Raw data')

            current_group_name = '_'.join(['zaptime', str(zaptime_number).zfill(2)])
            if current_group_name in list(raw_data_group.keys()) and not rewrite:
                print('Current folder already exists')
                return

            current_group = save_create(raw_data_group, current_group_name)
            if x_axis is not None and y_axis is not None:
                x_axis_dset = save_create_dset(current_group, 'x_axis', data=x_axis, rewrite=rewrite)
                y_axis_dset = save_create_dset(current_group, 'y_axis', data=y_axis, rewrite=rewrite)
            else:
                x_axis_dset = y_axis_dset = None
            for i, gz_file in enumerate(self.iter_zaptime(zaptime_number, copy=True, delta=delta)):
                if not gz_file:
                    return
                try:
                    data, header_dict = read_edf_gz(gz_file)
                    data = np.flip(data, axis=1)
                    dset = save_create_dset(current_group, str(i).zfill(5), data=data, rewrite=rewrite)
                    dset.attrs.update(header_dict)
                    if x_axis_dset is not None and y_axis_dset is not None:
                        dset.attrs.update({'x_axis': x_axis_dset.ref, 'y_axis': y_axis_dset.ref})
                except Exception as err:
                    self.log.exception(err)
