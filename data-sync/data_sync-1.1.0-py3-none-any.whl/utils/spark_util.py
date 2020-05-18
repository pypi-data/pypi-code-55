import os


class SparkUtil(object):
    def __init__(self, target_db, target_tb, biz_date, last_date, primary_key, sort_key, sub_table_key=''):
        self.target_db = target_db
        self.target_tb = target_tb
        self.biz_date = biz_date
        self.last_date = last_date
        self.primary_key = primary_key
        self.sort_key = sort_key
        self.sub_table_key = sub_table_key

    def execute(self):
        print("******[MERGE] start******")
        jar = " s3://sync.data/jars/sync-spark/prod/sync-spark-jar-with-dependencies.jar "
        class_name = " com.clubfactory.data.sync.spark.apps.IncrementalDataMergeApp "
        class_params = '''{last_dt_loc} {dt_loc} {primary_key} {sort_key} {sub_table_key}'''.format(
            last_dt_loc=self.last_date,
            dt_loc=self.biz_date,
            primary_key=self.primary_key,
            sort_key=self.sort_key,
            sub_table_key=self.sub_table_key)

        command = """
                                spark-submit \
                                --queue sparkOffline \
                                --name platform_wangbin_incremental \
                                --conf spark.executor.extraJavaOptions=-Xmn5G  \
                                --conf spark.default.parallelism=1000 \
                                --class {class_name} \
                                {jar} \
                                {class_params}
                            """.format(jar=jar, class_name=class_name, class_params=class_params)

        print(command)
        os.system(command)
        print("******[MERGE] end******")
