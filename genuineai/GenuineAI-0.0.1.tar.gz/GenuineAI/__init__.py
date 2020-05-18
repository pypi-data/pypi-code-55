#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geniune AI functions
Related to the iMICS lab research projects

@author: Ernest Namdar  ernest.namdar@utoronto.ca
"""
import random
import pandas as pd
import numpy as np
import sys
# to compare
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from scipy.integrate import trapz


def AUCPlus(act, pr):
    if type(act) != list:
        print("Actual values should be fed as a list")
        sys.exit(0)
    if type(pr) != list:
        print("Predicted values should be fed as a list")
        sys.exit(0)
    if len(pr) != len(act):
        print("Actual and predicted values have differebnt sizes.")
        sys.exit(0)
    batch_size = len(pr)
    dframe = pd.DataFrame(data=list(zip(act, pr)),
                          columns=["Actual", "Predicted"])
    # Separating actual positives and actual negatives
    a_pos_list = []  # actual positives (index)
    a_neg_list = []  # actual negatives (index)
    for i in range(batch_size):
        if dframe.iloc[i, 0] == 1:
            a_pos_list.append(i)
        else:
            a_neg_list.append(i)
    if a_pos_list == []:
        print("Fatal Error: No Actual Positives")
        sys.exit(0)
    if a_neg_list == []:
        print("Fatal Error: No Actual Negatives")
        sys.exit(0)
    a_pos = dframe.iloc[a_pos_list]  # actual positives
    a_neg = dframe.iloc[a_neg_list]  # actual negatives

    a_pos = a_pos.sort_values(by=["Predicted"])  # sorted AP
    a_neg = a_neg.sort_values(by=["Predicted"])  # sorted AN

    t = []  # thresholds
    t.append(0)  # zero and one are added separately
    # adding sorted predicted vcalues as thresholds
    sorted_dframe = dframe.sort_values(by=["Predicted"])
    sorted_dframe = sorted_dframe.reset_index(drop=True)
    for i in range(batch_size):
        t.append(sorted_dframe.iloc[i, 1])
    t.append(1)  # zero and one are added separately

    tp_list = []
    tn_list = []
    fp_list = []
    fn_list = []
    tpr_list = []
    fpr_list = []
    specifity_list = []
    precision_list = []
    accuracy_list = []
    f1_list = []
    for threshold in reversed(t):  # lowest t, highest tpr and fpr
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        predict = None
        for i in range(batch_size):
            if threshold == 0:
                predict = 1
            elif threshold == 1:
                predict = 0
            elif pr[i] > threshold:
                predict = 1
            else:
                predict = 0
            if predict == 1 and act[i] == 1:
                tp += 1
            elif predict == 0 and act[i] == 0:
                tn += 1
            elif predict == 1 and act[i] == 0:
                fp += 1
            elif predict == 0 and act[i] == 1:
                fn += 1
        if tp+tn+fp+fn != batch_size:
            print("Structural Error")
            sys.exit(0)
        tp_list.append(tp)
        tn_list.append(tn)
        fp_list.append(fp)
        fn_list.append(fn)
        tpr_list.append(tp/(tp+fn))
        fpr_list.append(fp/(fp+tn))
        specifity_list.append(1-(fp/(fp+tn)))
        try:
            precision_list.append(tp/(tp+fp))
        except ZeroDivisionError:
            precision_list.append("NaN")
        try:
            accuracy_list.append((tp+tn)/(tp+tn+fp+fn))
        except ZeroDivisionError:
            accuracy_list.append("NaN")
        try:
            f1_list.append(2*tp/(2*tp+fp+fn))
        except ZeroDivisionError:
            f1_list.append("NaN")
    paramframe = pd.DataFrame(data=list(zip(reversed(t),
                                            tp_list,
                                            tn_list,
                                            fp_list,
                                            fn_list,
                                            tpr_list,
                                            fpr_list,
                                            tpr_list,
                                            specifity_list,
                                            tpr_list,
                                            accuracy_list,
                                            precision_list,
                                            f1_list)),
                              columns=["Threshold",
                                       "True Positive",
                                       "True Negative",
                                       "False Positive",
                                       "False Negative",
                                       "True Positive Rate",
                                       "False Positive Rate",
                                       "Sensitivity",
                                       "Specificity",
                                       "Recall",
                                       "Accuracy",
                                       "Precision",
                                       "F1 Score"])

    # integration of ROC (==AUC) using trapezoid method(great for this case)
    integration = 0
    if act == pr:  # in this case we only have (0,0) and (1,1) integration=0.5!
        integration = 1
    else:
        for i in range(batch_size+1):
            integration += 0.5 * (tpr_list[i]+tpr_list[i+1]) * \
                           (fpr_list[i+1]-fpr_list[i])
#    # to prove that ROC is always staircase looking
#    # it will fail if predicted = 0 or predicted = 1 exists
#    integration2 = 0
#    for i in range(batch_size+1):
#        integration2 += tpr_list[i+1] * \
#                       (fpr_list[i+1]-fpr_list[i])
#    integration3 = 0
#    for i in range(batch_size+1):
#        integration3 += tpr_list[i] * \
#                       (fpr_list[i+1]-fpr_list[i])
#    if (integration != integration2) or (integration != integration3):
#        print("ROC is not staircase-looking!")
#        sys.exit(0)

    # (confidence) eddited AUC
    max_a_neg = a_neg.iloc[a_neg.shape[0]-1, 1]
    max_a_pos = a_pos.iloc[a_pos.shape[0]-1, 1]
    min_a_neg = a_neg.iloc[0, 1]
    min_a_pos = a_pos.iloc[0, 1]
    alpha = max_a_pos - min_a_neg
    beta = min_a_pos - max_a_neg
    kauc = np.exp(beta-1) * np.exp(alpha-1) * integration
    return tpr_list, fpr_list, integration, kauc, paramframe


name = "GeniuneAI"
