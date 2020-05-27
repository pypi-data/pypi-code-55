import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools
import datetime
import os


def cutoffpoints_to_interval(cut_off_points):
    """
    一定是连续值才有所谓分割区间
    :param cut_off_points: list, 不含起止点
    :return: list, 以cut_off_points为分割点，下限为-inf,上限为inf的区间列表
    """
    cut_off_points = list(set(cut_off_points))
    cut_off_points.sort()
    group_interval = [pd.Interval(left=float('-inf'),
                                  right=float(cut_off_points[0]))]
    for i in range(len(cut_off_points)-1):
        group_interval.append(pd.Interval(left=float(cut_off_points[i]),
                                          right=float(cut_off_points[i+1])))
    group_interval.append(pd.Interval(left=float(cut_off_points[-1]),
                                      right=float('inf')))
    return group_interval


def cutoffpoints_to_edge(x, cut_off_points):
    """
    :param x: 要映射的点
    :param cut_off_points: list, 不含起止点
    :return: 映射到的点
    """
    num_of_points = len(cut_off_points)
    first_point = min(cut_off_points)
    last_point = max(cut_off_points)
    if x <= first_point:
        return first_point
    elif x > last_point:
        return 10e10
    else:
        for i in range(num_of_points - 1):
            if cut_off_points[i] < x <= cut_off_points[i+1]:
                return cut_off_points[i+1]


def map_to_inf(regroup, col):
    """
    用于将连续型分箱表的col字段取值范围的最小值映射为-inf
    将最大值映射为inf
    :param regroup:分箱表dataframe，index必须是从0开始逐渐编号
    :param col:要调整上下限的字段名string
    :return: dataframe
    """
    regroup.sort_values(col, ascending=True, inplace=True)
    regroup = regroup.astype({col: 'object'})
    # 修改上下限为-inf  inf
    regroup.loc[0, col] = \
        pd.Interval(left=float('-inf'),
                    right=regroup.loc[0, col].right)
    last_index = regroup.shape[0] - 1
    regroup.loc[last_index, col] = pd.Interval(
        left=regroup.loc[last_index, col].left,
        right=float('inf'))
    return regroup


def map_to_bin(df, from_col, bin_df, to_col, test_indicator=False,
               target=None, fill_na=None, failure_value=0):
    """
    将原数据框df的某个列from_col映射为分箱表bin_df的to_col
    :param df: pd.Dataframe, 需要映射的表
    :param from_col: str, 需要映射的df的一个列
    :param bin_df: 用于将from_col的各个取值按bin_range映射为to_col取值的dataframe
                   bin_range列为col连续区间interval或取值list
    :param to_col: str, bin_df的一个列名
    :param test_indicator: bool, if True, a new bin_df will be returned
    :param target: str, 需要映射的df的目标列
    :param fill_na: float, 缺失值填充
    :param failure_value: float, 如果最后无法映射，就按这个值映射
    :return: list, 值为映射到的值
    """
    num_values = df.shape[0]
    num_of_bins = bin_df.shape[0]
    input_series = df[from_col]
    if fill_na is not None:
        input_series = input_series.fillna(fill_na)
    # pandas里面，如果某一列dtype为数值型，则none，np.nan都作为np.nan
    # 但是如果某一列为object类型，则none和np.nan是不一样的
    # 如果map传入的是一个字典，则字典无法涉及的部分会始终映射为np.nan
    mapped_value_list = [failure_value] * num_values
    if test_indicator:
        bin_total_list = [0] * num_of_bins
        bin_bad_list = [0] * num_of_bins
    for i in range(num_values):
        value = input_series.iloc[i]
        for j in range(num_of_bins):
            if value in bin_df['bin_range'].iloc[j]:
                mapped_value_list[i] = bin_df[to_col].iloc[j]
                if test_indicator:
                    bin_total_list[j] += 1
                    if target is not None:
                        bin_bad_list[j] += df[target].iloc[i]
                break
    if test_indicator:
        if target is not None:
            bin_df2 = pd.DataFrame({'bin_range': bin_df['bin_range'],
                                    'bin_total': bin_total_list,
                                    'bin_bad': bin_bad_list},
                                   index=np.arange(num_of_bins))
            bin_df2['bin_good'] = bin_df2['bin_total'] - bin_df2['bin_bad']
            bin_df2['bin_bad_rate'] = bin_df2['bin_bad'] / bin_df2['bin_total']
            bin_df2 = compute_woe_iv(bin_df2, 'bin_good', 'bin_bad', 'bin_total')
        else:
            bin_df2 = pd.DataFrame({'bin_range': bin_df['bin_range'],
                                    'bin_total': bin_total_list},
                                   index=np.arange(num_of_bins))
        # 在最后两列生成feature_name和bin_no
        bin_df2['feature_name'] = from_col
        bin_df2['bin_no'] = bin_df['bin_no']
        # 将最后两列调整到第前面
        bin_df2 = pd.concat(
            [bin_df2[['feature_name', 'bin_no']], bin_df2.iloc[:, :-2]], axis=1)
        return mapped_value_list, bin_df2
    else:
        return mapped_value_list


def unsupervised_split(df, var, num_of_split=5, quantile=True):
    """
    :param df: 数据集
    :param var: 需要分箱的变量, 仅限数值型
    :param num_of_split: 需要分箱个数，默认是5
    :param quantile: bool 默认是等频，否则是等距
    :return: list of split points, 不含首尾点
    """
    if quantile:
        interval_index = int(df.shape[0] / num_of_split)
        split_point_indices = [i * interval_index for i in range(1, num_of_split)]
        raw_values = df[var].sort_values(na_position='first')
        split_points = [raw_values.iloc[i] for i in split_point_indices]
        split_points = sorted(list(set(split_points)))
    else:
        var_max, var_min = max(df[var]), min(df[var])
        interval_value = (var_max - var_min) * 1.0 / num_of_split
        split_points = [var_min + i * interval_value for i in range(1, num_of_split)]
    return split_points


def concat_of_spec_bins(spec_bin_df, bin_df, range_col, continuous_flag):
    """
    将特殊取值对应的分箱（一定是离散型的）和已有分箱表连接起来
    :param spec_bin_df: 特殊取值对应的离散型分箱表dataframe
    :param bin_df: 已有分箱表dataframe
    :param range_col: 要连接并调整的分箱区间的字段名string
    :param continuous_flag: 已有分箱表为连续分箱表还是离散分箱表
                            如果为连续的，则拼接后的表仍然是连续的,
                                range_col字段存储的是col_values连续区间
                                取值为interval类型
                            如果是离散的，则拼接后的表仍然是离散的，
                                range_col字段存储的是col_values的取值list
                                取值为list类型
    :return: 分箱表dataframe
    """
    regroup = bin_df.copy()
    regroup_single = spec_bin_df.copy()
    if not continuous_flag:
        regroup_single[range_col] = regroup_single[range_col].map(lambda x: [x])
    # 对于连续型变量，如果有缺失值需要单独设置，一定要人为设置这个缺失值比所有其他数值都小
    regroup = pd.concat([regroup_single, regroup], sort=False)
    if continuous_flag:
        group_interval = regroup[range_col].tolist()
        # 取每个区间的最大值, cut_off_points不含起止点
        cut_off_points = []
        for i in group_interval[:-1]:
            if isinstance(i, pd.Interval):
                cut_off_points.append(i.right)
            else:
                cut_off_points.append(i)
        # 第一个区间就是(-inf---特殊值], 第二个区间为（特殊值----某个值].....
        regroup[range_col] = cutoffpoints_to_interval(cut_off_points)
    # 重新把index编号调整为从0开始逐渐增大
    regroup.reset_index(drop=True, inplace=True)
    return regroup


