"""
分箱逻辑：
    1、类别型特征
      1）类别数在5个以下，可以直接根据类别来分箱 (binning_categorical)
      2）类别数在5个以上，建议做降基处理，再根据降基后的类别做分箱(binning_categorical)
    2、数值型特征
      1）无顺序型数值特征：
        若特征value的非重复计数在5个以下，可以直接根据非重复计数值来分箱(binning_categorical)
        若特征value的非重复计数在5个以上，建议根据业务解释或者数据分布做自定义分箱(binning_custom)
      2）连续型数值特征：
        可以用卡方分箱或自定义分箱。(binning_continuous, binning_custom)
        PS:一些特征用卡方分可能会报错，建议这些特征改为手动自定义分箱(binning_custom))
    3、其他
      1）缺失率在5%以下，可以先对缺失做填充处理再分箱
      2）缺失率在5%以上，建议将缺失当作一个类别来分箱
      3) 建议将稀疏值（一般为0）单独分为一箱
"""
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
import utils


class Discretizer(object, metaclass=ABCMeta):
    def __init__(self, continuous_flag,
                 spe_value_list, spe_bin_indicator):
        self._spe_value_list = spe_value_list
        self._spe_bin_indicator = spe_bin_indicator
        self._continuous_flag = continuous_flag
        self._bin_df = None
        self._change_bin_num = False

    @property
    def model(self):
        return self._bin_df

    @abstractmethod
    def _fit_core(self, df, col, target):
        pass

    def fit(self, df, col, target=None):
        if self._continuous_flag is None:
            if df[col].dtypes == 'object':
                self._continuous_flag = False
            else:
                self._continuous_flag = True
        if len(self._spe_value_list) >= 1:
            df1 = df.loc[df[col].isin(self._spe_value_list)]
            df2 = df.loc[~df[col].isin(self._spe_value_list)]
            if df1.shape[0] != 0 and self._spe_bin_indicator:
                self._change_bin_num = True
            else:
                self._change_bin_num = False
        else:
            df2 = df.copy()

        # 对于无监督学习，dataframe[bin_range, bin_total]
        # 对于有监督学习，dataframe[bin_range, bin_total,
        #                        bin_good, bin_bad, bin_bad_rate]
        if df2.shape[0] == 0:
            print('no effective data, failure')
            bin_df = None
        else:
            bin_df = self._fit_core(df2, col, target)
        if bin_df is not None:
            if len(self._spe_value_list) >= 1 \
                    and self._spe_bin_indicator is True:
                if target is None:
                    regroup_single = pd.DataFrame()
                    regroup_single['bin_total'] = df1.groupby(col).size()
                    # dataframe [col, bin_total]
                    regroup_single.reset_index(inplace=True)
                else:
                    # dataframe [col, bin_total, bin_good, bin_bad, bin_bad_rate]
                    regroup_single = utils.bin_bad_rate(df1, col, target)
                regroup_single.rename(columns={col: 'bin_range'}, inplace=True)
                bin_df = utils.concat_of_spec_bins(regroup_single, bin_df,
                                                   'bin_range', self._continuous_flag)

            if target is not None:
                bin_df = utils.compute_woe_iv(bin_df, 'bin_good', 'bin_bad', 'bin_total')
                if self._continuous_flag:
                    ks, _ = utils.cal_ks(df, col, target)
                    bin_df['ks'] = ks

            # 在最后两列生成feature_name和bin_no
            bin_df['feature_name'] = col
            if self._change_bin_num:
                bin_df['bin_no'] = np.array(
                    self._spe_value_list + list(range(
                        bin_df.shape[0] - len(self._spe_value_list)))
                ).astype('object')
            else:
                bin_df['bin_no'] = np.arange(bin_df.shape[0], dtype=float)
            # 将最后两列调整到第前面
            bin_df = pd.concat(
                [bin_df[['feature_name', 'bin_no']], bin_df.iloc[:, :-2]], axis=1)

        # 对于无监督学习，dataframe[feature_name, bin_range, bin_total, bin_no]
        # 对于有监督学习，dataframe[feature_name, bin_range, bin_total, bin_good,
        #                        bin_bad, bin_bad_rate, bin_no, bin_woe, iv]
        # index一定是从0开始逐渐增大
        self._bin_df = bin_df

    def transform(self, df, from_col, to_col, test_indicator=False,
                  target=None, fill_na=None, failure_value=0):
        assert self._bin_df is not None
        if fill_na is None and len(self._spe_value_list) != 0:
            fill_na = self._spe_value_list[0]
        if test_indicator:
            mapped_col, bin_df2 = \
                utils.map_to_bin(df, from_col, self._bin_df, to_col,
                                 test_indicator, target, fill_na, failure_value)

            if target is not None and self._continuous_flag:
                ks, _ = utils.cal_ks(df, from_col, target)
                bin_df2['ks'] = ks
            return mapped_col, bin_df2
        else:
            mapped_col = utils.map_to_bin(df, from_col, self._bin_df, to_col,
                                          test_indicator, target, fill_na, failure_value)
            return mapped_col

    def combine_bin_to_next(self, bin_df, index, inplace=False):
        """
        :param bin_df: 对于无监督学习，dataframe[feature_name, bin_range, bin_total, bin_no]
                       对于有监督学习，dataframe[feature_name, bin_range, bin_total, bin_good,
                                              bin_bad, bin_bad_rate, bin_no, bin_woe, iv]
                       bin_no和indices永远是从0开始递增
        :param index: int, rows of index and index+1 of bin_df will be combined
        :param inplace: bool, whether to update the mapping model
        """
        columns = bin_df.columns.tolist()
        # make sure bin_df is [feature_name, bin_range, bin_total] or
        # [feature_name, bin_range, bin_total, bin_good, bin_bad, bin_bad_rate]
        for col_name in ['bin_no', 'bin_woe', 'iv']:
            if col_name in columns:
                bin_df = bin_df.drop(col_name, axis=1)
        bin_df = utils.combine_bin_df(bin_df, 'bin_range', index, self._continuous_flag)
        if self._change_bin_num:
            bin_df['bin_no'] = np.array(
                self._spe_value_list + list(range(
                    bin_df.shape[0] - len(self._spe_value_list)))
            ).astype('object')
        else:
            bin_df['bin_no'] = np.arange(bin_df.shape[0], dtype=float)
        if 'bin_woe' in columns:
            bin_df = utils.compute_woe_iv(bin_df, 'bin_good', 'bin_bad', 'bin_total')
        if inplace:
            self._bin_df = bin_df
        return bin_df


