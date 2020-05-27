from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools.tools import add_constant
from scipy import stats
from sklearn import linear_model
import pandas as pd
import numpy as np
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)


def calculate_partial_correlation(input_df, column1, column2):
    """
    Returns linear partial correlation coefficients
    between pairs of variables,
    controlling all the other variables

    Parameters
    ----------
    input_df : pandas.DataFrame, shape (n, p)
        Array with candidate variables. Each column is taken as a variable.

    Returns
    -------
    P :  partial correlation of input_df[:, column1] and input_df[:, column2]
        controlling for all other remaining variables.
    """
    if column1 == column2:
        return 1
    control_variables = input_df.columns.tolist()
    control_variables.remove(column1)
    control_variables.revove(column2)
    data_control_variable = input_df.loc[:, control_variables]
    data_column1 = input_df[column1].values
    data_column2 = input_df[column2].values
    fit1 = linear_model.LinearRegression(fit_intercept=True)
    fit2 = linear_model.LinearRegression(fit_intercept=True)
    fit1.fit(data_control_variable, data_column1)
    fit2.fit(data_control_variable, data_column2)
    residual1 = data_column1 - (
            np.dot(data_control_variable, fit1.coef_) + fit1.intercept_)
    residual2 = data_column2 - (
            np.dot(data_control_variable, fit2.coef_) + fit2.intercept_)
    return stats.pearsonr(residual1, residual2)[0]


def select_variables_univariante(df, candidate_features_iv, corr_threshold=0.8, partial=True):
    """perform feature selection based on pairwise correlation coefficient
        and remove the one with smaller iv if correlation coefficient > corr_threshold
    :param df: pandas.DataFrame, with all the features transformed by woe
    :param candidate_features_iv: pd.Series with iv values for candidate features
    :param corr_threshold: threshold of correlation coefficient bigger than which
        a pair of features is considered to be correlated
    :param partial: bool, whether to use partial correlation
    :return: list of selected features
    """
    candidate_features_iv.sort_values(ascending=False, inplace=True)
    deleted_index = []
    cnt_num = len(candidate_features_iv)
    for i in range(cnt_num):
        if i in deleted_index:
            continue
        x1 = candidate_features_iv.index[i]
        for j in range(cnt_num):
            if i == j or j in deleted_index:
                continue
            y1 = candidate_features_iv.index[j]
            if partial:
                roh = calculate_partial_correlation(
                    df[candidate_features_iv.index.tolist()], x1, y1)
            else:
                roh = np.corrcoef(df[x1], df[y1])[0, 1]
            if abs(roh) > corr_threshold:
                x1_iv = candidate_features_iv[x1]
                y1_iv = candidate_features_iv[y1]
                if x1_iv > y1_iv:
                    deleted_index.append(j)
                else:
                    deleted_index.append(i)
    single_analysis_vars = [candidate_features_iv.index[i] for i
                            in range(cnt_num) if i not in deleted_index]
    return single_analysis_vars