# def categorical_values_to_bins(categorical_values_df, col_key, col_values):
#     """
#     :param categorical_values_df: 数据框dataframe，必须含col_key, col_values字段
#     :param col_key: string, 字段名，该字段存储了区间划分的依据
#     :param col_values: string, 字段名，该字段存储了非重复的类别取值
#     :return: bin_range_df, 只有一个col: bin_range, 取值为分箱对应的col_values取值list
#     """
#     col_values_indices_dict = categorical_values_df.groupby(col_key).indices
#     bin_range_df = pd.DataFrame(columns=['bin_range'], dtype='object')
#     for key_range, indices in col_values_indices_dict.items():
#         values = categorical_values_df.loc[indices, col_values].tolist()
#         values = values if isinstance(values, list) else [values]
#         bin_df = pd.DataFrame(columns=['bin_range'], dtype='object')
#         bin_df.at[0, 'bin_range'] = values
#         bin_range_df = pd.concat([bin_range_df, bin_df])
#     bin_range_df.reset_index(drop=True, inplace=True)
#     return bin_range_df


# def categorical_bins_to_values(categorical_bins_df, col_no, col_range):
#     """
#     :param categorical_bins_df: 数据框dataframe，必须含col_no, col_bins字段
#     :param col_no: string, 分箱号的字段名，取值是非重复的
#     :param col_range: string, 字段名，存储了每个分箱对应的col_values取值列表
#     :return: binno_to_colvalues_dict, 键值为bin_no，取值为分箱对应的col_values取值list
#              binno_to_colvalues_df, 主要是为了便于展示分箱结果
#     """
#     binno_to_colvalues_df = pd.DataFrame(columns=['bin_range', 'bin_no'])
#     binno_to_colvalues_dict = {}
#     binrange_list = categorical_bins_df(col_range).tolist()
#     binno_list = categorical_bins_df(col_no).tolist()
#     for bin_no, col_values in zip(binno_list, binrange_list):
#         col_values = col_values if isinstance(col_values, list) else [col_values]
#         binno_to_colvalues_dict[bin_no] = col_values
#         bin_df = pd.DataFrame(columns=['bin_range', 'bin_no'])
#         bin_df['bin_range'] = col_values
#         bin_df['bin_no'] = bin_no
#         binno_to_colvalues_df = pd.concat([binno_to_colvalues_df, bin_df])
#     binno_to_colvalues_df.reset_index(drop=False, inplace=True)
#     binno_to_colvalues_df = \
#         binno_to_colvalues_df.astype({'bin_range': 'float', 'bin_no': 'object'})
#     return binno_to_colvalues_dict, binno_to_colvalues_df


def cal_chi2(df, bad_col, good_col, total_col):
    """
    :param df: 只有两个分箱的样本数据.
    :param bad_col: 列明string, 统计某个取值的坏样本数
    :param good_col: 列明string, 统计某个取值的好样本数
    :param total_col: 列明string, 统计某个取值的全部样本数
    :return: chi2 二联卡卡方值
    """
    all_bad_rate = df[bad_col].sum() * 1.0 / df[total_col].sum()
    all_good_rate = df[good_col].sum() * 1.0 / df[total_col].sum()
    # 当全部样本只有好或者坏样本时，卡方值为0
    if all_bad_rate in [0, 1]:
        return 0.0
    df2 = df.copy()
    # 计算每组的坏用户期望数量
    df2['bad_expected'] = df2[total_col] * all_bad_rate
    df2['good_expected'] = df2[total_col] * all_good_rate
    # 遍历每组的坏用户期望数量和实际数量
    bad_combined = zip(df2['bad_expected'], df2[bad_col])
    good_combined = zip(df2['good_expected'], df2[good_col])
    # 计算每组的卡方值
    bad_chi = [(i[0] - i[1]) ** 2 / (i[0] + 1e-6) for i in bad_combined]
    good_chi = [(i[0] - i[1]) ** 2 / (i[0] + 1e-6) for i in good_combined]
    # 计算总的卡方值
    chi2 = sum(bad_chi) + sum(good_chi)
    return chi2


def combine_bin_df(regroup, col, best_combined_index, continuous_flag=False):
    """
    :param regroup: dataframe [feature_name(optional), col, bin_total] or
      [feature_name(optional), col, bin_total, bin_bad, bin_good, bin_bad_rate]
      each row of col is a list if continuous_flag is False, else a pd.Interval.
      the indices must be increasing from 0 with increment of 1
    :param col: string, name of the feature range
    :param best_combined_index: int, the rows of this index
      and the next index of regroup will be combined and then filled
      into the row of this index, and then the row of the next index will be removed
    :param continuous_flag: bool
    """
    regroup_df = regroup.copy()
    # do this because pd.categorical dtype is not allowed to edit
    if continuous_flag:
        regroup_df[[col]] = regroup_df[[col]].astype('object')
    combine_df = regroup_df.loc[best_combined_index:best_combined_index+1, :]
    if continuous_flag:
        # pd.dataframe.at is like loc,
        # must use the index and column name, rather than positions
        regroup_df.at[best_combined_index, col] = pd.Interval(
            left=combine_df[col][best_combined_index].left,
            right=combine_df[col][best_combined_index+1].right)
    else:
        regroup_df.at[best_combined_index, col] = \
            combine_df[col][best_combined_index] + combine_df[col][best_combined_index+1]
    regroup_df.at[best_combined_index, 'bin_total'] = combine_df['bin_total'].sum()
    if 'bin_bad_rate' in regroup.columns.tolist():
        regroup_df.at[best_combined_index, 'bin_bad'] = combine_df['bin_bad'].sum()
        regroup_df.at[best_combined_index, 'bin_good'] = combine_df['bin_good'].sum()
        regroup_df.at[best_combined_index, 'bin_bad_rate'] = \
            regroup_df['bin_bad'][best_combined_index] / regroup_df['bin_total'][best_combined_index]
    # 删除合并前的右区间, regroup_df的index始终保持从0开始从小到大排序
    regroup_df = regroup_df.loc[regroup_df.index != (best_combined_index+1), :]
    # make sure the indices are increasing from 0 with increment 1 when bin_df's returned
    regroup_df.reset_index(drop=True, inplace=True)
    return regroup_df