class SimpleEncoder(Discretizer):
    def __init__(self, spe_value_list=[], spe_bin_indicator=False, continuous_flag=False,
                 min_binpct=0.05, monoticity=False, auto_merge=True):
        super(SimpleEncoder, self).__init__(False,
                                            spe_value_list,
                                            spe_bin_indicator)
        self._auto_merge = auto_merge
        self._min_binpct = min_binpct
        self._monoticity = monoticity
        self._continuous_flag = continuous_flag

    def _fit_core(self, df, col, target=None):
        if target is None:
            bin_df = pd.DataFrame()
            bin_df['bin_total'] = df.groupby(col).size()
            bin_df.reset_index(inplace=True)
            # dataframe [col, bin_total]
        else:
            # dataframe [col, bin_total, bin_good, bin_bad, bin_bad_rate]
            # index一定是从0开始逐渐编号
            bin_df = utils.bin_bad_rate(df, col, target)
            bin_df[col] = bin_df[col].apply(lambda x: [x])
            if self._continuous_flag:
                group_interval = bin_df[col].tolist()
                if bin_df.shape[0] == 1:
                    cut_off_points = [max(group_interval[0])]
                    bin_df[col] = [pd.Interval(left=float('-inf'),
                                               right=float(cut_off_points[0]))]
                else:
                    # 取每个区间的最大值, cutoffpoints不含起止点
                    cut_off_points = [max(i) if isinstance(i, list) else i
                                      for i in group_interval[:-1]]
                    bin_df[col] = utils.cutoffpoints_to_interval(cut_off_points)
            else:
                # 对于类别型变量需要按坏账率排序，合并相似坏账率的组
                bin_df.sort_values(by='bin_bad_rate', inplace=True)
                bin_df.reset_index(inplace=True)
            if self._auto_merge:
                bin_df = utils.check_bin(bin_df, col, self._continuous_flag,
                                         self._min_binpct, self._monoticity)
                if bin_df is None:
                    return None
        bin_df.rename(columns={col: 'bin_range'}, inplace=True)
        return bin_df


