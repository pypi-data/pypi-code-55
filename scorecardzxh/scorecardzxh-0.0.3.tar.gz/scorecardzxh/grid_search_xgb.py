import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import GridSearchCV, PredefinedSplit, cross_val_score
from sklearn.metrics import f1_score, accuracy_score, roc_auc_score
from bayes_opt import BayesianOptimization
import warnings
warnings.filterwarnings('ignore')


class GridSearchXGB(object):
    def __init__(self, alg):
        """
        :param alg: XGBClassifier object
          please note that the alg that is used to initialize the class instance will be changed
          after gridsearch because python uses reference of address like that in C++
        """
        self._alg = alg

    def get_params(self):
        return self._alg.get_params()

    def set_params(self, **setting_params):
        self._alg.set_params(**setting_params)

    def predict(self, x):
        """
        :param x: array-like(dim=2), Feature matrix
        """
        # np.array
        # defaults to best_ntree_limit if early stopping is available,
        # otherwise 0 (use all trees).
        prediction = self._alg.predict(x)
        return prediction

    def predict_proba(self, x):
        """
        :param x: array-like(dim=2), Feature matrix
        """
        # np.array
        # defaults to best_ntree_limit if early stopping is available,
        # otherwise 0 (use all trees).
        prediction = self._alg.predict_proba(x)
        return prediction

    def predict_proba_with_best_threshold(self, x, y, metric_list=['f1']):
        """
        tune threshold with best threshold
        :param x: array-like(dim=2), Feature matrix
        :param y: array-like(dim=1), Label
        :param metric_list: a list of metrics
        """
        max_score_list = []
        best_t_list = []
        for metric in metric_list:
            assert metric in ['f1', 'accuracy', 'roc_auc']
            max_score_list.append([metric, -1])
            best_t_list.append([metric, -1])
        y_prediction = self.predict_proba(x)[:, 1]
        for t in np.arange(0, 1, 0.05):
            y_hat = np.zeros_like(y_prediction)
            y_hat[y_prediction >= t] = 1
            for i in range(len(metric_list)):
                max_score = max_score_list[i][1]
                metric = max_score_list[i][0]
                if metric == 'f1':
                    score = f1_score(y, y_hat)
                elif metric == 'accuracy':
                    score = accuracy_score(y, y_hat)
                elif metric == 'roc_auc':
                    score = roc_auc_score(y, y_hat)
                else:
                    raise RuntimeError('not-supported metric: {}'.format(metric))
                if score > max_score:
                    max_score_list[i][1] = score
                    best_t_list[i][1] = t

        return y_prediction, max_score_list, best_t_list

    def fit(self, x_train, y_train, param_dict=None):
        if param_dict is not None:
            self._alg = XGBClassifier(**param_dict)
        self._alg.fit(x_train, y_train)

    def _custom_f1_score(self, y_pred, y_true_dmatrix):
        """
        the signature is func(y_predicted, DMatrix_y_true) where DMatrix_y_true is
        a DMatrix object such that you may need to call the get_label method.
        It must return a (str, value) pair where the str is a name for the evaluation
        and value is the value of the evaluation function.
        The callable function is always minimized.
        :param y_pred: np.array, probability score predicted by the xgbclassifier
        :param y_true_dmatrix: xgb DMatrix, true label, with positive instances as 1
        """
        y_true = y_true_dmatrix.get_label()
        y_hat = np.zeros_like(y_pred)
        y_hat[y_pred >= self._alg.get_params()['base_score']] = 1
        f1 = f1_score(y_true, y_hat)
        return 'f1_err', 1 - f1

    def _regularize_metric(self, eval_metric, early_stopping_rounds):
        """
        :param eval_metric: list of str, each str should be a built-in metric of sklearn
        :param early_stopping_rounds: int or None
        """
        feval = None
        eval_metric_list = []
        for metric in eval_metric:
            if early_stopping_rounds is not None:
                if metric == 'f1':
                    # when this happens, feval will always be used for early stopping.
                    # For custom function, the smaller the returned value the better,
                    # but for built in metrics, the cv package will automatically decide
                    # according to the metric type, e.g., the smaller the better for error
                    # but the bigger the better for auc, etc.
                    feval = self._custom_f1_score
                elif metric == 'accuracy':
                    # It is calculated as #(wrong cases)/#(all cases).
                    # The evaluation will regard the instances
                    # with prediction value larger than 0.5 as positive instances, i.e., 1 instances)
                    eval_metric_list.append('error')
                elif metric == 'roc_auc':
                    eval_metric_list.append('auc')
                else:
                    raise RuntimeError('not-supported metric: {}'.format(metric))
            else:
                if metric in ['f1', 'accuracy', 'roc_auc']:
                    eval_metric_list.append(metric)
                else:
                    raise RuntimeError('not-supported metric: {}'.format(metric))
        return feval, eval_metric_list

    def _regularize_xgb_params(self, **params_to_optimize):
        regularized_dict = {}
        for key, value in self._alg.get_params().items():
            if key in params_to_optimize.keys():
                if key in ['max_depth', 'n_estimators', 'min_child_weight',
                           'max_delta_step', 'num_parallel_tree']:
                    regularized_dict[key] = int(params_to_optimize[key])
                else:
                    regularized_dict[key] = params_to_optimize[key]
            else:
                regularized_dict[key] = value
        return regularized_dict

    def _make_train_val(self, x_train, y_train, eval_set, cv):
        """
        :param x_train: array-like(dim=2), Feature matrix
        :param y_train: array-like(dim=1), Label
        :param eval_set: a list of (X, y) tuples, only one tuple is supported as of now
        :param cv: int, number of folds for cross_validation
        """
        if eval_set is not None:
            print('using self-defined eval-set')
            assert len(eval_set) == 1
            if type(x_train) is pd.core.frame.DataFrame:
                x_train_val = pd.concat([x_train, eval_set[0][0]], axis=0)
                y_train_val = pd.concat([y_train, eval_set[0][1]], axis=0)
            else:
                x_train_val = np.concatenate((x_train, eval_set[0][0]), axis=0)
                y_train_val = np.concatenate((y_train, eval_set[0][1]), axis=0)
            # initialize all indices to 0 except the section of training
            # to -1, which means this part will not be in validation.
            # So only one fold is made
            test_fold = np.zeros(x_train_val.shape[0])
            test_fold[:x_train.shape[0]] = -1
            cv = PredefinedSplit(test_fold=test_fold)
            folds = []
            for train_indices_array, val_indices_array in cv.split():
                folds.append((train_indices_array.tolist(),
                              val_indices_array.tolist()))
        else:
            print('using cv {}'.format(cv))
            x_train_val = x_train
            y_train_val = y_train
            folds = None
        return x_train_val, y_train_val, cv, folds

    def search_with_bayesian(self, x_train, y_train, tuning_dict,
                             eval_set=None, eval_metric=['f1'], cv=3, verbose=True,
                             init_points=5, n_iter=25, acq='ucb', kappa=2.576, xi=0.0, **gp_params):
        """
        :param x_train: array-like(dim=2), Feature matrix
        :param y_train: array-like(dim=1), Label
        :param tuning_dict: dict with keys being params in XGBClassifier,
         and values being a list of lowerbound and upperbound
        :param eval_set: a list of (X, y) tuples, only one tuple is supported as of now
        :param eval_metric: a list of str
         str should be a built-in evaluation metric of sklearn, but only the last will be used
        :param cv: int, number of folds for cross_validation
        :param verbose: bool
        :param init_points: int, number of initial points for bayesian optimization
        :param n_iter: int, number of other points for bayesian optimization besides init_points
        :param acq: 'str', acquisition function used in exporation stage of bayesian,
          must be in ['ucb', 'ei', 'poi']
        :param kappa: param used in acquisition function. As of 'ucb' function, for example,
          the bigger kappas is, the more likely our bayesian is gonna search the unknown spaces
        :param xi: param used in acquisition function
        :param gp_params: param used in gaussian process
        """
        feval, eval_metric_list = self._regularize_metric(eval_metric, None)
        x_train_val, y_train_val, cv, _ = self._make_train_val(x_train, y_train, eval_set, cv)

        # use closure to pass in x_train_val and y_train_val, scoring and n_jobs, cv
        # because the params of the objective function can only be the params to optimize
        def rf_cv(**params_to_optimize):
            xgb_param = self._regularize_xgb_params(**params_to_optimize)
            # cross_val_score returns an array with each element being the val score
            # on each fold
            val = cross_val_score(XGBClassifier(**xgb_param),
                                  x_train_val, y_train_val,
                                  scoring=eval_metric_list[-1],
                                  n_jobs=self._alg.get_params()['n_jobs'],
                                  cv=cv).mean()
            return val
        rf_bo = BayesianOptimization(f=rf_cv, pbounds=tuning_dict,
                                     random_state=self._alg.get_params()['random_state'],
                                     verbose=2 if verbose else 0)
        rf_bo.maximize(init_points=init_points, n_iter=n_iter, acq=acq,
                       kappa=kappa, xi=xi, **gp_params)
        optimized_xgb_params = self._regularize_xgb_params(**rf_bo.max['params'])
        # rf_bo.maximize will not get self._alg fitted
        # please note that the alg that is used to initialize the class instance is also changed
        # because python uses reference of address like that in C++
        self._alg.set_params(**optimized_xgb_params)
        print('best tuning: {} with val score {}'.format(rf_bo.max['params'],
                                                         rf_bo.max['target']))
        print('current model: {}'.format(self._alg.get_params()))
        return self._alg.get_params()

    def search(self, x_train, y_train, tuning_dict, eval_set=None, eval_metric=['f1'], cv=3,
               early_stopping_rounds=None, verbose=True):
        """
        :param x_train: array-like(dim=2), Feature matrix
        :param y_train: array-like(dim=1), Labels
        :param tuning_dict: dict with keys being params in XGBClassifier,
         and values being a list of grid point to probe
        :param eval_set: a list of (X, y) tuples, only one tuple is supported as of now
        :param eval_metric: a list of str
         str should be a built-in evaluation metric of sklearn.
        :param cv: int, number of folds for cross_validation
        :param early_stopping_rounds: int, Validation metric needs to improve at least once
         in every 'early_stopping_rounds' round(s) to continue training.
         Note that we use this parameter for the search of best number of estimators so all the other
         parameters will be kept unchanged
         If there’s more than one metric in eval_metric, the last metric will be used for early stopping
        :param verbose: bool, If verbose, prints the evaluation metric measured on the validation set.
        """
        feval, eval_metric_list = self._regularize_metric(eval_metric, early_stopping_rounds)
        if early_stopping_rounds is not None:
            print('warning: only the number of estimators will be increased '
                  'until early stopping criteria'
                  'is met and the tuning grid will not be used')
            x_train_val, y_train_val, cv, folds = self._make_train_val(x_train, y_train, eval_set, cv)
            xgb_dmatrix = xgb.DMatrix(x_train_val, label=y_train_val)
            xgb_param = self._alg.get_xgb_params()
            # when folds is defined in xgb.cv, nfold will not be used
            cvresult = xgb.cv(xgb_param, xgb_dmatrix,
                              num_boost_round=self._alg.get_params()['n_estimators'],
                              nfold=cv,
                              metrics=eval_metric_list,
                              feval=feval,
                              folds=folds,
                              early_stopping_rounds=early_stopping_rounds,
                              verbose_eval=True if verbose else None,
                              seed=self._alg.get_params()['random_state'])
            # returns the best n_estimators
            # please note that the alg that is used to initialize the class instance is also changed
            # because python uses reference of address like that in C++
            self._alg.set_params(n_estimators=cvresult.shape[0])
            print('best n_estimators: {} with val score {}'.format(self._alg.get_params()['n_estimators'],
                                                                   cvresult.iloc[-1, :][-2]))
            print('current model: {}'.format(self._alg.get_params()))
            return self._alg.get_params()
        else:
            x_train_val, y_train_val, cv, _ = self._make_train_val(x_train, y_train, eval_set, cv)
            grid_search_params = {'estimator': self._alg,
                                  'param_grid': tuning_dict,
                                  'scoring': eval_metric_list,
                                  'cv': cv,
                                  'verbose': 2 if verbose else 0,
                                  'refit': eval_metric_list[-1],
                                  'n_jobs': self._alg.get_params()['n_jobs']}
            grsearch = GridSearchCV(**grid_search_params)
            grsearch.fit(x_train_val, y_train_val)
            # after grsearch-fitting, the estimator in GridSearchCV will not get fitted
            # please note that the alg that is used to initialize the class instance is also changed
            # because python uses reference of address like that in C++
            self._alg.set_params(**grsearch.best_params_)
            print('best tuning: {} with val score {}'.format(grsearch.best_params_,
                                                             grsearch.best_score_))
            print('current model: {}'.format(self._alg.get_params()))
            return self._alg.get_params()


