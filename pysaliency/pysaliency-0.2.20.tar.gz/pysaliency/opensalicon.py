from __future__ import absolute_import, print_function, division, unicode_literals

import os
import tempfile
import zipfile
import tarfile
from pkg_resources import resource_string,  resource_listdir

from boltons.fileutils import mkdir_p
import numpy as np
from scipy.ndimage import zoom

from .utils import TemporaryDirectory, download_and_check, run_matlab_cmd
from .saliency_map_models import SaliencyMapModel
from .external_models import ExternalModelMixin, download_extract_patch


class OpenSALICON(ExternalModelMixin, SaliencyMapModel):
    """OpenSALICON is an open source implementation of the SALICON saliency model

    .. seealso::
        Huang, X., Shen, C., Boix, X., & Zhao, Q. (2015). SALICON: Reducing
        the Semantic Gap in Saliency Prediction by Adapting Deep Neural
        Networks. In Proceedings of the IEEE International Conference on
        Computer Vision (pp. 262-270).

        https://github.com/CLT29/OpenSALICON
    """

    __modelname__ = 'OpenSALICON'

    def __init__(self, location=None, **kwargs):
        self.setup(location)
        super(OpenSALICON, self).__init__(**kwargs)
        import caffe
        prototxt_file = os.path.join(self.location, 'salicon.prototxt').encode('utf8')
        model_file = os.path.join(self.location, 'model_files', 'salicon_osie.caffemodel').encode('utf8')

        self.net = caffe.Net(prototxt_file, model_file, caffe.TEST)

    def _setup(self):
        mkdir_p(self.location)
        download_extract_patch('http://www.cs.pitt.edu/~chris/files/2016/model_files.tgz',
                               'c150041a975e52cf2ff234975a699fd6',
                               self.location,
                               location_in_archive=False,
                               patches=None)
        download_and_check('https://raw.githubusercontent.com/CLT29/OpenSALICON/36d4de26c8a57a4cfa27387df4f64a208a748e46/salicon.prototxt',
                           os.path.join(self.location, 'salicon.prototxt'),
                           'f7df84bd721b33d0c07518e466021037')

    def process_the_image(self, im):
        MEAN_VALUE = np.array([103.939, 116.779, 123.68])   # BGR
        MEAN_VALUE = MEAN_VALUE[:,None, None]
        # put channel dimension first
        im = np.transpose(im, (2,0,1))
        # switch to BGR
        im = im[::-1, :, :]
        # subtract mean
        im = im - MEAN_VALUE
        im = im[None,:]
        im = im / 255 # convert to float precision
        return im

    def _saliency_map(self, stimulus):
        FINE_SCALE = np.array([1,3,1200,1600], dtype=np.float32)
        COARSE_SCALE = np.array([1,3,600,800], dtype=np.float32)
        im = self.process_the_image(stimulus)
        coarse_img = zoom(im,tuple(COARSE_SCALE / np.asarray(im.shape, dtype=np.float32)), np.dtype(np.float32), mode='nearest')
        assert(coarse_img.shape == (1,3,600,800))
        fine_img = zoom(im,tuple(FINE_SCALE / np.asarray(im.shape, dtype=np.float32)), np.dtype(np.float32), mode='nearest')
        assert(fine_img.shape == (1,3,1200,1600))
        self.net.blobs['fine_scale'].data[...] = fine_img
        self.net.blobs['coarse_scale'].data[...] = coarse_img
        self.net.forward()
        sal_map = self.net.blobs['saliency_map_out'].data
        sal_map = sal_map[0,0,:,:]
        sal_map = sal_map - np.amin(sal_map)
        sal_map = sal_map / np.amax(sal_map)
        sal_map = zoom(sal_map,tuple(np.asarray(im.shape[2:], dtype=np.float32) / np.asarray(sal_map.shape,dtype=np.float32)), np.dtype(np.float32), mode='nearest')
        return sal_map