def select_variables_multivariant_forward(x, y,
                                          candidate_features=[],
                                          initial_list=[],
                                          threshold_in=0.05,
                                          check_positive_coef=True,
                                          verbose=True):
    """ Perform a forward feature selection for logistic regression
    Arguments:
        candidate_features - list of the names the candidate features
        x - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of x)
        threshold_in - include a feature if its p-value < threshold_in
        check_positive_coef - whether to make sure the coefficients are all positive
              if True, all the features should be transformed by woe
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features
    """
    if len(candidate_features) == 0:
        candidate_features = x.columns.tolist()

    included = initial_list

    # selection begins
    count = 1
    best_llr_pvalue = 10000
    while True:
        if verbose:
            print('Iteration {}'.format(count))

        count += 1

        # forward step
        excluded = list(set(candidate_features)-set(included))
        new_coef_list = []
        new_pval_list = []
        new_llr_pvalue_list = []
        new_prsquared_list = []
        new_features_list = []
        for new_column in excluded:
            model = Logit(y, add_constant(x.loc[:, included+[new_column]])).fit()
            coefficients = model.params
            pvalues = model.pvalues
            llr_pvalue = model.llr_pvalue
            prsquared = model.prsquared
            if np.isnan(pvalues.iloc[-1]):
                if verbose:
                    print('{}: bad fit'.format(new_column))
                continue
            if (check_positive_coef and (coefficients.iloc[1:] > 0).all()) \
                    or (not check_positive_coef):
                new_features_list.append(new_column)
                new_coef_list.append(coefficients)
                new_pval_list.append(pvalues)
                new_llr_pvalue_list.append(llr_pvalue)
                new_prsquared_list.append(prsquared)
        if len(new_pval_list) == 0:
            if verbose:
                print('positive coefficients can not be guaranteed')
            break
        # the same length as new_pval_list
        new_pval_array = np.array([i.iloc[-1] for i in new_pval_list])
        # so best_pval_idx is the index into new_pval_list
        best_pval_idx = new_pval_array.argmin()
        best_pval = new_pval_array[best_pval_idx]
        if best_pval < threshold_in:
            llr_pvalue = new_llr_pvalue_list[best_pval_idx]
            if (llr_pvalue < threshold_in) or (llr_pvalue <= best_llr_pvalue):
                best_llr_pvalue = min(llr_pvalue, best_llr_pvalue)
                best_feature = new_features_list[best_pval_idx]
                included.append(best_feature)
                if verbose:
                    best_prsquared = new_prsquared_list[best_pval_idx]
                    best_coefficients = new_coef_list[best_pval_idx]
                    best_pvalues = new_pval_list[best_pval_idx]
                    display_df = pd.DataFrame(columns=['coefficients', 'pvalue',
                                                       'llr_pvalue', 'pseudoR2'],
                                              index=best_coefficients.index)
                    display_df.loc[:, 'coefficients'] = best_coefficients.values
                    display_df.loc[:, 'pvalue'] = best_pvalues.values
                    display_df.iloc[0, -2] = best_llr_pvalue
                    display_df.iloc[0, -1] = best_prsquared
                    print('Add ', best_feature)
                    print(display_df)
            else:
                if verbose:
                    print('overall fitting is not significant or improving')
                break
        else:
            if verbose:
                print('coefficient of univariant is not significant')
            break

    return included


def select_variables_multivariant_backward(x, y,
                                           candidate_features=[],
                                           threshold_in=0.05,
                                           check_positive_coef=True,
                                           verbose=True):
    """ Perform a backward feature selection for logistic regression
    Arguments:
        candidate_features - list of the names the candidate features
        x - pandas.DataFrame with candidate features
        y - list-like with the target
        threshold_in - include a feature if its p-value < threshold_in
        check_positive_coef - whether to make sure the coefficients are all positive
              if True, all the features should be transformed by woe
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features
    """
    if len(candidate_features) == 0:
        candidate_features = x.columns.tolist()

    # selection begins
    count = 1
    best_llr_pvalue = 10000
    excluded = []
    included = list(set(candidate_features))
    while True:
        if verbose:
            print('Iteration {}'.format(count))

        count += 1

        # backward step
        for col in excluded:
            included.remove(col)
        model = Logit(y, add_constant(x.loc[:, included])).fit()
        coefficients = model.params
        pvalues = model.pvalues
        llr_pvalue = model.llr_pvalue
        prsquared = model.prsquared
        if verbose:
            display_df = pd.DataFrame(columns=['coefficients', 'pvalue',
                                               'llr_pvalue', 'pseudoR2'],
                                      index=coefficients.index)
            display_df.loc[:, 'coefficients'] = coefficients.values
            display_df.loc[:, 'pvalue'] = pvalues.values
            display_df.iloc[0, -2] = llr_pvalue
            display_df.iloc[0, -1] = prsquared
            print(display_df)
        if (llr_pvalue < threshold_in) or (llr_pvalue <= best_llr_pvalue):
            new_pval_array = pvalues.values[1:]
            worst_pval_idx = new_pval_array.argmax()
            worst_pval = new_pval_array[worst_pval_idx]
            worst_feature = included[worst_pval_idx]
            best_llr_pvalue = min(best_llr_pvalue, llr_pvalue)
            if worst_pval > threshold_in:
                excluded.append(worst_feature)
                if verbose:
                    print('Pop ', worst_feature)

            else:
                if verbose:
                    print('every univariant is significant')
                break
        else:
            if verbose:
                print('overall fitting significance is no longer improving')
            break

    return included


if __name__ == '__main__':
    pdf = pd.read_excel('lr_test_data.xlsx', encoding='utf-8')
    x_train = pdf.iloc[:, :-1]
    y_train = pdf.iloc[:, -1]
    # included_features = select_variables_multivariant_forward(x_train, y_train, check_positive_coef=False)
    included_features = select_variables_multivariant_backward(x_train, y_train)
    print('included_fetures', included_features)


