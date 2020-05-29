import os
from rpy2 import robjects as ro
# from rpy2 import rinterface as ri
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.methods import RS4

pandas2ri.activate()
# numpy2ri.activate()

start_dir = os.getcwd()
# if os.path.isdir(os.getcwd()+"/r_data"):
#     os.chdir(os.getcwd()+"/r_data")
# else:
#     os.makedirs(os.getcwd()+"/r_data")
#     os.chdir(os.getcwd() + "/r_data")
# os.chdir(os.getcwd()+"/r_data")
data_table = importr('data.table')
if os.path.isfile('pyeset.Rda'):
    session = importr('session')
    # session.restore_session(file='pyeset.Rda')
    # session = importr('session')
    methods = importr('methods')
    # matrix = importr('Matrix')
    devices = importr('grDevices')
    base = importr('base')
    ballgown = importr('ballgown')
    biobase = importr('Biobase')
    r.assign('Biobase', 'Biobase')

else:
    methods = importr('methods')
    devices = importr('grDevices')
    base = importr('base')
    ballgown = importr('ballgown')
    biobase = importr('Biobase')
    r_pkgs = ['base', 'methods', 'grDevices', 'Biobase']
    [r.assign(pkg, pkg) for pkg in r_pkgs]
    session = importr('session')
    # session.save_session(file='pyeset.Rda')
os.chdir(start_dir)


class PyEset:

    def __init__(self, eset):
        import ExpressionTools.pyXset as pyXset
        if isinstance(eset, RS4):
            self.ExpressionSet = eset
            # # self.protocol_data = self.protocol_data
            # self.feature_data = eset.do_slot('featureData').do_slot('data')
            # self.pheno_data = eset.do_slot('phenoData').do_slot('data')
            #
            # # self.protocol_data = self.protocol_data
            # self.annot = eset.do_slot('annotation')
            # self.experiment_data = eset.do_slot('experimentData').do_slot('data')

        elif isinstance(eset, pyXset.PyXset):
            self.ExpressionSet = self._eset_from_xset(eset)

    def __eq__(self, other):
        if not isinstance(other, PyEset):
            return NotImplementedError
        else:
            return self.exprs.equals(other.exprs) and\
                   self.feature_data.equals(other.feature_data) and\
                   self.pheno_data.equals(other.pheno_data)

    def _eset_from_xset(self, xset):
        pdata = xset.pdata.append(xset.groups).T
        eset = biobase.ExpressionSet(
                assayData=xset.exprs.to_numpy(),
                phenoData=pdata,
                featureData=xset.fdata,
                experimentData=biobase.MIAME(xset.experiment_data),
                protocolData=xset.protocol_data,
                annotation=ro.StrVector(xset.annotation)
            )
        return eset

    @property
    def exprs(self):
        return biobase.exprs(self.ExpressionSet)

    @exprs.setter
    def exprs(self, array):
        exprs_set = r('`exprs<-`')
        mat = r.matrix(array, nrow=array.shape[0], ncol=array.shape[1])
        exprs_set(self.ExpressionSet, mat)
        # biobase.exprs<-(self.ExpressionSet, mat)
        # biobase.exprs(self.ExpressionSet) = mat

    @property
    def feature_names(self):
        return biobase.featureNames(self.ExpressionSet)

    @feature_names.setter
    def feature_names(self, array):
        fnames_setter = r("`featureNames<-`")
        new_eset = fnames_setter(self.ExpressionSet, array)
        self.ExpressionSet = new_eset

    @property
    def assay_data(self):
        return self.ExpressionSet.do_slot('assayData')

    @assay_data.setter
    def assay_data(self, a_data):
        self.ExpressionSet.do_slot_assign(name='assayData', value=a_data)

    @property
    def feature_data(self):
        try:
            return self.ExpressionSet.do_slot('featureData').do_slot('data')
        except ValueError:
            pass
    @feature_data.setter
    def feature_data(self, f_data):

            curr_fdata = self.ExpressionSet.do_slot('featureData')
            curr_fdata.do_slot_assign('data', pandas2ri.py2rpy(f_data))

    @property
    def pheno_data(self):
         return self.ExpressionSet.do_slot('phenoData').do_slot('data')

    @pheno_data.setter
    def pheno_data(self, p_data):
        curr_pdata = self.ExpressionSet.do_slot('phenoData')
        curr_pdata.do_slot_assign('data', pandas2ri.py2rpy(p_data))

    @property
    def protocol_data(self):
        protodata = self.ExpressionSet.do_slot('protocolData')
        return protodata

    @protocol_data.setter
    def protocol_data(self, val):
        self.ExpressionSet.do_slot_assign('protocolData', val)

    @property
    def experiment_data(self):
        return self.ExpressionSet.do_slot('experimentData')

    @experiment_data.setter
    def experiment_data(self, val):
        self.ExpressionSet.do_slot_assign('experimentData', val)

    @property
    def annot(self):
        return self.ExpressionSet.do_slot('annotation')[0]

    @annot.setter
    def annot(self, val):
        self.ExpressionSet.do_slot('annotation')[0] = val
