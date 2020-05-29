import pandas as pd
from ExpressionTools import helpers
import mygene


class Xset:

    def __init__(self, exprs=pd.DataFrame(), g=None):
        self.exprs = exprs
        self.post_data = dict()
        if g is None:
            self.groups = pd.DataFrame(columns=exprs.columns, dtype='bool')
        else:
            self.groups = g

    def __eq__(self, other):
        if not isinstance(other, Xset):
            return NotImplementedError
        else:
            return self.exprs.equals(other.exprs) and self.groups.equals(other.groups)
    @classmethod
    def translate_gene_ids(cls, ids, id_type, translate_to, species='human'):
        # entrezgene ensemble.gene symbol name alias summary refseq unigene uniprot pdb pfam interpro go
        # geneids must be entrez or ensemble
        # http://mygene.info/doc/annotation_service.html
        gene_converter = mygene.MyGeneInfo()
        return gene_converter.querymany(qterms=ids, scopes=id_type, fields=translate_to, species=species,
                                        as_dataframe=True)

    def update_groups(self, df: pd.DataFrame):
        idx = df.index.to_list()
        common = set(idx).intersection(set(self.groups.index.to_list()))
        if common is not None:
            self.groups.drop(common, inplace=True)
        self.groups = self.groups.append(df.astype(bool))

    def get_groups(self, row: list):
        return self.groups.loc[[row], :]

    def subset(self, groups: list = None, name_ext=False):
        if groups is None:
            return None
        exprs_df = self.exprs.loc[:, self.groups.loc[groups[0], :]]
        new_groups = self.groups.loc[:, self.groups.loc[groups[0], :]]
        if len(groups) > 1:
            for i in groups[1:]:
                exprs_df.join(self.groups.loc[i, :], axis=1, how='outer')
                new_groups.join(self.groups.loc[i, :], axis=1, how='outer')
        if name_ext:
            exprs_df.columns = [col + "_{}".format(groups) for col in exprs_df.columns]
        return Xset(exprs=exprs_df, g=new_groups)

    def load_exprs_file(self, filepath):
        self.exprs = pd.read_csv(filepath, index_col=0)
        self.groups = pd.DataFrame(columns=self.exprs.columns, dtype='bool')

    def search_strings(self, search_terms, name, column_names=True):
        if column_names:
            data = self.groups.columns.to_list()
        else:
            data = self.groups.index.to_list()
        search = helpers.search_list_of_strings(search_terms, data)
        found = pd.DataFrame(self.groups.columns.isin(search), index=name, columns=data)
        return found

    def search_numbers(self, upper, lower, name: list, columns=True):
        if columns:
            data = self.groups.columns.to_list()
        else:
            data = self.groups.index.to_list()
        search = helpers.search_num_range(lower, upper, data)
        found = pd.DataFrame(self.groups.columns.isin(search), index=name, columns=data)
        return found


class PyXset(Xset):
    import ExpressionTools.pyEset as pyEset

    def __init__(self, pyeset: pyEset.PyEset):
        super().__init__()
        # dataframe
        if pyeset.feature_data is not None:
            self.fdata = pyeset.feature_data
        else:
            self.fdata = pd.DataFrame(index=pyeset.feature_names)

        # array
        self.feature_names = pyeset.feature_names
        # dataframe
        self.pdata = pyeset.pheno_data.T
        # array
        self.sample_names = self.pdata.columns.to_numpy()
        # dataframe
        self.exprs = pd.DataFrame(data=pyeset.exprs, index=self.feature_names, columns=self.pdata.columns.to_numpy())
        #
        self.annotation = pyeset.annot
        #
        self.protocol_data = pyeset.protocol_data
        #
        self.experiment_data = pyeset.experiment_data
        # dataframe
        self.groups = pd.DataFrame(columns=self.sample_names)

    def __add__(self, other):
        pass

    def subset(self, group_data=False, fdata=False, group="", fd_col="", name_ext=False):
        if group_data and not fdata:
            df = self.exprs.loc[self.groups.loc[:, group], :]
            if name_ext:
                df.columns = [col + "_{}".format(group) for col in df.columns]

        elif fdata and not group_data:
            df = pd.merge([self.exprs, self.fdata.loc[:, fd_col]],
                          left_index=True, right_index=True).set_index(fd_col, inplace=True)

        elif group_data and fdata:
            df = pd.merge([self.exprs, self.fdata.loc[:, fd_col]],
                          left_index=True, right_index=True).set_index(fd_col, inplace=True)
            df = df.loc[self.groups.loc[:, group], :]
            if name_ext:
                df.columns = [col + "_{}".format(group) for col in df.columns]
        else:
            df = None
        return df

    def clean_data(self, cutoff):
        # need to add more here
        # https://peterlangfelder.com/2018/11/25/filtering-and-collapsing-data/
        keepers = ~self.exprs.isnull().any()
        self.exprs = self.exprs.loc[keepers, :]
        self.pdata = self.pdata.loc[keepers, :]
        self.fdata = self.fdata.loc[keepers, :]

    def get_fdata(self, col):
        return self.fdata.loc[self.fdata.loc[:, col], :]

    def search_pdata(self, search_terms: str or list, name: str, pdata_row: str = 'title'):
        if pdata_row not in self.pdata.index:
            return None
        else:
            found = helpers.search_list_of_strings(search_terms, self.pdata.loc[pdata_row, :])
            found.name = name
            return found


