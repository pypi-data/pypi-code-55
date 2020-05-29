import os
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector, FactorVector
from rpy2.rinterface import StrSexpVector
from rpy2.robjects import pandas2ri, RS4
import pandas as pd
import tarfile, gzip, shutil
from ExpressionTools.pyEset import PyEset
pandas2ri.activate()

start_dir = os.getcwd()
# if os.path.isdir(os.getcwd()+"/r_data"):
#     os.chdir(os.getcwd()+"/r_data")
# else:
#     os.makedirs(os.getcwd()+"/r_data")
#     os.chdir(os.getcwd() + "/r_data")

# if os.path.isfile('prime.Rda'):
session = importr('session')
# session.restore_session(file='prime.Rda')
# session = importr('session')
base = importr('base')
utils = importr('utils')
stats = importr('stats')
data_table = importr('data.table')
oligo_classes = importr('oligoClasses')
affycoretools = importr('affycoretools')
oligo = importr('oligo')
geoquery = importr('GEOquery')
lumi = importr('lumi')

biobase = importr('Biobase')
pd_hugene_21_st = importr('pd.hugene.2.1.st')
# else:
#     base = importr('base')
#     utils = importr('utils')
#     stats = importr('stats')
#     data_table = importr('data.table')
#     oligo_classes = importr('oligoClasses')
#     affycoretools = importr('affycoretools')
#     oligo = importr('oligo')
#     geoquery = importr('GEOquery')
#     lumi = importr('lumi')
#     biobase = importr('Biobase')
#     pd_hugene_21_st = importr('pd.hugene.2.1.st')
#     r_pkgs = ['base', 'utils', 'stats', 'data.table',
#               'affy', 'affycoretools', 'oligo', 'GEOquery',
#               'lumi', 'limma', 'Biobase', 'pd.hugene.2.1.st']
#     [r.assign(pkg, pkg) for pkg in r_pkgs]
#     session = importr('session')
    # session.save_session(file='prime.Rda')
importr('RSQLite')
importr('DBI')
os.chdir(start_dir)


class ExPrep:
    # TODO: add feature to load from feather
    def __init__(self):
        pass

    def load_file(self):
        pass

    def preprocess(self):
        pass


class GeoPrep(ExPrep):
    # TODO: parseGEO function for already downloaded data
    #   search for prospective file name and try to open it, if an error/not existing then download
    def __init__(self, ID, save_dir):
        super().__init__()
        self.ID = ID
        self.input_save = save_dir
        self.eset = None

    def load_geo(self, gse_matrix=True):
        data = geoquery.getGEO(self.ID, GSEMatrix=gse_matrix, destdir=self.input_save, AnnotGPL=True)
        if isinstance(data, RS4):
            self.eset = PyEset(data)

        else:
            self.eset = PyEset(data[0])

    @classmethod
    def box_qc(cls, ):
        pass

    @classmethod
    def density_qc(cls):
        pass

    @classmethod
    def histogram_qc(cls):
        pass


class IlluminaPrep(GeoPrep):
    # https://www.rdocumentation.org/packages/lumi/versions/2.24.0

    def __init__(self, ID, save_dir):
        super().__init__(ID, save_dir)
        self.raw_data = None
        self.eset = None

    def load_geo(self):
        pass

    def load_file(self, filename):
        in_path = os.path.join(self.input_save, filename)
        self.raw_data = lumi.lumiR(in_path, QC=True)
        return self.raw_data

    def preprocess(self):
        self.eset = PyEset(lumi.lumiExpresso(self.raw_data))
        return self.eset


class AffyPrep(GeoPrep):

    def __init__(self, ID, save_dir):
        super().__init__(ID, save_dir)
        self.raw_data = None
        self.eset

    def load_geo(self):
        tar_path = os.path.join(os.path.join(self.input_save, '{}_RAW'.format(self.ID)))
        if not os.path.isdir(os.path.join(self.input_save, '{}_RAW'.format(self.ID))):
            if os.path.isfile(os.path.join(self.input_save, '{}_RAW.tar'.format(self.ID))):
                pass
            else:
                geoquery.getGEOSuppFiles(self.ID, baseDir=self.input_save, makeDirectory=False)
            tarfile.open(name=os.path.join(self.input_save, '{}_RAW.tar'.format(self.ID)),
                         mode="r:*").extractall(path=tar_path)
            # for affy_file in os.scandir(tar_path):
            #     with gzip.open(affy_file.path, 'rb') as f_in:
            #         with open(affy_file.path.split('.gz')[0], 'wb') as f_out:
            #             shutil.copyfileobj(f_in, f_out)
        affy_files = oligo_classes.list_celfiles(tar_path, listGzipped=True)
        cel_files = [str(tar_path) + "/" + str(affy_file) for affy_file in affy_files]
        sv = StrVector(cel_files)
        print(type(sv[0]))
        data = oligo.read_celfiles(filenames=sv)

        self.raw_data = data

    def load_metadata(self):
        metadata = geoquery.getGEO(self.ID, GSEMatrix=True, destdir=self.input_save, AnnotGPL=True)
        self.eset.pheno_data = metadata.do_slot('phenoData').do_slot('data')
        self.eset.feature_data = metadata.do_slot('featureData').do_slot('data')

    def preprocess(self):
        self.eset = PyEset(oligo.rma(self.raw_data))
