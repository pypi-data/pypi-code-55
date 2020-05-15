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

    def __init__(self, **kwargs):
        self.mongo_hook = kwargs.get('mongo_hook')
        self.log = kwargs.get('log', Log(self.__class__.__name__))

    def conn_mongo(self, **kwargs):
        if self.mongo_hook:
            self.qa_db = self.mongo_hook.get_conn()['QaReport']
        else:
            self.qa_db = MongoHelper().connect(**kwargs)['QaReport']
        self.collection_qa = self.qa_db[self.__class__.__name__]

    def check(self, **kwargs):
        pass
        # self.conn_mongo(**kwargs)

    def get_history_qa_result(self, qa_type: str, record_count=10):
        qas = []
        for each in self.collection_qa.find({'qa_type': qa_type}):
            each.pop('_id')
            each.pop('qa_type')
            qas.append(pd.DataFrame(each))
        if not qas:
            return
        qa_history = pd.concat(qas).sort_index(ascending=False).head(record_count)
        return qa_history

    def check_qa_result(self, qa_now: pd.DataFrame, qa_type: str, **kwargs):
        qa_history = self.get_history_qa_result(qa_type)
        if not qa_history:
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

    def run(self, **kwargs):

        if kwargs.get('ti'):
            ti = kwargs['ti']
            task_ids = kwargs.get('task_ids', 'extract')
            xcom = ti.xcom_pull(task_ids=task_ids)
            files = xcom.get('export_result') if isinstance(xcom, dict) else [xcom]
            kwargs['files'] = files
        self.check(**kwargs)
        return self.after_run(**kwargs)

    def after_run(self, **kwargs):
        run_result = {}  # things to return
        if kwargs.get('email'):
            to = kwargs.get('email')
            email_result = self.send_qa_error_email(to)
            run_result['email_result'] = email_result
        return run_result

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
    t.check(file=r"C:\Users\Administrator\Downloads\canabis_qa_test\ca_cannabis_store_2019-11-21.csv", calc_history=True)