def test_tunning_grid():
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    print('preparing data...')
    # 产生随机分类数据集，10个特征， 2个类别
    x, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=2)
    train_cols_list = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
    pdf = pd.DataFrame(x, columns=train_cols_list)
    pdf['label'] = y
    x_train, x_test, y_train, y_test = train_test_split(pdf.loc[:, train_cols_list],
                                                        pdf.loc[:, 'label'],
                                                        random_state=1)
    alg = XGBClassifier(learning_rate=0.1,
                        n_estimators=1000,
                        max_depth=5,
                        min_child_weight=1,
                        gamma=0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        objective='binary:logistic',
                        reg_lambda=1,
                        reg_alpha=0,
                        n_jobs=4,
                        scale_pos_weight=1,
                        random_state=27)
    tuning_grid = {'gamma': [0.1, 0.2]}
    gs = GridSearchXGB(alg)
    best_param = gs.search(x_train, y_train, tuning_grid)
    print('search result')
    print(best_param)
    print('current result')
    print(gs.get_params())


def test_early_stopping():
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    print('preparing data...')
    # 产生随机分类数据集，10个特征， 2个类别
    x, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=2)
    train_cols_list = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
    pdf = pd.DataFrame(x, columns=train_cols_list)
    pdf['label'] = y
    x_train, x_test, y_train, y_test = train_test_split(pdf.loc[:, train_cols_list],
                                                        pdf.loc[:, 'label'],
                                                        random_state=1)
    alg = XGBClassifier(learning_rate=0.1,
                        n_estimators=1000,
                        max_depth=5,
                        min_child_weight=1,
                        gamma=0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        objective='binary:logistic',
                        reg_lambda=1,
                        reg_alpha=0,
                        n_jobs=4,
                        scale_pos_weight=1,
                        random_state=27)
    tuning_grid = {'gamma': [0.1, 0.2]}
    gs = GridSearchXGB(alg)
    best_param = gs.search(x_train, y_train, tuning_grid,
                           [(x_test, y_test)], ['f1', 'roc_auc'],
                           early_stopping_rounds=3)
    print('search result')
    print(best_param)
    print('recheck current result')
    print(gs.get_params())


