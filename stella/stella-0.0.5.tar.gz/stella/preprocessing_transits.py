import numpy as np
from tqdm import tqdm
from astropy impot units as u
from astropy.table import Table

from .utils import break_rest

__all__ =['TransitDataSet']


class TransitDataSet(object):
    """
    Given a directory of files, reformat data to
    create a training set for the convolutional
    neural network.
    Files must be in '.npy' file format and contain
    at minimum the following indices:
         - 0th index = array of time
         - 1st index = array of flux
         - 2nd index = array of flux errors
    All other indices in the files are ignored.
    This class requires light curves and a catalog
    of transits, taken from the ExoFOP website.
    This class will be passed into the stella.neural_network()
    class to create and train the neural network.
    """
    
    def __init__(self, fn_dir, catalog, cadences=200, frac_balance=0.73,
                 training=0.80, validation=0.90):
        """
        Loads in time, flux, flux error data. Reshapes
        arrays into `cadences`-sized bins and labels
        transits vs. non-transits using the input catalog.

        Parameters
        ----------
        fn_dir : str
             The path to where the files for the training
             set are stored.
        catalog : str
             The path and filename of the catalog with
             marked flare start times.
        cadences : int, optional
             The size of each training set. Default is 200.
        frac_balance : float, optional
             The amount of the negative class to remove.
             Default is 0.75.
        training : float, optional
             Assigns the percentage of training set data for the
             model. Default is 80%
        validation : float, optionl
             Assigns the percentage of validation and testing set
             data for the model. Default is 90%.
        """

        self.fn_dir   = fn_dir
        self.catalog  = Table.read(catalog, format='ascii')
        self.cadences = cadences

        self.frac_balance = frac_balance
        self.load_files()

    def load_files(self):
        """
        Loads light curve files for TOIs. Files follow the 
        npy file naming of '{0}_sector{1}.npy'.format(tic, sector).
        
        Attributes
        ----------
        tics : np.array
             Array of TIC IDs.
        time : np.ndarray
             Array of times for each TIC.
        flux : np.ndarray
             Array of fluxes for each TIC.
        err : np.ndarray
             Array of flux errors for each TIC.
        quality : np.ndarray
             Array of quality flags for each TIC.
        sectors : np.array
             Array of sectors for each loaded light curve.
        """
        files = os.listdir(self.fn_dir)

        files = np.sort([i for i in files if i.endswith('.npy')])

        tics, time, flux, err, quality, sectors = [], [], [], [], [], []

        for fn in tqdm(files):
            data = np.load(os.path.join(self.fn_dir, fn))
            split_fn = fn.split('-')
            tics.append(int(split_fn[2]))
            sectors.append(int(split_fn[1].split('s')[1]))
            time.append(data[0])
            flux.append(data[1])
            err.append( data[2])
            quality.append(data[3])
            
        self.ids      = np.array(tics)
        self.time     = np.array(time)    # in TBJD  
        self.flux     = np.array(flux)
        self.flux_err = np.array(err)
        self.quality  = np.array(quality) 
        self.secotrs  = np.array(sectors)
