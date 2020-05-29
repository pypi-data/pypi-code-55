from napoleontoolbox.forecasting import forecasting_utility



class LassoModel():

    def __init__(self):#, method = 'standard'):
        pass
        # """ Initialize shape of target. """
        # if method == 'standard':
        #     self.model =  linear_model.LinearRegression()
        # if method == 'lasso':
        #     alpha = 0.1
        #     self.model = Lasso(alpha=alpha, fit_intercept=False, max_iter=5000)
        # if method == 'lgbm':
        #     self.model = lgb.LGBMRegressor()
        # if method == 'xgb':
        #     self.model = xgb.XGBRegressor()


    def calibrate(self, X, y):#, method = 'standard'):
        pass
        # if method == 'standard':
        #     #nothing to calibrate here
        #     self.model = linear_model.LinearRegression()
        # if method == 'lasso':
        #     param_grid = {
        #         'alpha': [0.01, 0.1,0.5,1],
        #     }
        #     gbm_grid = GridSearchCV(self.model, param_grid, cv=2)
        #     gbm_grid.fit(X, y)
        #     print('Best parameters found by grid search are:', gbm_grid.best_params_)
        #     best_params = gbm_grid.best_params_
        #     self.model = Lasso(alpha=best_params['alpha'], fit_intercept=False, max_iter=5000)
        # if method == 'lgbm':
        #     param_grid = {
        #         'boosting_type': ['gbdt'],
        #         'num_leaves': [int(x) for x in np.linspace(start=10, stop=30, num=10)],
        #         'max_depth': [int(x) for x in np.linspace(start=-1, stop=7, num=3)],
        #         'learning_rate': [0.001,0.01,0.2],
        #         'n_estimators': [int(x) for x in np.linspace(start=40, stop=120, num=40)]
        #     }
        #     gbm_grid = GridSearchCV(self.model, param_grid, cv=2)
        #     gbm_grid.fit(X, y)
        #     print('Best parameters found by grid search are:', gbm_grid.best_params_)
        #     best_params = gbm_grid.best_params_
        #     self.model.set_params(**best_params)
        #     return best_params
        # if method == 'xgb':
        #     params = {
        #         "colsample_bytree": uniform(0.7, 0.3),
        #         "gamma": uniform(0, 0.5),
        #         "learning_rate": uniform(0.03, 0.3),  # default 0.1
        #         "max_depth": randint(2, 6),  # default 3
        #         "n_estimators": randint(100, 150),  # default 100
        #         "subsample": uniform(0.6, 0.4)
        #     }
        #     cv = 2
        #     n_iter = 50
        #     # cv=3
        #     # n_iter = 200
        #     search = RandomizedSearchCV(self.model, param_distributions=params, random_state=42, n_iter=n_iter, cv=cv,
        #                                 verbose=1, n_jobs=1, return_train_score=True)
        #     search.fit(X, y)
        #     print('reporting best scores')
        #     report_best_scores(search.cv_results_, 1)

    def fit(self, X_train, y_train, X_val, y_val):#, method = 'standard'):
        pass
        # if method == 'standard':
        #     self.model.fit(X_train, y_train)
        # if method == 'lasso':
        #     self.model.fit(X_train, y_train)
        # if method == 'lgbm':
        #     self.model.fit(X_train, y_train,eval_set=[(X_val, y_val)],eval_metric= ['l1','l2'],early_stopping_rounds=5,verbose= 0)
        # if method == 'xgb':
        #     self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric=['rmse', 'logloss'],
        #                    early_stopping_rounds=5, verbose=0)
        #

    def predict(self, X_test):#, method = 'standard'):
        pass
        # y_pred = self.model.predict(X_test)
        # return y_pred


    def get_features_importance(self, features_names):#, method = 'standard'):
        pass
        # run_importances = {}
        # if method == 'lgbm':
        #     for (name, imp) in zip(features_names, self.model.feature_importances_):
        #         run_importances[name] = imp
        # if method == 'standard':
        #     for (name, imp) in zip(features_names, self.model.coef_):
        #         run_importances[name] = imp
        # return run_importances