def test_consecutive_tuning_and_predict():
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    print('preparing data...')
    # 产生随机分类数据集，10个特征， 2个类别
    x, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=2)
    train_cols_list = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
    pdf = pd.DataFrame(x, columns=train_cols_list)
    pdf['label'] = y
    x_train, x_test, y_train, y_test = train_test_split(pdf.loc[:, train_cols_list],
                                                        pdf.loc[:, 'label'],
                                                        random_state=1)
    alg = XGBClassifier(learning_rate=0.1,
                        n_estimators=1000,
                        max_depth=5,
                        min_child_weight=1,
                        gamma=0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        objective='binary:logistic',
                        reg_lambda=1,
                        reg_alpha=0,
                        n_jobs=4,
                        scale_pos_weight=1,
                        random_state=27)
    tuning_grid = {'gamma': [0.1, 0.2]}
    gs = GridSearchXGB(alg)
    best_param = gs.search(x_train, y_train, tuning_grid,
                           eval_set=[(x_test, y_test)], eval_metric=['accuracy', 'roc_auc'],
                           early_stopping_rounds=3)
    print('after n_estimators search is completed...')
    print(gs.get_params())
    best_param = gs.search(x_train, y_train, tuning_grid,
                           eval_set=[(x_test, y_test)], eval_metric=['accuracy', 'roc_auc'])
    print('after gamma_search is completed...')
    print(gs.get_params())
    gs.fit(x_train, y_train)
    print('model after fit...')
    print(gs.get_params())
    prediction, best_score_list, best_threshold_list = \
        gs.predict_proba_with_best_threshold(x_test, y_test, ['f1', 'roc_auc'])
    print(best_score_list)
    print(best_threshold_list)