class CommonNumericalDiscretizer(Discretizer):
    def __init__(self, spe_value_list=[], spe_bin_indicator=False,
                 cut=5, quantile=True, min_binpct=0, monoticity=False,
                 auto_merge=True):
        super(CommonNumericalDiscretizer, self).__init__(True,
                                                         spe_value_list,
                                                         spe_bin_indicator)
        self._auto_merge = auto_merge
        self._min_binpct = min_binpct
        self._monoticity = monoticity
        self._quantile = quantile
        if len(spe_value_list) >= 1 and spe_bin_indicator is True:
            self._cut = cut - len(spe_value_list)
        else:
            self._cut = cut

    def _fit_core(self, df, col, target=None):
        if self._quantile:
            bucket = pd.qcut(df[col], self._cut, duplicates='drop')
        else:
            bucket = pd.cut(df[col], self._cut)
        if target is None:
            bin_df = pd.DataFrame()
            bin_df['bin_total'] = df.groupby(bucket.rename('bin_range')).size()
            # dataframe [bin_range, bin_total]
            # index一定是从0开始逐渐编号
            bin_df.reset_index(inplace=True)
        else:
            # dataframe [bin_range, bin_total, bin_good, bin_bad, bin_bad_rate]
            # index一定是从0开始逐渐编号
            bin_df = utils.bin_bad_rate(df, bucket.rename('bin_range'), target)
            if self._auto_merge:
                bin_df = utils.check_bin(bin_df, 'bin_range', True,
                                         self._min_binpct, self._monoticity)
                if bin_df is None:
                    return None
        bin_df = utils.map_to_inf(bin_df, 'bin_range')
        return bin_df


class CommonCategoricalDiscretizer(Discretizer):
    def __init__(self, spe_value_list=[], spe_bin_indicator=False, monoticity=False,
                 cut=5, quantile=True, min_binpct=0, auto_merge=True):
        super(CommonCategoricalDiscretizer, self).__init__(False,
                                                           spe_value_list,
                                                           spe_bin_indicator)
        self._auto_merge = auto_merge
        self._min_binpct = min_binpct
        self._quantile = quantile
        self._monoticity = monoticity
        if len(spe_value_list) >= 1 and spe_bin_indicator is True:
            self._cut = cut - len(spe_value_list)
        else:
            self._cut = cut

    def _fit_core(self, df, col, target=None):
        # 类别型变量往往取值极其不平衡，而且样本数目远远大于类别数目
        # 如果在原始数据上直接取等频分位点的话，会出现大量重复的分割点，
        # 这样也不能等频划分为你想要的区间数目。
        # 因此，如果对类别取值去重，然后取分位点。这样处理的后果是：
        # 1. 等宽划分，完全不受去重的影响，因为等宽分位点是按取值的大小进行的
        # 2. 等频分位点是按序列的index取的，因此去重后的index是不一样的，
        #    划分的区间映射回原始数据集，各个区间的样本个数也是不同的
        #    最后的结果和等宽划分差别并不大
        if target is None:
            map_dict = df.groupby(col)[col].count().to_dict()
            df.loc[:, 'proxy'] = df[col].map(map_dict)
        else:
            regroup = utils.bin_bad_rate(df, col, target)
            map_dict = regroup.set_index(col)['bin_bad_rate'].to_dict()
            df.loc[:, 'proxy'] = df[col].map(map_dict)
        if not self._quantile:
            bucket = pd.cut(df['proxy'], self._cut)
        else:
            bucket = pd.qcut(df['proxy'], self._cut, duplicates='drop')
        # iterable of arrays
        indices_list = df.groupby(bucket).indices.values()
        bin_df = pd.DataFrame()
        # 在未排序的dataframe中，按照indices来取数,
        # 由于indices是array，因此得到的一定是series,
        # series.unique()得到的一定是array且tolist()以后一定是list
        # dataframe [bin_range, bin_total]
        col_values = [df.loc[df.index[indices], col].unique().tolist() for indices in indices_list
                      if indices.shape[0] != 0]
        bin_df['bin_range'] = col_values
        col_total = [df.loc[df.index[indices], col].size for indices in indices_list
                     if indices.shape[0] != 0]
        bin_df['bin_total'] = col_total
        if target is not None:
            # dataframe [bin_range, bin_total, bin_good, bin_bad, bin_bad_rate]
            # index一定是从0开始逐渐增大的
            col_bad = [df.loc[df.index[indices], target].sum() for indices in indices_list
                       if indices.shape[0] != 0]
            bin_df['bin_bad'] = col_bad
            bin_df['bin_good'] = bin_df['bin_total'] - bin_df['bin_bad']
            bin_df['bin_bad_rate'] = bin_df['bin_bad'] / bin_df['bin_total']
            if self._auto_merge:
                bin_df = utils.check_bin(bin_df, 'bin_range', False,
                                         self._min_binpct, self._monoticity)
                if bin_df is None:
                    return None
        return bin_df


