import os
import numpy as np
import pandas as pd
import json

from copy import deepcopy
import subprocess
from joblib import Parallel, delayed
import multiprocessing

import tensorflow as tf
from keras import backend as K
from keras.models import model_from_json
import abstention as ab
import abstention
from abstention.abstention import AuPrcAbstentionEval
from abstention.abstention import MarginalDeltaAuPrc

from collections import namedtuple
from collections import OrderedDict
from collections import defaultdict
from matplotlib import pyplot as plt

import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser(
        description='Deeplift sarkany model. Results are stored in .npy files and optionally in bigwig files.')

    parser.add_argument("--modeldir", type=str, help="model output directories from tf-dragonn/sarkany.")
    parser.add_argument("--valid-file", type=str, help="valid file")
    parser.add_argument("--test-file", type=str, help="test file")
    parser.add_argument("--summit-file", type=str, help="summit file")
    parser.add_argument("--task-idx", type=int, default=0, help="task_idx. Default: 512.")
    parser.add_argument("--perf-out-file", type=str, help="output file to write performance after eviction")
    parser.add_argument("--summit-out-file", type=str, help="output file of calibrated predictions")
    parser.add_argument("--test-out-file", type=str, help="output file of calibrated predictions")
    parser.add_argument("--valid-out-file", type=str, help="output file of validation data")
    parser.add_argument("--visiblegpus", type=str, help="visiblegpus")

    args = parser.parse_args()
    return args