def test_bayesian():
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    print('preparing data...')
    # 产生随机分类数据集，10个特征， 2个类别
    x, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=2)
    train_cols_list = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
    pdf = pd.DataFrame(x, columns=train_cols_list)
    pdf['label'] = y
    x_train, x_test, y_train, y_test = train_test_split(pdf.loc[:, train_cols_list],
                                                        pdf.loc[:, 'label'],
                                                        random_state=1)
    alg = XGBClassifier(learning_rate=0.1,
                        n_estimators=1000,
                        max_depth=5,
                        min_child_weight=1,
                        gamma=0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        objective='binary:logistic',
                        reg_lambda=1,
                        reg_alpha=0,
                        n_jobs=4,
                        scale_pos_weight=1,
                        random_state=27)
    tuning_grid = {'learning_rate': [0.11, 0.3], 'n_estimators': [10, 200]}
    gs = GridSearchXGB(alg)
    best_param = gs.search_with_bayesian(x_train, y_train, tuning_dict=tuning_grid,
                                         eval_set=[(x_test, y_test)], eval_metric=['f1', 'roc_auc'],
                                         init_points=1, n_iter=3)
    print('after bayesian search is completed...')
    print(gs.get_params())


if __name__ == '__main__':
    test_consecutive_tuning_and_predict()