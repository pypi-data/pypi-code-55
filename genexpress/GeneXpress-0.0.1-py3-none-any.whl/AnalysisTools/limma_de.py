from ExpressionTools import pyEset, pyXset
from rpy2.robjects.packages import importr
from pandas import DataFrame

r_base = importr('base')
limma = importr('limma')
stats = importr('stats')


class LimmaDiffEx:
    # https://www.bioconductor.org/help/course-materials/2009/BioC2009/labs/limma/limma.pdf
    def __init__(self, data, model: DataFrame = None):
        if isinstance(data, pyEset.PyEset):
            self.data = data.exprs
            self.model = data.groups.astype(int)
        elif issubclass(type(data), pyXset.Xset):
            self.data = data.exprs.to_numpy()
            self.model = data.groups.astype(int).T
        else:
            # some stuff to convert normalized counts and a model into a l
            self.data = data
            self.model = model.T
        # self.model_mat = self.make_model_matrix()
        self.lm = self.run_lmfit()
        self.contrasts = None
        self.contrast_fit = None
        self.ebayes = None

    def run_lmfit(self):
        return limma.lmFit(self.data, self.model)

    def run_ebayes(self):
        self.ebayes = limma.ebayes(self.contrast_fit)
        return self.ebayes

    def make_contrasts(self, experimental: list, control: str, comps=None):
        if comps is None:
            self.contrasts = limma.makeContrasts(*[experiment + "-" + control for experiment in experimental], levels=self.model)
            return self.contrasts
        else:
            self.contrasts = limma.makeContrasts(comps, levels=self.model)
            return self.contrasts

    def run_contrast_fit(self):
        if self.contrasts is None:
            return None
        return limma.contrasts_fit(self.lm, self.contrasts)

    def run_toptable(self, sort_by, n=None, coef=1):
        if n is None:
            n = len(self.data.index)
        tops = limma.topTable(self.ebayes, adjust='fdr', sort_by=sort_by, n=n, coef=coef)
        return tops
    # def make_model_matrix(self, intercept=True):
    #     if intercept:
    #         mat = stats.model_matrix(self.model.to_array())
    #     else:
    #         mat = stats.model_matrix(self.model.to_array())
    #     colnames = r("`colnames<-`")
    #     mat = colnames(mat, StrVector(self.model.columns.to_array()))
    #     return mat