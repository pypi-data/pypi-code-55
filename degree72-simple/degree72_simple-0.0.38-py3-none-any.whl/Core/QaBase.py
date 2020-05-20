import numpy as np
import pandas as pd
from Util.MongoHelper import MongoHelper
from Core.Log import Log
from Util.JobHelper import *
from Util.EmailHelper import QaErrorEmailHelper


class QaBase:
    file = None  # file to check
    qa_db = None
    collection_qa = None
    run_result = {}

    def __init__(self, **kwargs):
        self.mongo_hook = kwargs.get('mongo_hook')
        self.log = kwargs.get('log', Log(self.__class__.__name__))

    def conn_mongo(self, **kwargs):
        if self.mongo_hook:
            self.qa_db = self.mongo_hook.get_conn()['QaReport']
        else:
            self.qa_db = MongoHelper().connect(**kwargs)['QaReport']
        self.collection_qa = self.qa_db[self.__class__.__name__]

    def get_history_qa_result(self, qa_type: str, record_count=10):
        qas = []
        for each in self.collection_qa.find({'qa_type': qa_type}):
            each.pop('_id')
            each.pop('qa_type')
            qas.append(pd.DataFrame(each))
        if not qas:
            return pd.DataFrame()
        qa_history = pd.concat(qas).sort_index(ascending=False).head(record_count)
        return qa_history

    def check_qa_result(self, qa_now: pd.DataFrame, qa_type: str, check_method: str = '3_sigema', **kwargs): # check qa result using 3 sigema princ
        if check_method == '3_sigema':
            return self.check_qa_result_use_3_sigema(qa_now, qa_type)
        else:
            raise ValueError('unknown check method', str(check_method))

    def check_qa_result_use_3_sigema(self, qa_now: pd.DataFrame, qa_type: str,): # check qa result using 3 sigema princ
        qa_history = self.get_history_qa_result(qa_type)
        if qa_history.empty:
            self.log.error("we haven't got history records yet", qa_type)
            return

        for col in qa_history:
            try:
                data_history = qa_history[col]
                std = data_history.std()
                mean = data_history.mean()
                if mean is np.nan:
                    self.log.info('Col in Nan %s ' % col)
                    continue
                if col in qa_now.columns:
                    data_this_run = qa_now[col].values[0]
                else:
                    self.log.error('''PAY ATTENTION !!!! We don't have column {} in this run'''.format(col))
                    continue

                if mean - 3 * std <= data_this_run <= mean + 3 * std:
                    pass
                else:
                    self.log.error(
                        "Column %s not qualified\n mean %s std %s data this run %s" % (
                            str(col), str(mean), str(std), str(data_this_run)))
                    self.log.error("increase/decrease ratio is %s" % str((data_this_run - mean) / mean))
            except Exception as e:
                self.log.error("failed to process col %s except: %s" % (str(col), str(e)))

    def save_qa_result(self, qa_result: pd.DataFrame, qa_type: str):
        qa_result_dict = qa_result.to_dict()
        qa_result_dict['qa_type'] = qa_type
        self.collection_qa.insert_one(qa_result_dict)

    @staticmethod
    def read_data_from_file(file) -> pd.DataFrame :
        '''
        user pandas to read data from file
        :param file:
        :return: pandas data frame
        '''
        if str(file).split('.')[-1] == 'csv':
            df = pd.read_csv(file)
        else:
            raise ValueError('Unknown file type', file)
        return df

    def read_data_from_mysql(self, **kwargs):
        pass

    def on_run(self, **kwargs):
        pass

    def run(self, **kwargs):
        self.before_run()
        self.run_result['run_result'] = self.on_run(**kwargs)
        self.after_run(**kwargs)
        return self.run_result

    def after_run(self, **kwargs):  # do something after run
        dag = kwargs.get('dag')
        if dag:
            email = dag.default_args.get('email')
            if email:
                email_result = self.send_qa_error_email(email)
                self.run_result['email_result'] = email_result

    def report_qa(self, qa_type):
        from tabulate import tabulate
        df_report = self.get_history_qa_result(qa_type)
        report_msg_consle = tabulate(df_report, showindex=True, headers='keys', tablefmt='psql')
        print('\n' + '{}:'.format(qa_type) + '\n' + report_msg_consle)

    def before_run(self, **kwargs):  # do something before run
        self.conn_mongo(**kwargs)

    def send_qa_error_email(self, to):
        if debug():
            return
        if not self.log.error_list:
            self.log.info('nothing wrong happened')
            return
        html_content = pd.DataFrame(self.log.error_list).to_html()
        QaErrorEmailHelper(to=to, html_content=html_content).send_email()
        return to


if __name__ == '__main__':
    t = QaBase()