def get_logger():
    log_formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s] %(message)s')
    logger = logging.getLogger('run-deeplift')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(log_formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger

def setup_keras_session(visiblegpus):
    os.environ['CUDA_VISIBLE_DEVICES'] = str(visiblegpus)
    session_config = tf.ConfigProto()
    session = tf.Session(config=session_config)
    K.set_session(session)

    return None


def get_keras_models(modeldir, visiblegpus):
    #modeldir = "{}/full_mouse/fineFactorized/task_{}-naivegw".format(root, task_idx)
    weightfile = "{0}/{1}".format(modeldir, "model.weights.h5")
    archfile = "{0}/{1}".format(modeldir, "model.arch.json")
    setup_keras_session(int(visiblegpus))
    json_pointer = open(archfile, 'r')
    loaded_json_string = json_pointer.read()
    json_pointer.close()
    keras_model = model_from_json(loaded_json_string)
    keras_model.load_weights(weightfile)

    return keras_model


def get_onehot(data, intervals=[], onehot_data=None):
    from genomelake.extractors import ArrayExtractor
    import pybedtools
    extractor = ArrayExtractor('/oak/stanford/groups/akundaje/msharmin/genomelake_data/mm10_no_alt_analysis_set_ENCODE.fasta/')
    seqids = list(data.index)
    for seqid in seqids:
        interval = pybedtools.create_interval_from_list(list(data.loc[seqid, :3]))
        intervals.append(interval)
    onehot_data = extractor(intervals)

    return onehot_data

def batch_iter(iterable, batch_size):
    it = iter(iterable)
    try:
        while True:
            values = []
            for n in range(batch_size):
                values += (next(it),)
            yield values
    except StopIteration:
        yield values


def generate_onehots(data, batch_size=256):
    from genomelake.extractors import ArrayExtractor
    import pybedtools

    bt = pybedtools.bedtool.BedTool.from_dataframe(data)
    extractor = ArrayExtractor('/oak/stanford/groups/akundaje/msharmin/genomelake_data/mm10_no_alt_analysis_set_ENCODE.fasta/')
    intervals_generator = batch_iter(bt, batch_size)
    for intervals_batch in intervals_generator:
        inputs = extractor(intervals_batch)
        yield inputs

def get_preacts(preact_func, data):
    iterator = generate_onehots(data.loc[:, :2])
    data_preacts = None
    for batch_indx, batch in enumerate(iterator):
        tmp_preacts = np.array(preact_func(data=batch, learning_phase=0, batch_size=256))
        if(data_preacts is None):
            data_preacts = tmp_preacts
        else:
            data_preacts = np.hstack((data_preacts, tmp_preacts))

    return data_preacts

from sklearn.metrics import precision_recall_curve, auc

def get_accuracy_threshold(labels, pred_values, fdr_cut_off=0.5):

    precision, recall, thresholds = precision_recall_curve(labels, pred_values)

    fdr = 1-precision
    index_for_fdrK = min(np.argwhere(~np.array(fdr >= fdr_cut_off)))-1 #max(np.argwhere(fdr >= fdr_cut_off))
    threshold_for_accuracy = thresholds[index_for_fdrK]

    area = auc(recall, precision)
    return threshold_for_accuracy, recall[index_for_fdrK], area


def abstention_pipeline():
    args = parse_args()
    logger = get_logger()

    if(os.path.exists(args.perf_out_file)):
        os.remove(args.perf_out_file)
    with open(args.perf_out_file, 'w') as fp:
        fp.write("task_idx\tcalibrated_threshold\tcalibrated_recall\tauprc\tcalibrated_marginal_auprc\tcorrect_peaks\tcorrect_nonpeaks\t")
        fp.write("incorrect_peaks\tincorrect_nonpeaks\ttotal_summits\tcorrect_summits\tincorrect_summits\tpercentage_of_correct_summits\t")
        #fp.write("unified_threshold\tunified_recall\tcorrect_unifieds\tcorrect_nonunifieds\tincorrect_unifieds\tincorrect_nonunifieds\t")
        #fp.write("ensembl_threshold\tensembl_recall\tcorrect_ensembls\tcorrect_nonensembls\tincorrect_ensembls\tincorrect_nonensembls")
        fp.write("\n")

    logger.info("loading model...")
    model = get_keras_models(args.modeldir, args.visiblegpus)
    valid_data = pd.read_table(args.valid_file, header=None)
    valid_data = valid_data.sort_values(by=[0, 1])
    valid_data.index = range(valid_data.shape[0])
    test_data = pd.read_table(args.test_file, header=None)
    test_data = test_data.sort_values(by=[0, 1])
    test_data.index = range(test_data.shape[0])

    logger.info("calculating preactivations...")
    preact_func = ab.util.get_preact_func(model=model, task_idx=0)
    valid_preacts = get_preacts(preact_func, valid_data)
    test_preacts = get_preacts(preact_func, test_data)

    cb_method_name_to_factory = OrderedDict([
        #Expit is just the sigmoid; no calibration
        ("uncalibrated_posterior", ab.calibration.Expit()),
        ("platt_calibrated_posterior", ab.calibration.PlattScaling())
    ])
    cb_method_name_to_cb_func = OrderedDict()
    for cb_method_name, cb_factory in cb_method_name_to_factory.items():
        cb_method_name_to_cb_func[cb_method_name] = cb_factory(valid_preacts=valid_preacts,
                                                           valid_labels=np.array(valid_data[3]))
    cb_method_name_to_valid_posterior_prob = OrderedDict()
    cb_method_name_to_test_posterior_prob = OrderedDict()
    for cb_method_name, cb_func in cb_method_name_to_cb_func.items():
        cb_method_name_to_valid_posterior_prob[cb_method_name] = cb_func(valid_preacts)
        cb_method_name_to_test_posterior_prob[cb_method_name] = cb_func(test_preacts)

    AbstentionFuncInfo = namedtuple('AbstentionFuncInfo', ('method_name', 'factory', 'posterior', 'uncert'))
    evaluation_functions = OrderedDict([('auPRC_0.95',AuPrcAbstentionEval(0.95)),
                                    ('auPRC_0.8',AuPrcAbstentionEval(0.8))])

    abstention_func_infos = [AbstentionFuncInfo(method_name='calibrated_marginal_auprc',
                            factory=MarginalDeltaAuPrc(), posterior='platt_calibrated_posterior', uncert=None)]

    metric_to_method_name_to_test_perfs = OrderedDict()
    for metric_name in evaluation_functions:
        method_name_to_test_perfs = OrderedDict([
            (abstention_func.method_name, []) for abstention_func in abstention_func_infos])
        metric_to_method_name_to_test_perfs[metric_name] = method_name_to_test_perfs

    for abstention_func_info in abstention_func_infos:
        logger.info("\nCalling method: {}".format(abstention_func_info.method_name))

        factory = abstention_func_info.factory
        posterior_name = abstention_func_info.posterior
        uncert_name = abstention_func_info.uncert

        valid_posterior = cb_method_name_to_valid_posterior_prob[posterior_name]
        test_posterior = cb_method_name_to_test_posterior_prob[posterior_name]
        valid_uncert = transform_name_to_valid_uncert[uncert_name] if uncert_name else None
        test_uncert = transform_name_to_test_uncert[uncert_name] if uncert_name else None

        #The abstention factor takes the validation labels, probabilities
        #and uncertainty estimates (some of these may be None depending on the method)
        #and returns abstention_func, which accepts the test probabilities
        #and uncertainties and returns abstention priority scores
        #(higher scores are evicted sooner)
        abstention_func = factory(valid_labels=np.array(valid_data[3]),
                              valid_posterior=valid_posterior,
                              valid_uncert=valid_uncert)
        test_abstention_scores = abstention_func(posterior_probs=test_posterior,
                                             uncertainties=test_uncert)

        for evaluation_func_name, evaluation_func in evaluation_functions.items():
            test_perf = evaluation_func(abstention_scores=test_abstention_scores,
                                    y_true=np.array(test_data[3]), y_score=test_posterior)
            metric_to_method_name_to_test_perfs[evaluation_func_name]\
                                      [abstention_func_info.method_name].append(test_perf)

    for metric_name in ["auPRC_0.8", "auPRC_0.95"]:
        logger.info("\nBest "+metric_name+" methods - test")
        metric_to_test_score = defaultdict(lambda: 0)
        metric_name_ranks = sorted(
                metric_to_method_name_to_test_perfs[metric_name].keys(),
                key=lambda x: -metric_to_method_name_to_test_perfs[metric_name][x][0])
        for idx, name in enumerate(metric_name_ranks):
            metric_to_test_score[name] += idx
            logger.info(metric_name+" ranks:")
            logger.info("\n".join(str(x[0])+":\n\t"+metric_name+": "
                    +str(np.mean(metric_to_method_name_to_test_perfs[metric_name][x[0]]))
                    +", rank: "+str(len(metric_to_test_score)-x[1])
                    for x in sorted(metric_to_test_score.items(), key=lambda x: x[1])))

    calibrated_test_preds = cb_method_name_to_test_posterior_prob["platt_calibrated_posterior"]
    uncalibrated_test_preds = cb_method_name_to_test_posterior_prob["uncalibrated_posterior"]
    test_data[4] = uncalibrated_test_preds
    test_data[5] = test_preacts
    test_data[6] = calibrated_test_preds
    test_data[7] = test_abstention_scores
    test_data.to_csv(args.test_out_file, sep='\t', header=False, index=False, compression='gzip')

    valid_data[4] = valid_preacts
    valid_data.to_csv(args.valid_out_file, sep='\t', header=False, index=False, compression='gzip')

    calibrated_threshold, calibrated_recall, auPRC = get_accuracy_threshold(np.array(test_data[3]), calibrated_test_preds)
    correct_peaks = sum(np.logical_and(calibrated_test_preds > calibrated_threshold, np.array(test_data[3])==1))
    incorrect_peaks = sum(np.logical_and(calibrated_test_preds <= calibrated_threshold, np.array(test_data[3])==1))
    correct_nonpeaks = sum(np.logical_and(calibrated_test_preds > calibrated_threshold, np.array(test_data[3])==0))
    incorrect_nonpeaks = sum(np.logical_and(calibrated_test_preds <= calibrated_threshold, np.array(test_data[3])==0))

    with open(args.perf_out_file, 'a') as fp:
        fp.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(args.task_idx, calibrated_threshold[0], calibrated_recall[0], auPRC,
                                str(np.mean(metric_to_method_name_to_test_perfs["auPRC_0.95"]["calibrated_marginal_auprc"][0])),
                                correct_peaks, correct_nonpeaks, incorrect_peaks, incorrect_nonpeaks))
        logger.info("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(args.task_idx, calibrated_threshold[0], calibrated_recall[0],
                                str(np.mean(metric_to_method_name_to_test_perfs["auPRC_0.95"]["calibrated_marginal_auprc"][0])),
                                correct_peaks, correct_nonpeaks, incorrect_peaks, incorrect_nonpeaks))

    logger.info("generating summit calibrated data...")
    summit_data = pd.read_table(args.summit_file, header=None)
    summit_preacts = get_preacts(preact_func, summit_data)
    calibrated_summit_preds = cb_method_name_to_cb_func["platt_calibrated_posterior"](summit_preacts)
    uncalibrated_summit_preds = cb_method_name_to_cb_func["uncalibrated_posterior"](summit_preacts)
    summit_abstention_scores = abstention_func(posterior_probs=calibrated_summit_preds, uncertainties=None)
    summit_data[3] = uncalibrated_summit_preds
    summit_data[4] = summit_preacts
    summit_data[5] = calibrated_summit_preds
    summit_data[6] = summit_abstention_scores
    summit_data.to_csv(args.summit_out_file, sep='\t', header=False, index=False, compression='gzip')
    correct_peaks = sum(calibrated_summit_preds > calibrated_threshold)
    percentage_of_correct_peaks = correct_peaks/(1.0*len(calibrated_summit_preds))
    with open(args.perf_out_file, 'a') as fp:
        fp.write("\t{}\t{}\t{}\t{}".format(len(calibrated_summit_preds), correct_peaks,
                                        len(calibrated_summit_preds) - correct_peaks,
                                        percentage_of_correct_peaks))

        logger.info("\t{}\t{}\t{}\t{}".format(len(calibrated_summit_preds), correct_peaks,
                                        len(calibrated_summit_preds) - correct_peaks,
                                        percentage_of_correct_peaks))
    return None

abstention_pipeline()