def bin_bad_rate(df, col, target):
    """
    :param df: dataframe
    :param col: string, 需要计算好坏率的变量名
    :param target:string, 目标变量的字段名
    :return:dataframe[col, bin_total, bin_bad, bin_good, bin_bad_rate]
            按照col取值去重后从小到大排列， index一定是从0开始逐渐编号
    """
    # 按col的值去重后从小到大排列，并作为index
    total = df.groupby([col])[target].count()
    bad = df.groupby([col])[target].sum()
    regroup = pd.merge(pd.DataFrame({'bin_total': total}),
                       pd.DataFrame({'bin_bad': bad}),
                       left_index=True, right_index=True, how='left')
    # 默认drop=false，原来的index，即col的值去重后从小到大排列的值，另外生成一列
    regroup = regroup.reset_index()
    # 计算根据col分组后每组的违约率, 对于无顺序型数据，需要计算好坏比来代替原来离散的数值
    regroup['bin_good'] = regroup['bin_total'] - regroup['bin_bad']
    regroup['bin_bad_rate'] = regroup['bin_bad'] / regroup['bin_total']
    return regroup


def compute_woe_iv(bin_df, col_good, col_bad, col_total):
    """
    param bin_df:DataFrame|分箱表, 按照bin_range,
        或col_values取值去重后从小到大排列
    param col_good:str|feature名称，统计每个分箱的好样本个数
    param col_bad:str|feature名称，统计每个分箱的坏样本个数
    param col_total:str|feature名称，统计每个分箱一共有多少样本
    return: 原dataframe增添多列
    """
    d2 = bin_df.copy()
    total = d2[col_total].sum()
    bad = d2[col_bad].sum()
    good = total - bad

    d2['bin_good_rate'] = d2[col_good] / d2[col_total]
    d2['badattr'] = d2[col_bad] / bad
    d2['goodattr'] = d2[col_good] / good
    sum_bad = 0
    acc_bad_rate_list = []
    for i in d2[col_bad]:
        sum_bad += i
        acc_bad_rate_list.append(sum_bad / bad)
    d2['acc_bad_rate'] = acc_bad_rate_list
    sum_good = 0
    acc_good_rate_list = []
    for i in d2[col_good]:
        sum_good += i
        acc_good_rate_list.append(sum_good / good)
    d2['acc_good_rate'] = acc_good_rate_list
    d2['bin_total_rate'] = d2[col_total] / total
    d2['total_bad_rate'] = bad / total

    def compute_woe(badattr, goodattr):
        return np.log(badattr / (goodattr + 1e-6) + 1e-6)
    # 如果有全bad的分箱，则该分箱woe=inf，表示该分箱的坏账率远大于整体坏账率
    # 如果有全good的分箱，则woe=-inf，表示该分箱坏账率远小于整体坏账率
    # 如果分箱的坏账率和整体一致，则woe=0
    # 因此woe取值范围是(-inf---inf)
    d2['bin_woe'] = d2.apply(
        lambda x: compute_woe(x['badattr'], x['goodattr']),
        axis=1)
    # 如果有全bad或全good的分箱，则iv=inf，表示该分箱的坏账率水平和整体相比差异大
    #   该分箱预测能力极高
    # 如果分箱坏账率和整体一致，则iv=0，表示该分箱没有预测能力
    # 因此iv取值范围是[0----inf)
    d2['bin_iv'] = d2.apply(
        lambda x: (x['badattr'] - x['goodattr']) * x['bin_woe'],
        axis=1)
    # 变量的总iv
    d2['iv'] = d2['bin_iv'].sum()

    d2.drop(['badattr', 'goodattr'], axis=1, inplace=True)

    return d2


def cal_ks(predict, target, plot=False):
    """
    ks经济学意义:
      将预测为坏账的概率从大到小排序，然后按从大到小依次选取一个概率值作为阈值，
      大于阈值的部分为预测为坏账的部分--记录其中真实为坏账的个数， 真实为好账的个数，
      上述记录值每次累加且除以总的坏账个数即累计坏账率，除以总好账个数为累计好账率, 累加结果存入列表
    sklearn.metrics.roc_curve（二分类标签，预测为正例的概率或得分）:
      将预测为正例（默认为1）的概率（0-1间）或得分（不限大小）从大到小排序, 然后按从大到小依次选取一个值作为阈值
      大于阈值的部分为预测为正例的部分--其中真实为正例的个数即TP, 真实为负例的个数即为FP
      上述值每次累加且除以总的正例个数为TPR, 除以总的负例个数为FPR，累加结果存入列表
    ks = max(累计坏账率list - 累计好账率list) = max(TPR_list - FPR_list)
    :param predict: list like, 可以为某个数值型特征字段，也可以是预测为坏账的概率的字段
    :param target: list like, 好坏账标签字段，字段中1为坏账
    :param plot: bool, 是否画图
    :return: ks, ks_thresh
    """
    # fpr即FPR_list, tpr即TPR_list, thresholds为上述所谓依次选取的阈值
    # thresholds一定是递减的，第一个值为max(预测为正例的概率或得分)+1
    fpr, tpr, thresholds = roc_curve(target, predict)
    ks = (tpr-fpr).max()
    ks_index = np.argmax(tpr-fpr)
    ks_thresh = thresholds[ks_index]
    if plot:
        # 绘制曲线
        plt.plot(tpr, label='bad_cum', linewidth=2)
        plt.plot(fpr, label='good_cum', linewidth=2)
        plt.plot(tpr-fpr, label='ks_curve', linewidth=2)
        # 标记ks点
        x_point = (ks_index, ks_index)
        y_point = (fpr[ks_index], tpr[ks_index])
        plt.plot(x_point, y_point, label='ks {:.2f}@{:.2f}'.format(ks, ks_thresh),
                 color='r', marker='o', markerfacecolor='r',
                 markersize=5)
        plt.scatter(x_point, y_point, color='r')
        # 绘制x轴（阈值）, thresholds第一个值为max(预测为正例的概率或得分)+1, 因此不画出来
        effective_indices_num = thresholds[1:].shape[0]
        if effective_indices_num > 5:
            # 向下取整
            increment = int(effective_indices_num / 5)
        else:
            increment = 1
        indices = range(1, thresholds.shape[0], increment)
        plt.xticks(indices, [round(i, 2) for i in thresholds[indices]])
        plt.xlabel('thresholds')
        plt.legend()
        plt.show()
    return ks, ks_thresh


def plot_roc(label, prediction):
    fpr, tpr, thresholds = roc_curve(label, prediction, pos_label=1)
    metric = auc(fpr, tpr)
    plt.plot(fpr, tpr)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.title('ROC curve, auc:%.4f' % metric)
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.grid(True)
    plt.show()