class Chi2Discretizer(Discretizer):
    def __init__(self, spe_value_list=[], spe_bin_indicator=False,
                 continuous_flag=True, precut=100, prequantile=True,
                 max_bin_num=5, min_binpct=0.0, monoticity=True):
        super(Chi2Discretizer, self).__init__(continuous_flag,
                                              spe_value_list,
                                              spe_bin_indicator)
        self._monoticity = monoticity
        self._precutthreshold = precut
        self._prequantile = prequantile
        self._min_binpct = min_binpct
        self._max_bin_num = max_bin_num

    def _fit_core(self, df, col, target):
        if len(self._spe_value_list) >= 1 and self._spe_bin_indicator is True and self._change_bin_num:
            max_bin_num = self._max_bin_num - len(self._spe_value_list)
        else:
            max_bin_num = self._max_bin_num
        if self._continuous_flag:
            if len(df[col].unique()) > self._precutthreshold:
                # 对于连续型变量，如果唯一值数目过大，
                # 则先做一次等宽或等频分箱，把原col映射到盖帽分割点上（注意不是分箱号)
                split_points = utils.unsupervised_split(df, col, self._precutthreshold, self._prequantile)
                df[col] = df[col].map(lambda x: utils.cutoffpoints_to_edge(x, split_points))
            bin_df = utils.bin_bad_rate(df, col, target)
            bin_df[col] = bin_df[col].apply(lambda x: [x])
        else:
            if len(df[col].unique()) > self._precutthreshold:
                preprocessor = CommonCategoricalDiscretizer(spe_value_list=[],
                                                            spe_bin_indicator=False,
                                                            cut=self._precutthreshold,
                                                            quantile=self._prequantile,
                                                            min_binpct=0,
                                                            monoticity=False,
                                                            auto_merge=False)
                preprocessor.fit(df, col, target)
                # index一定是从0开始逐渐增大
                bin_df = preprocessor.model[['bin_range', 'bin_total', 'bin_bad',
                                             'bin_good', 'bin_bad_rate']].rename(
                    columns={'bin_range': col})
            else:
                bin_df = utils.bin_bad_rate(df, col, target)
                bin_df[col] = bin_df[col].apply(lambda x: [x])
                bin_df.sort_values(by='bin_bad_rate', inplace=True)
                # index一定是从0开始逐渐增大
                bin_df.reset_index(inplace=True, drop=True)

        bin_df = utils.chi2_merge(bin_df, col, max_bin_num,
                                  self._min_binpct, self._monoticity)

        if self._continuous_flag:
            group_interval = bin_df[col].tolist()
            if bin_df.shape[0] == 1:
                cut_off_points = [max(group_interval[0])]
                bin_df[col] = [pd.Interval(left=float('-inf'),
                                           right=float(cut_off_points[0]))]
            else:
                # 取每个区间的最大值, cutoffpoints不含起止点
                cut_off_points = [max(i) if isinstance(i, list) else i
                                  for i in group_interval[:-1]]
                bin_df[col] = utils.cutoffpoints_to_interval(cut_off_points)

        # dataframe [bin_range, bin_total, bin_bad, bin_good, bin_bad_rate]
        bin_df.rename(columns={col: 'bin_range'}, inplace=True)
        return bin_df


class Chi2Discretizer2(Discretizer):
    def __init__(self, bc_iv_lower, bc_iv_upper, spe_value_list=[], spe_bin_indicator=False,
                 continuous_flag=True, max_bin_num=5, min_binpct=0.1, monotonicity=True,
                 auto_merge=True):
        assert continuous_flag is True
        assert 0.05 <= min_binpct < 1
        super(Chi2Discretizer2, self).__init__(continuous_flag,
                                               spe_value_list,
                                               spe_bin_indicator)
        self._monotonicity = monotonicity
        self._bc_iv_lower = bc_iv_lower
        self._bc_iv_upper = bc_iv_upper
        self._min_binpct = min_binpct
        self._max_bin_num = max_bin_num
        self._auto_merge = auto_merge

    def _fit_core(self, df, col, target):
        if len(self._spe_value_list) >= 1 and self._spe_bin_indicator is True and self._change_bin_num:
            max_bin_num = self._max_bin_num - len(self._spe_value_list)
        else:
            max_bin_num = self._max_bin_num
        total = df.shape[0]
        bad = df[target].sum()
        good = total - bad
        bc_good_bad = (good, bad)
        bc_gap = total * self._min_binpct
        df['temp'] = col
        group = df.loc[:, ['temp', col, target]].values.tolist()
        bin_df = utils.best_chisq_bin(group, max_bin_num, bc_good_bad, bc_gap, self._monotonicity,
                                      self._bc_iv_lower, self._bc_iv_upper, self._auto_merge)
        return bin_df


