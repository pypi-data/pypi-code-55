from pandas import DataFrame
from sklearn.metrics import explained_variance_score
from sklearn.metrics import max_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score


class Metric:

    @staticmethod
    def get(y_true, y_pred, label="metric"):
        """
        compares the root mean square error between the two data sets

        :param y_true:
        :param y_pred:
        :param label:
        :return:
        """

        mse = mean_squared_error(y_true=y_true, y_pred=y_pred)
        rmse = mse ** 0.5

        result = {
            'mse': [mse],
            'rmse': [rmse],
            'log_mse': [mean_squared_log_error(y_true, y_pred)],
            'explained_variance_score': [explained_variance_score(y_true=y_true, y_pred=y_pred)],
            'r2_score': [r2_score(y_true, y_pred)],
            'median_absolute_error': [median_absolute_error(y_true, y_pred)],
            'mean_squared_log_error': [mean_squared_log_error(y_true, y_pred)],
            'mean_absolute_error': [mean_absolute_error(y_true, y_pred)],
            'max_error': [max_error(y_true, y_pred)],
            'max_true': [y_true.max()],
            'max_pred': [y_pred.max()],
            'max_dif': [abs(y_true.max() - y_pred.max())],
            'integral_diff': [abs(y_true.sum() - y_pred.sum())]
        }
        df = DataFrame(result).transpose()
        df.columns = [label]
        df[f"rounded-{label}"] = df[label].round(2)
        return df