def calc_lift(df, pred, target, groupnum=None, plot=True):
    if groupnum is None:
        groupnum = len(df.index)

    def n0(x): return sum(x == 0)
    def n1(x): return sum(x == 1)
    dfkslift = df.sort_values(pred, ascending=False).reset_index(drop=True)\
        .assign(group=lambda x: np.ceil((x.index+1)/(len(x.index)/groupnum)))\
        .groupby('group')[target].agg([n0, n1])\
        .reset_index().rename(columns={'n0': 'good', 'n1': 'bad'})\
        .assign(
        group=lambda x: (x.index+1)/len(x.index),
        good_distri=lambda x: x.good/sum(x.good),
        bad_distri=lambda x: x.bad/sum(x.bad),
        badrate=lambda x: x.bad/(x.good+x.bad),
        cumbadrate=lambda x: np.cumsum(x.bad)/np.cumsum(x.good+x.bad),
        lift=lambda x: (np.cumsum(x.bad)/np.cumsum(x.good+x.bad))/(sum(x.bad)/sum(x.good+x.bad)),
        cumgood=lambda x: np.cumsum(x.good)/sum(x.good),
        cumbad=lambda x: np.cumsum(x.bad)/sum(x.bad))\
        .assign(ks=lambda x: abs(x.cumbad-x.cumgood))
    dfkslift = pd.concat([pd.DataFrame({'group': 0, 'good': 0, 'bad': 0,
                                        'good_distri': 0, 'bad_distri': 0,
                                        'badrate': 0, 'cumbadrate': np.nan,
                                        'cumgood': 0, 'cumbad': 0, 'ks': 0, 'lift': np.nan}, index=np.arange(1)),
                          dfkslift], ignore_index=True)

    if plot:
        dfks = dfkslift.loc[lambda x: x.ks == max(x.ks)].sort_values('group').iloc[0]
        fig, ax = plt.subplots()
        ax.plot(dfkslift.group, dfkslift.ks, 'b-',
                 dfkslift.group, dfkslift.cumgood, 'k-',
                 dfkslift.group, dfkslift.cumbad, 'k-')
        ax.plot([dfks['group'], dfks['group']], [0, dfks['ks']], 'r--')
        fig.gca().set(title='K-S', xlabel='worst % of population', ylabel='total good/bad rate',
                      xlim=[0, 1], ylim=[0, 1], aspect='equal')
        ax.text(0.2, 0.8, 'Bad', horizontalalignment='center')
        ax.text(0.8, 0.55, 'Good', horizontalalignment='center')
        ax.text(dfks['group'], dfks['ks'], 'KS:' + str(round(dfks['ks'], 2)) + '@' +
                str(round(dfks['group'], 2)), horizontalalignment='center', color='b')

        badrate_avg = sum(dfkslift.bad)/sum(dfkslift.good+dfkslift.bad)
        fig, ax = plt.subplot(2, 1, 2)
        ax.plot(dfkslift.group, dfkslift.cumbadrate, 'k-')
        ax.plot([0, 1], [badrate_avg, badrate_avg], 'r--')
        fig.gca().set(title='Lift', xlabel='worst % of population', ylabel='group bad rate',
                      xlim=[0, 1], ylim=[0, 1], aspect='equal')
        ax.text(0.7, np.mean(dfkslift.cumbadrate), 'cumulate badrate', horizontalalignment='center')
        ax.text(0.7, badrate_avg, 'mean: ' + str(round(badrate_avg, 2)), horizontalalignment='center')
    return dfkslift


def cal_psi_bin(base_bin_total, expected_bin_total):
    """
    :param base_bin_total: pd.Series, number of values in each bin
    :param expected_bin_total: pd.Series, number of values in each bin
    """
    assert base_bin_total.shape[0] == expected_bin_total.shape[0]
    base_total = base_bin_total.sum()
    expected_total = expected_bin_total.sum()
    psi_list = []
    psi = 0
    for i in range(base_bin_total.shape[0]):
        base = base_bin_total.iloc[i] / base_total
        expected = expected_bin_total.iloc[i] / expected_total
        p = (expected - base) * np.log(expected / (base + 1e-6) + 1e-6)
        psi_list.append(p)
        psi += p
    return psi, psi_list


def check_trend(var_series, time_series, interval, continuous=True):
    """
    :param var_series: pd.Series, 变量
    :param time_series: pd.Series, 时间
    :param interval: int,间隔,以天为单位
    :param continuous: bool,是否是连续性变量
    """
    time_series = pd.to_datetime(time_series)
    first = time_series.min()
    last = time_series.max()
    date_list = []

    def agg_func(input_series):
        num = input_series.shape[0]
        return [input_series.quantile(0.5),
                input_series.mean(),
                input_series.isnull().sum() / num]

    df_values = []
    for i in range(0, (last - first).days - interval, interval):
        left = first + datetime.timedelta(days=i)
        right = left + datetime.timedelta(days=interval)
        date_list.append('[' + left.strftime("%Y-%m-%d") + ' - '
                         + right.strftime("%Y-%m-%d") + ')')
        data_set = var_series[(time_series >= left) & (time_series < right)]
        if continuous:
            df_values.append(agg_func(data_set))
        else:
            df_values.append([data_set.isnull().sum() / data_set.shape[0]])
    left = right
    right = last
    date_list.append('[' + left.strftime("%Y-%m-%d") + ' - '
                     + right.strftime("%Y-%m-%d") + ']')
    data_set = var_series[(time_series >= left) & (time_series <= right)]
    if continuous:
        df_values.append(agg_func(data_set))
        output_df = pd.DataFrame(df_values, index=date_list,
                                 columns=['0.5q', 'mean', 'null_rate'])
    else:
        df_values.append([data_set.isnull().sum() / data_set.shape[0]])
        output_df = pd.DataFrame(df_values, index=date_list,
                                 columns=['null_rate'])
    return output_df


def plot_trend(df_list, val_column, name_list=[''], save_dir=None):
    """
    看不同数据集上，某个变量随时间变化的趋势是否一致
    :param df_list: list of pd.dataframe, dataframe的index为时间
    :param val_column: string, 当name_list==1的是时候是要看趋势的变量名
                               否则为统计量的名称
    :param name_list: list of string, df_list每个元素的名字
    :param save_dir: string, 当前路径下的相对路径
    """
    assert len(df_list) == len(name_list)
    if len(name_list) == 1:
        trend_df = df_list[0]
    else:
        trend_df = df_list[0][[val_column]].rename(
            columns={val_column: name_list[0]})
        for df, name in zip(df_list[1:], name_list[1:]):
            trend_df = trend_df.join(df[val_column].rename(name), how='outer')
    trend_df.plot(marker='o', markersize=3, title=val_column)
    plt.legend()
    # 绘制x轴（阈值）
    effective_indices_num = trend_df.index.shape[0]
    if effective_indices_num > 5:
        # 向下取整
        increment = int(effective_indices_num / 5)
    else:
        increment = 1
    indices = range(0, effective_indices_num, increment)
    plt.xticks(indices, [i for i in trend_df.index[indices]],
               rotation=-20, horizontalalignment='left')
    if save_dir is not None:
        current_dir = os.getcwd()
        new_dir = os.path.join(current_dir, save_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        save_path = os.path.join(new_dir, val_column + '.jpg')
        plt.savefig(save_path, bbox_inches='tight')
        plt.clf()
        plt.close('all')
    else:
        plt.show()


def check_statistics(df, val_list, continuous=True):
    """
    :param df: pd.dataframe
    :param val_list: list of string, 变量名列表
    :param continuous: bool,是否是连续性变量
    """
    def agg_func_co(input_series):
        num = input_series.shape[0]
        result_arr = np.concatenate(
            (input_series.quantile([0.25, 0.5, 0.75]),
             [input_series.max(), input_series.min(),
              input_series.mean(), input_series.isnull().sum() / num]))
        return pd.Series(result_arr,
                         index=['0.25q', '0.5q', '0.75q',
                                'max', 'min', 'mean', 'null_rate'])

    if continuous:
        output_df = df.loc[:, val_list].apply(agg_func_co, axis=0)
    else:
        output_df = df.loc[:, val_list].apply(
            lambda x: pd.Series(x.isnull().sum() / x.shape[0],
                                index=['null_rate']), axis=0)
    return output_df


def plot_statistics(df_list, val_column, statistics_list,
                    plot_type='bar', name_list=[''], save_dir=None):
    """
    看不同数据集上，某个变量的各项统计指标是否一致
    :param df_list: list of pd.dataframe, dataframe的index是统计指标
    :param val_column: string,要查看的变量名
    :param statistics_list: list of string,统计指标列表，必须和dataframe对应
    :param plot_type: string，如果是bar的话为柱状图，否则为折线图
    :param name_list: list of string, df_list里面的每个元素的名字
    :param save_dir: string,当前路径下的相对路径
    """
    assert len(df_list) == len(name_list)
    if len(name_list) == 1:
        df_bar = df_list[0].loc[statistics_list, [val_column]]
    else:
        df_bar = df_list[0].loc[statistics_list, [val_column]].rename(
            columns={val_column: name_list[0]})
        for df, name in zip(df_list[1:], name_list[1:]):
            df_bar = df_bar.join(
                df.loc[statistics_list, val_column].rename(name), how='outer')
    if plot_type == 'bar':
        df_bar.plot(kind='bar', title=val_column)
    else:
        df_bar.plot(marker='o', markersize=3, title=val_column)
    plt.legend()
    if save_dir is not None:
        current_dir = os.getcwd()
        new_dir = os.path.join(current_dir, save_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        save_path = os.path.join(new_dir, val_column + '.jpg')
        plt.savefig(save_path)
        plt.clf()
        plt.close('all')
    else:
        plt.show()


def plot_bin_df(bin_df_list, name_list=[''], save_dir=None):
    """
    :param bin_df_list: list of dataframe
    :param name_list: bin_df_list里面每个元素的名字
    :param save_dir: string, 前路径下的相对路径
    """
    assert len(bin_df_list) == len(name_list)
    if len(name_list) == 1:
        bar_width = 0.9
    else:
        bar_width = 0.8
    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    df_bin_total = pd.DataFrame()
    df_bad_rate = pd.DataFrame()
    for bin_df, name in zip(bin_df_list, name_list):
        bin_pct_series = bin_df['bin_total_rate'].rename(name + ' bin_pct')
        df_bin_total = pd.concat([df_bin_total, bin_pct_series], axis=1)
        if 'bin_bad_rate' in bin_df.columns.tolist():
            bad_rate_series = bin_df['bin_bad_rate'].rename(name + ' bad_rate')
            df_bad_rate = pd.concat([df_bad_rate, bad_rate_series], axis=1)
    df_bin_total.index = bin_df['bin_no']
    title = bin_df['feature_name'][0]
    ax = df_bin_total.plot(kind='bar', cmap=cm_light,
                           width=bar_width, title=title)
    if 'bin_bad_rate' in bin_df.columns.tolist():
        df_bad_rate.plot(ax=ax, marker='o', markersize=5, cmap=cm_dark)
    ax.set_xlim([-0.5, bin_df.shape[0] - 0.5])
    plt.legend()
    plt.xlabel('bin no.')
    if save_dir is not None:
        current_dir = os.getcwd()
        new_dir = os.path.join(current_dir, save_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        save_path = os.path.join(new_dir, title + '.jpg')
        plt.savefig(save_path)
        plt.clf()
        plt.close('all')
    else:
        plt.show()


# def cal_psi_score(base, expectation):
#     """
#     :param base: pd.Series
#     :param expectation: pd.Series
#     """
#     base_column = pd.qcut(base, 10, duplicates='drop')
#     base_bin = pd.DataFrame(base_column.cat.categories, columns=['bin_range'])
#     base_bin = map_to_inf(base_bin, 'bin_range')
#     base_column = base.astype('category').cat.set_categories(base_bin['bin_range'], ordered=True)
#     base_bin_total = base_column.value_counts().sort_index()
#     expectation_column = pd.cut(expectation, base_bin['bin_range'].astype('category').cat.categories)
#     expected_bin_total = expectation_column.value_counts().sort_index()
#     psi, psi_list = cal_psi_bin(base_bin_total, expected_bin_total)
#     return psi, psi_list


def cal_psi_score(actual_array, expected_array,
                  bins=10, quantile=True, detail=False):
    """
    :param actual_array: np.array
    :param expected_array: np.array
    :param bins: int, number_of_bins you want for calculating psi
    :param quantile: bool
    :param detail: bool, if True, print the process of calculation
    """
    # 异常处理，所有取值都相同时, 说明该变量是常量, 返回None
    if np.min(expected_array) == np.max(expected_array):
        return None
    expected_array = pd.Series(expected_array).dropna()
    actual_array = pd.Series(actual_array).dropna()

    """step1: 确定分箱间隔"""
    def scale_range(input_array, scaled_min, scaled_max):
        """
        功能: 对input_array线性放缩至[scaled_min, scaled_max]
        :param input_array: numpy array of original values, 需放缩的原始数列
        :param scaled_min: float, 放缩后的最小值
        :param scaled_max: float, 放缩后的最大值
        :return input_array: numpy array of original values, 放缩后的数列
        """
        input_array += -np.min(input_array) # 此时最小值放缩到0
        if scaled_max == scaled_min:
            raise Exception('放缩后的数列scaled_min = scaled_min, 值为{}, '
                            '请检查expected_array数值！'.format(scaled_max))
        scaled_slope = np.max(input_array) * 1.0 / (scaled_max - scaled_min)
        input_array /= scaled_slope
        input_array += scaled_min
        return input_array

    breakpoints = np.arange(0, bins + 1) / bins * 100  # 等距分箱百分比
    if not quantile:
        # 等距分箱
        breakpoints = scale_range(breakpoints,
                                  np.min(expected_array),
                                  np.max(expected_array))
    else:
        # 等频分箱
        breakpoints = np.stack([np.percentile(expected_array, b)
                                for b in breakpoints])

    """step2: 统计区间内样本占比"""
    def generate_counts(arr, breakpoints):
        """
        功能: Generates counts for each bucket by using the bucket values
        :param arr: ndarray of actual values
        :param breakpoints: list of bucket values
        :return cnt_array: counts for elements in each bucket,
                           length of breakpoints array minus one
        :return score_range_array: 分箱区间
        """
        def count_in_range(input_arr, low, high, start):
            """
            功能: 统计给定区间内的样本数(Counts elements in array between
                 low and high values)
            :param input_arr: ndarray of actual values
            :param low: float, 左边界
            :param high: float, 右边界
            :param start: bool, 取值为Ture时，区间闭合方式[low, high],否则为(low, high]
            :return cnt_in_range: int, 给定区间内的样本数
            """
            if start:
                cnt_in_range = len(np.where(np.logical_and(input_arr >= low,
                                                           input_arr <= high))[0])
            else:
                cnt_in_range = len(np.where(np.logical_and(input_arr > low,
                                                           input_arr <= high))[0])
            return cnt_in_range
        cnt_array = np.zeros(len(breakpoints) - 1)
        range_array = [''] * (len(breakpoints) - 1)
        for i in range(1, len(breakpoints)):
            cnt_array[i - 1] = count_in_range(arr,
                                              breakpoints[i - 1],
                                              breakpoints[i], i == 1)
            if 1 == i:
                range_array[i - 1] = '[' + \
                                     str(round(breakpoints[i - 1], 4)) \
                                     + ',' + str(round(breakpoints[i], 4)) \
                                     + ']'
            else:
                range_array[i - 1] = '(' + \
                                     str(round(breakpoints[i - 1], 4)) \
                                     + ',' + str(round(breakpoints[i], 4)) \
                                     + ']'

        return cnt_array, range_array

    expected_cnt, score_range_array = generate_counts(expected_array,
                                                      breakpoints)[0]
    expected_percents = expected_cnt / len(expected_array)
    actual_cnt = generate_counts(actual_array, breakpoints)[0]
    actual_percents = actual_cnt / len(actual_array)
    delta_percents = actual_percents - expected_percents
    score_range_array = generate_counts(expected_array, breakpoints)[1]

    """step3: 得到最终稳定性指标"""
    def sub_psi(e_perc, a_perc):
        """
        功能: 计算单个分箱内的psi值
        :param e_perc: float, 期望占比
        :param a_perc: float, 实际占比
        :return value: float, 单个分箱内的psi值
        """
        if a_perc == 0: # 实际占比
            a_perc = 0.001
        if e_perc == 0: # 期望占比
            e_perc = 0.001
        value = (e_perc - a_perc) * np.log(e_perc * 1.0 / a_perc)
        return value
    sub_psi_array = [sub_psi(expected_percents[i], actual_percents[i])
                     for i in range(0, len(expected_percents))]
    if detail:
        psi_value = pd.DataFrame()
        psi_value['score_range'] = score_range_array
        psi_value['expecteds'] = expected_cnt
        psi_value['expected(%)'] = expected_percents * 100
        psi_value['actucals'] = actual_cnt
        psi_value['actucal(%)'] = actual_percents * 100
        psi_value['ac - ex(%)'] = delta_percents * 100
        psi_value['actucal(%)'] = psi_value['actucal(%)'].apply(
            lambda x: round(x, 2))
        psi_value['ac - ex(%)'] = psi_value['ac - ex(%)'].apply(
            lambda x: round(x, 2))
        psi_value['ln(ac/ex)'] = psi_value.apply(
            lambda row: np.log((row['actucal(%)'] + 0.001)
                               / (row['expected(%)'] + 0.001)), axis=1)
        psi_value['psi'] = sub_psi_array
        flag = lambda x: '<<<<<<<' if x == psi_value.psi.max() else ''
        psi_value['max'] = psi_value.psi.apply(flag)
        psi_value = psi_value.append([{'score_range': '>>> summary',
                                       'expecteds': sum(expected_cnt),
                                       'expected(%)': 100,
                                       'actucals': sum(actual_cnt),
                                       'actucal(%)': 100,
                                       'ac - ex(%)': np.nan,
                                       'ln(ac/ex)': np.nan,
                                       'psi': np.sum(sub_psi_array),
                                       'max': '<<< result'}], ignore_index=True)
    else:
        psi_value = np.sum(sub_psi_array)
    return psi_value


def check_monotone(regroup, col, ascending):
    """
    :param regroup: dataframe, bin_df with bin_woe
    :param col: str, the column to be chekcked
    :param ascending: True for ascending, False for descending, None for any one
    """
    if regroup.shape[0] <= 2 and (ascending is None):
        return True
    my_list = regroup[col].tolist()

    # ascending
    flag1 = all(x < y for x, y in zip(my_list, my_list[1:]))
    # descending
    flag2 = all(x > y for x, y in zip(my_list, my_list[1:]))
    if ascending is not None:
        if ascending:
            return flag1
        else:
            return flag2
    else:
        return flag1 or flag2


def chi2_merge(regroup, col, max_bin_num=5, min_binpct=0.0, monoticity=True):
    """
    :param regroup: dataframe [col, bin_total, bin_bad, bin_good, bin_bad_rate]
       rows of col are all list
       indices must be increasing from 0 with increment 1
    :param col: string, col name
    :param max_bin_num: int
    :param min_binpct: float
    :param monoticity: bool. If false, bad_rate could be of no order
    :return: dataframe [col, bin_total, bin_bad, bin_good, bin_bad_rate]
      indices is increasing from 0 with increment 1
    """
    monotone = False
    while not monotone:
        # 按卡方合并箱体
        # 当group_interval的长度大于max_bin时，执行while循环
        while regroup.shape[0] > max_bin_num:
            chi_list = []
            for i in range(regroup.shape[0] - 1):
                # 计算每一对相邻区间的卡方值
                chi_df = regroup.loc[i:i+1, :]
                chi_value = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                chi_list.append(chi_value)
            # 最小的卡方值的索引,如最小值不止一个则index函数保证取第一个
            best_combined_index = chi_list.index(min(chi_list))
            # 将卡方值最小的一对区间进行合并
            regroup = combine_bin_df(regroup, col, best_combined_index)

        bin_df = regroup.copy()
        # 检查是否有箱只有好样本或者只有坏样本
        min_bad_rate = bin_df['bin_bad_rate'].min()
        max_bad_rate = bin_df['bin_bad_rate'].max()
        while min_bad_rate == 0.0 or max_bad_rate == 1.0:
            # 违约率为1或0的箱体的index. index总是返回列表，因此用[0]取第一个元素
            bad_index = bin_df[bin_df['bin_bad_rate'].isin([0.0, 1.0])].index[0]
            if bad_index == (bin_df.shape[0] - 1):
                bin_df = combine_bin_df(bin_df, col, bad_index-1)
            elif bad_index == 0:
                bin_df = combine_bin_df(bin_df, col, 0)
            else:
                # 计算bad_index和前面一个的箱体的卡方值
                chi_df = bin_df.loc[bad_index-1:bad_index, :]
                chi1 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                # 计算bad_index和后一个箱体之间的卡方值
                chi_df = bin_df.loc[bad_index:bad_index+1, :]
                chi2 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                if chi1 < chi2:
                    # 当chi1<chi2时, 合并bad_index之前与bad_index对应的箱体
                    bin_df = combine_bin_df(bin_df, col, bad_index-1)
                else:
                    # 当chi1>=chi2时,合并bad_index和bad_index之后对应的箱体
                    bin_df = combine_bin_df(bin_df, col, bad_index)

            # 计算每个区间的违约率, 其index一定是从0开始从小到大编号
            min_bad_rate = bin_df['bin_bad_rate'].min()
            max_bad_rate = bin_df['bin_bad_rate'].max()

        # 检查分箱后的最小占比
        if min_binpct > 0.0:
            # 得出最小的区间占比
            min_pct = (bin_df['bin_total'] / bin_df['bin_total'].sum()).min()
            # 当最小的区间占比小于min_binpct且箱体的个数大于3
            while min_pct < min_binpct and bin_df.shape[0] > 3:
                # 下面的逻辑基本与“检验是否有箱体只有好/坏样本”的一致
                bad_index = \
                    bin_df[(bin_df['bin_total']
                            / bin_df['bin_total'].sum()) == min_pct].index[0]
                if bad_index == (bin_df.shape[0] - 1):
                    bin_df = combine_bin_df(bin_df, col, bad_index-1)
                elif bad_index == 0:
                    bin_df = combine_bin_df(bin_df, col, 0)
                else:
                    chi_df = bin_df.loc[bad_index-1:bad_index, :]
                    chi1 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                    chi_df = bin_df.loc[bad_index:bad_index+1, :]
                    chi2 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                    if chi1 < chi2:
                        bin_df = combine_bin_df(bin_df, col, bad_index-1)
                    else:
                        bin_df = combine_bin_df(bin_df, col, bad_index)
                min_pct = (bin_df['bin_total'] / bin_df['bin_total'].sum()).min()
        if monoticity:
            bin_df2 = compute_woe_iv(bin_df, 'bin_good', 'bin_bad', 'bin_total')
            monotone = check_monotone(bin_df2, 'bin_woe', None)
            if not monotone:
                print('another chi2 merge is going to be made as the bad rate is not monotonic')
            max_bin_num -= 1
        else:
            break
    return bin_df


def check_bin(regroup, col, continuous_flag, min_binpct=0.05, monoticity=True):
    """
    :param regroup: dataframe [col, bin_total, bin_bad, bin_good, bin_bad_rate]
       indices must be increasing from 0 with increment 1
    :param col: string, col name
    :param min_binpct: float
    :param monoticity: bool. If false, bad_rate could be of no order
    :return: dataframe [col, bin_total, bin_bad, bin_good, bin_bad_rate]
      indices is increasing from 0 with increment 1
    """
    bin_df = regroup.copy()
    # 检查是否有箱只有好样本或者只有坏样本
    min_bad_rate = bin_df['bin_bad_rate'].min()
    max_bad_rate = bin_df['bin_bad_rate'].max()
    while (min_bad_rate == 0.0 or max_bad_rate == 1.0) and bin_df.shape[0] > 2:
        # 违约率为1或0的箱体的index. index总是返回列表，因此用[0]取第一个元素
        bad_index = bin_df[bin_df['bin_bad_rate'].isin([0.0, 1.0])].index[0]
        if bad_index == (bin_df.shape[0] - 1):
            bin_df = combine_bin_df(bin_df, col, bad_index - 1, continuous_flag)
        elif bad_index == 0:
            bin_df = combine_bin_df(bin_df, col, 0, continuous_flag)
        else:
            # 计算bad_index和前面一个的箱体的卡方值
            chi_df = bin_df.loc[bad_index - 1:bad_index, :]
            chi1 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
            # 计算bad_index和后一个箱体之间的卡方值
            chi_df = bin_df.loc[bad_index:bad_index + 1, :]
            chi2 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
            if chi1 < chi2:
                # 当chi1<chi2时, 合并bad_index之前与bad_index对应的箱体
                bin_df = combine_bin_df(bin_df, col, bad_index - 1, continuous_flag)
            else:
                # 当chi1>=chi2时,合并bad_index和bad_index之后对应的箱体
                bin_df = combine_bin_df(bin_df, col, bad_index, continuous_flag)

        # 计算每个区间的违约率, 其index一定是从0开始从小到大编号
        min_bad_rate = bin_df['bin_bad_rate'].min()
        max_bad_rate = bin_df['bin_bad_rate'].max()
    if (min_bad_rate == 0.0 or max_bad_rate == 1.0) and bin_df.shape[0] <= 2:
        print('all good or bad, failure')
        return None

    # 检查分箱后的最小占比
    if min_binpct > 0.0:
        # 得出最小的区间占比
        min_pct = (bin_df['bin_total'] / bin_df['bin_total'].sum()).min()
        # 当最小的区间占比小于min_binpct且箱体的个数大于2
        while min_pct < min_binpct and bin_df.shape[0] > 2:
            # 下面的逻辑基本与“检验是否有箱体只有好/坏样本”的一致
            bad_index = \
                bin_df[(bin_df['bin_total']
                        / bin_df['bin_total'].sum()) == min_pct].index[0]
            if bad_index == (bin_df.shape[0] - 1):
                bin_df = combine_bin_df(bin_df, col, bad_index - 1, continuous_flag)
            elif bad_index == 0:
                bin_df = combine_bin_df(bin_df, col, 0, continuous_flag)
            else:
                chi_df = bin_df.loc[bad_index - 1:bad_index, :]
                chi1 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                chi_df = bin_df.loc[bad_index:bad_index + 1, :]
                chi2 = cal_chi2(chi_df, 'bin_bad', 'bin_good', 'bin_total')
                if chi1 < chi2:
                    bin_df = combine_bin_df(bin_df, col, bad_index - 1, continuous_flag)
                else:
                    bin_df = combine_bin_df(bin_df, col, bad_index, continuous_flag)
            min_pct = (bin_df['bin_total'] / bin_df['bin_total'].sum()).min()
        if min_pct < min_binpct and bin_df.shape[0] <= 2:
            print('few data in a bin, failure')
            return None

    if monoticity:
        bin_df2 = compute_woe_iv(bin_df, 'bin_good', 'bin_bad', 'bin_total')
        monotone = check_monotone(bin_df2, 'bin_woe', None)
        if not monotone:
            print('woe not monotone, failure')
            return None
    return bin_df


def select_vals_using_iv(dict_of_bin_df, threshold_iv=0.02):
    indices_list = []
    iv_list = []
    for val_name, bin_df in dict_of_bin_df.items():
        indices_list.append(val_name)
        iv_list.append(bin_df['iv'].iloc[0])
    ax = plt.subplot(111)
    iv_series = pd.Series(iv_list, index=indices_list).sort_values(ascending=False)
    selected_vals_series = iv_series[iv_series >= threshold_iv]
    iv_series.plot(kind='bar', ax=ax, color='g', alpha=0.3)
    plt.ylabel('iv')
    plt.show()
    return selected_vals_series


def sub_chisq(ks_points, start, end, bc_gap, bad_rate):
    if start >= end - 1 or sum(ks_points[end][1:]) - sum(ks_points[start][1:]) < 2 * bc_gap:
        return []
    temp = []
    start_good, start_bad = ks_points[start][1], ks_points[start][2]
    good, bad = max(ks_points[end][1] - start_good, 1e-6), max(ks_points[end][2] - start_bad, 1e-6)
    if good == 0 or bad == 0:
        return []
    for j in range(start, end):
        cur_good = ks_points[j][1]
        cur_bad = ks_points[j][2]

        if cur_good + cur_bad > 0:
            left_total = cur_good - start_good + cur_bad - start_bad
            right_total = good - cur_good + bad - cur_bad
            left_bad_expected = int(left_total * bad_rate)
            right_bad_expected = int(right_total * bad_rate)
            left_good_expected = int(left_total * (1 - bad_rate))
            right_good_expected = int(right_total * (1 - bad_rate))
            a11 = 0 if left_good_expected == 0 else np.square(
                (cur_good - start_good) - left_good_expected) / left_good_expected
            a12 = 0 if left_bad_expected == 0 else \
                np.square((cur_bad - start_bad) - left_bad_expected) / left_bad_expected
            a21 = 0 if right_good_expected == 0 else np.square(
                (good - cur_good) - right_good_expected) / right_good_expected
            a22 = 0 if right_bad_expected == 0 else \
                np.square((bad - cur_bad) - right_bad_expected) / right_bad_expected
            chisq = a11 + a12 + a21 + a22

        else:
            chisq = -1
        temp.append((chisq, j - start))
    max_index = max(temp, key=lambda x: x[0])[1]
    while temp[max_index][0] > 0 and \
            (sum(ks_points[max_index + start][1:]) - sum(ks_points[start][1:]) < bc_gap
             or sum(ks_points[end][1:]) - sum(ks_points[max_index + start][1:]) < bc_gap):
        temp[max_index] = (-1, -1)
        ks_points[max_index + start] = (ks_points[max_index + start][0], 0, 0)
        max_index = max(temp, key=lambda x: x[0])[1]

    if temp[max_index][0] <= 0:
        return []
    return [ks_points[max_index + start]] + sub_chisq(ks_points, start, max_index + start, bc_gap, bad_rate) \
           + sub_chisq(ks_points, max_index + start, end, bc_gap, bad_rate)


def best_combine(ks_points, good_bad, piece, monotonicity, lower, upper):
    num_cut_point = len(ks_points)
    num_of_cut = min(piece - 1, num_cut_point)
    cut_points = list(itertools.combinations(range(num_cut_point), num_of_cut))
    sol, max_iv = None, 0
    for cut in cut_points:
        old, iv, iv_list, woe_list = [0, 0], 0, [], []
        for c in cut:
            good_pcnt = (ks_points[c][-2] - old[0]) / good_bad[0]
            bad_pcnt = (ks_points[c][-1] - old[1]) / good_bad[1]
            old = (ks_points[c][-2], ks_points[c][-1])
            woe_list.append(np.log(bad_pcnt / (good_pcnt + 1e-6) + 1e-6))
            iv_list.append(woe_list[-1] * (bad_pcnt - good_pcnt))
            iv += iv_list[-1]
        good_pcnt = (good_bad[0] - old[0]) / good_bad[0]
        bad_pcnt = (good_bad[1] - old[1]) / good_bad[1]
        woe_list.append(np.log(bad_pcnt / (good_pcnt + 1e-6) + 1e-6))
        iv_list.append(woe_list[-1] * (bad_pcnt - good_pcnt))
        iv += iv_list[-1]
        if iv > max_iv:
            flag = True
            flag2 = True
            if monotonicity:
                for i in range(1, len(woe_list)):
                    if woe_list[i] < woe_list[i - 1]:
                        flag = False
                        break
                for i in range(1, len(woe_list)):
                    if woe_list[i] >= woe_list[i - 1]:
                        flag2 = False
                        break
                flag = flag or flag2
            if upper < lower:
                for i in range(1, len(iv_list)):
                    if iv_list[i] < lower or iv_list[i] > upper:
                        flag = False
                        break
            if flag:
                sol = cut
                max_iv = iv
    return sol


def calc_all_information(ks_points, good_bad, sol):
    result, old = [], [0, 0]
    for t in range(len(sol)):
        c = sol[t]
        if t == 0:
            bin_name = pd.Interval(left=float('-inf'), right=ks_points[c][0])
        else:
            bin_name = pd.Interval(left=ks_points[sol[t - 1]][0], right=ks_points[c][0])
        gd_cum, bd_cum = ks_points[c][-2], ks_points[c][-1]
        gd, bd = gd_cum - old[0], bd_cum - old[1]
        total = gd + bd
        bad_rate = bd / total if total > 0 else 0.0
        old = (ks_points[c][-2], ks_points[c][-1])
        result.append([bin_name, total, gd, bd, round(bad_rate, 6)])
    bin_name = pd.Interval(left=ks_points[sol[-1]][0], right=float('inf'))
    gd_cum, bd_cum = float(good_bad[0]), float(good_bad[1])
    gd, bd = gd_cum - old[0], bd_cum - old[1]
    total = gd + bd
    bad_rate = bd / total if total > 0 else 1.0
    result.append([bin_name, total, bd, gd, round(bad_rate, 6)])
    return result


def best_chisq_bin(group, bc_piece, bc_good_bad, bc_gap, bc_strict_monotonicity,
                   bc_iv_lower, bc_iv_upper, merge):
    feat_name = group[0][0]
    good = bc_good_bad[0]
    bad = bc_good_bad[1]
    bad_rate = 1.0 * bad / (bad + good)
    group = sorted(group, key=lambda x: x[1])
    counter = [1.0, 0.0] if group[0][-1] == 0 else [0.0, 1.0]

    ks_points = [(feat_name, counter[0], counter[1])]
    for j in range(1, len(group)):
        if group[j][1] != group[j - 1][1]:
            ks_points.append((group[j - 1][1], counter[0], counter[1]))
        counter[0 if group[j][-1] == 0 else 1] += 1
    if group[-1][1] != ks_points[-1][0]:
        ks_points.append((group[-1][1], counter[0], counter[1]))

    if merge:
        ks_points = sub_chisq(ks_points, 0, len(ks_points) - 1, bc_gap, bad_rate)
        ks_points = sorted(ks_points, key=lambda x: x[0])
        sub_piece = bc_piece
    else:
        sub_piece = len(ks_points) - 1
        ks_points = ks_points[1:-1]

    can_be_bin = False
    for tmp_piece in range(sub_piece - 1):
        sol = best_combine(ks_points, bc_good_bad, sub_piece - tmp_piece,
                           bc_strict_monotonicity, bc_iv_lower, bc_iv_upper)
        if sol:
            can_be_bin = True
            result = calc_all_information(ks_points, bc_good_bad, sol)
            break
    if not can_be_bin:
        print("不能对字段{}进行分箱".format(feat_name))
        return None
    return pd.DataFrame(result, columns=['bin_range', 'bin_total', 'bin_bad', 'bin_good', 'bin_bad_rate'])
