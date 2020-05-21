import argparse
import math
import re

import requests
from lxml import etree


class XmlGeneration:

    def __init__(self):
        self.environment_info = {}
        self.stages_info_skipped = []
        self.stages_skipped = set()
        self.stages_unskipped = set()
        self.stages_info_unskipped = []


    def handler_request(self, url):
        """
        :param url:
        :return:
        """
        html = requests.get(url)
        if html.status_code == 200:
            return etree.HTML(html.content.decode('utf8'))
        else:
            print("Can not access! Please check the URL address: " + url)
            return -1

    def get_suffix(self, url, status_code):
        """
        Interestingly empty TODO
        :param url:
        :param status_code:
        :return:
        """
        tree = self.handler_request(url)
        if status_code == 0:
            return tree.xpath('//*[@id="completedJob-table"]/thead/tr/th[1]/a/@href')
        elif status_code == 1:
            return tree.xpath('//*[@id="completedStage-table"]/thead/tr/th[1]/a/@href')
        else:
            return -1

    def get_jobs_page(self, host, jobs):
        """
        page http://host:port/history/application_*************_****/1/jobs
        :param host:
        :param jobs:
        :return:
        """
        tree = self.handler_request(host + jobs)
        for line in tree.xpath(
                '/html/body/div[@class="container-fluid"]/div[4]/table[@id="completedJob-table"]/tbody/tr'):
            job = line.xpath('./td[2]/a/@href')[0]
            self.get_job_page(host + job)
        self.resolve_dependencies()

    def resolve_dependencies(self):
        for stage in self.stages_info_skipped:
            for equal_stage in self.stages_info_unskipped:
                if stage['stage_rdds'] <= equal_stage['stage_rdds']:
                    if stage['stage_rdds'] >= equal_stage['stage_rdds']:
                        stage['equal_stage'] = equal_stage['stage_id']
                        break
                else:
                    stage['equal_stage'] = []

    def get_job_page(self, url):
        """
        For each job
        :param url:
        :return:
        """
        tree = self.handler_request(url)
        lists = []
        for line in tree.xpath('//*[@id="dag-viz-metadata"]/div'):
            dicts = {'Job_id': re.findall(r'\d+', tree.xpath('/html/body/div[2]/div[1]/div/h3')[0].text.strip())[0],
                     'stage_id': int(line.attrib['stage-id']),
                     'stage_skipped': line.attrib['skipped']}
            list_parents_rdds = []
            for stage in line.xpath('./div'):
                if stage.attrib['class'] == 'dot-file':
                    set_rdd = set()
                    if re.search(r'\d+->\d+', stage.text):
                        for rdd in re.findall(r'\d+->\d+', stage.text):
                            set_rdd.update(tuple(rdd.split('->')))
                    dicts['stage_rdds'] = set_rdd
                elif stage.attrib['class'] == 'incoming-edge':
                    list_parents_rdds.append(stage.text.split(',')[0])
                else:
                    pass
            dicts['parent_rdds'] = set(tuple(list_parents_rdds))
            dicts['parent_stages'] = set()
            lists.append(dicts)
        reversed_list = list(reversed(lists))
        for i, stage in enumerate(reversed_list):
            if stage['parent_rdds']:
                for stage_parent in range(i + 1, len(reversed_list)):
                    if stage['parent_rdds'] & reversed_list[stage_parent]['stage_rdds']:
                        stage['parent_stages'].add(reversed_list[stage_parent]['stage_id'])

        stage_index = 0
        for line in tree.xpath(
                '//table[@id="completedStage-table"]/tbody/tr'):
            dicts_data = {
                'Task_Raw': line.xpath(
                    'normalize-space(./td[@class="progress-cell"]/div[@class="progress"]/span/text())').split(
                    '/')[0],
                'Input': self.transfer(line.xpath('./td[6]/text()')),
                'Output': self.transfer(line.xpath('./td[7]/text()')),
                'Shuffle_Read': self.transfer(line.xpath('./td[8]/text()')),
                'Shuffle_Write': self.transfer(line.xpath('./td[9]/text()'))}
            while reversed_list[stage_index]['stage_skipped'] == 'true':
                stage_index = stage_index + 1

            reversed_list[stage_index].update(dicts_data)
            stage_index = stage_index + 1

        for stage in reversed_list:
            if stage['stage_skipped'] == 'true':
                self.stages_info_skipped.append(stage)
                self.stages_skipped.add(stage['stage_id'])
            elif stage['stage_skipped'] == 'false':
                self.stages_info_unskipped.append(stage)
                self.stages_unskipped.add(stage['stage_id'])
            else:
                print("no skipped id")

    def get_stages_page(self, host, application):
        """                job = line.xpath('./td[2]/a/@href')[0]

        page http://host:port/history/application_*************_****/1/stages/?&completedStage.sort=Stage+Id&completedStage.desc=false&completedStage.pageSize=100#completed
        :param host: host:name
        :param application: application
        :return: lists
        """
        suffix = '/1/stages/?&completedStage.sort=Stage+Id&completedStage.desc=false&completedStage.pageSize=100#completed'
        url = host + '/history/' + application + suffix
        tree = self.handler_request(url)
        environment = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/ul[@class='nav']/li[4]/a/@href")[
            0]

        jobs = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/ul[@class='nav']/li[1]/a/@href")[
            0]
        self.get_jobs_page(host, jobs)
        self.get_environment_page(host + environment, application.split('_')[2])

    def get_environment_page(self, url, app_id):
        """
        page http://host:name/history/application_*************_****/1/environment/
        :param url: http://host:name/history/application_*************_****/1/environment/
        :param app_id: Application id
        :return: dicts
        """
        tree = self.handler_request(url)
        Application_Name = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/p[@class='navbar-text pull-right']/strong/@title")

        self.environment_info = {'Application_Name': app_id + '_' + Application_Name[0]}
        for line in tree.xpath(
                "/html/body/div[@class='container-fluid']/span/table[@class='table table-bordered table-condensed table-striped sortable'][2]/tbody/tr"):
            if line.xpath('./td[1]/text()')[0] == 'spark.executor.memory':
                self.environment_info['spark.executor.memory'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.executor.cores':
                self.environment_info['spark.executor.cores'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.driver.memory':
                self.environment_info['spark.driver.memory'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.default.parallelism':
                self.environment_info['spark.default.parallelism'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.memory.offHeap.size':
                self.environment_info['spark.memory.offHeap.size'] = line.xpath('./td[2]/text()')[0]
            '''
                Todo
            '''

    # return dicts

    def get_executor_num(self, url):
        """
        page http://host:name/history/application_*************_****/1/executors/
        :param url: http://host:name/history/application_*************_****/1/executors/
        :return:
        Todo
        """

        tree = self.handler_request(url)
        tree.path(
            "/html/body/div[@class='container-fluid']/div[2]/div[@id='active-executors']/div[@class='container-fluid'][2]/div[@class='container-fluid']/div[@id='active-executors-table_wrapper']/div[@class='row'][2]/div[@class='col-sm-12']/table[@id='active-executors-table']/tbody/tr[@class='odd'][1]/td[2]")

    def start(self, host, application, slaves, batch_file):
        """
        :param host: host:port
        :param application: application
        :param slaves: slave numbers
        :param batch_file: batch file path and names
        """
        self.get_stages_page(host, application)
        self.generate_xml(slaves, batch_file)

    def generate_xml(self, slaves, batch_file):
        """
        generating xml file
        :param slaves: slave numbers
        :param batch_file: batch file path and names
        """
        root = etree.Element('Configuration')
        DebugLevel = etree.SubElement(root, 'DebugLevel')
        DebugLevel.text = '0'
        SimuationGranularity = etree.SubElement(root, 'SimuationGranularity')
        SimuationGranularity.text = '65536'
        DiskReadGranularity = etree.SubElement(root, 'DiskReadGranularity')
        DiskReadGranularity.text = '65536'
        DiskWriteGranularity = etree.SubElement(root, 'DiskWriteGranularity')
        DiskWriteGranularity.text = '65536'
        TaskLogLevel = etree.SubElement(root, 'TaskLogLevel')
        TaskLogLevel.text = 'Standard'
        TaskLogModule = etree.SubElement(root, 'TaskLogModule')
        TaskLogModule.text = 'TaskALL'
        AppSetting = etree.SubElement(root, 'AppSetting')
        '''
             Generate AppSetting_header
        '''
        AppName = etree.SubElement(AppSetting, 'AppName')
        spark_settings = self.environment_info
        AppName.text = spark_settings['Application_Name']
        QueueName = etree.SubElement(AppSetting, 'QueueName')
        QueueName.text = 'Default'
        UserName = etree.SubElement(AppSetting, 'UserName')
        UserName.text = 'root'
        AppID = etree.SubElement(AppSetting, 'AppID')
        AppID.text = '0'
        ClientID = etree.SubElement(AppSetting, 'ClientID')
        ClientID.text = '0'
        AppType = etree.SubElement(AppSetting, 'AppType')
        AppType.text = 'Batch'
        RunMode = etree.SubElement(AppSetting, 'RunMode')
        RunMode.text = 'Yarn'
        Priority = etree.SubElement(AppSetting, 'Priority')
        Priority.text = '0'
        MaxCoreNumUsed = etree.SubElement(AppSetting, 'MaxCoreNumUsed')
        MaxCoreNumUsed.text = '288'
        MaxMemUsed = etree.SubElement(AppSetting, 'MaxMemUsed')
        MaxMemUsed.text = '1572864'
        list_stages=list(reversed(self.stages_info_unskipped))
        for index, stage in enumerate(list_stages):
            StageSetting = etree.SubElement(AppSetting, 'StageSetting')
            Name = etree.SubElement(StageSetting, 'Name')
            Name.text = 'Stage ' + str(stage['stage_id'])
            StageID = etree.SubElement(StageSetting, 'StageID')
            StageID.text = '1' + str("%03d" % int(stage['stage_id']))
            StageType = etree.SubElement(StageSetting, 'StageType')
            StageType.text = 'ShuffleMapTask'
            HasShuffleOutput = etree.SubElement(StageSetting, 'HasShuffleOutput')
            if stage['Shuffle_Write'] != '0':
                HasShuffleOutput.text = 'Y'
            else:
                HasShuffleOutput.text = 'N'
            TaskNum = etree.SubElement(StageSetting, 'TaskNum')
            if index == 0 and int(stage['Task_Raw']) < 7:
                TaskNum.text = '7'
            else:
                TaskNum.text = stage['Task_Raw']
            if (len(stage['parent_stages'])) | (
                    (index > 0)):
                ParentsStageID = etree.SubElement(StageSetting, 'ParentsStageID')

            RDDOperationSetting = etree.SubElement(StageSetting, 'RDDOperationSetting')
            ParentsOperationID = etree.SubElement(RDDOperationSetting, 'ParentsOperationID')
            ParentsOperationID.text = '-1'
            OperationType = etree.SubElement(RDDOperationSetting, 'OperationType')
            OperationType.text = 'Union'
            OperationID = etree.SubElement(RDDOperationSetting, 'OperationID')
            OperationID.text = '3'
            OperationCost = etree.SubElement(RDDOperationSetting, 'OperationCost')
            OperationCost.text = '0.1'
            InputRDDID = etree.SubElement(RDDOperationSetting, 'InputRDDID')
            InputRDDPartitionNum = etree.SubElement(RDDOperationSetting, 'InputRDDPartitionNum')

            if len(stage['parent_stages']):
                a=stage['parent_stages']

                for parent_stage_id in stage['parent_stages']:  # each parent stage
                    if parent_stage_id in self.stages_skipped:
                        for parent_real_stage in self.stages_info_skipped:
                            if parent_real_stage['stage_id'] == parent_stage_id:
                                if type(parent_real_stage['equal_stage']) is list:
                                    if ParentsStageID.text:
                                        ParentsStageID.text = ParentsStageID.text + ',' + '1' + str(
                        "%03d" % int(list_stages[index - 1]['stage_id']))
                                        InputRDDID.text = InputRDDID.text + ',' + '1' + str(
                        "%03d" % int(list_stages[index - 1]['stage_id']))
                                        InputRDDPartitionNum.text = InputRDDPartitionNum.text + ',' + list_stages[index - 1]['Task_Raw']

                                    else:
                                        ParentsStageID.text = '1' + str("%03d" % int(list_stages[index - 1]['stage_id']))
                                        InputRDDID.text = '1' + str(
                                            "%03d" % int(list_stages[index - 1]['stage_id']))
                                        InputRDDPartitionNum.text = list_stages[index - 1]['Task_Raw']
                                    break
                                else:
                                    if ParentsStageID.text:
                                        ParentsStageID.text = ParentsStageID.text + ',' + '1' + str(
                                            "%03d" % int(parent_real_stage['equal_stage']))
                                        InputRDDID.text = InputRDDID.text + ',' + '1' + str(
                                            "%03d" % int(parent_real_stage['equal_stage']))
                                    else:
                                        ParentsStageID.text = '1' + str("%03d" % int(parent_real_stage['equal_stage']))
                                        InputRDDID.text = '1' + str(
                                            "%03d" % int(parent_real_stage['equal_stage']))
                                    for real_stage in self.stages_info_unskipped:
                                        if real_stage['stage_id'] == parent_real_stage['equal_stage']:
                                            if InputRDDPartitionNum.text:
                                                InputRDDPartitionNum.text = InputRDDPartitionNum.text + ',' + \
                                                                            real_stage['Task_Raw']
                                            else:
                                                InputRDDPartitionNum.text = real_stage['Task_Raw']
                                            break
                                    break
                    else:
                        for parent_stage in self.stages_info_unskipped:
                            if parent_stage['stage_id'] == parent_stage_id:
                                if InputRDDPartitionNum.text:
                                    InputRDDPartitionNum.text = InputRDDPartitionNum.text + ',' + \
                                                                parent_stage['Task_Raw']
                                else:
                                    InputRDDPartitionNum.text = parent_stage['Task_Raw']
                                break
                        if ParentsStageID.text:
                            ParentsStageID.text = ParentsStageID.text + ',' + '1' + str(
                                "%03d" % int(parent_stage_id))
                            InputRDDID.text = InputRDDID.text + ',' + '1' + str(
                                "%03d" % int(parent_stage_id))
                        else:
                            ParentsStageID.text = '1' + str("%03d" % int(parent_stage_id))
                            InputRDDID.text = '1' + str(
                                "%03d" % int(parent_stage_id))
            else:
                if (index > 0) & (stage['Job_id'] != list_stages[index - 1]['Job_id']):
                    ParentsStageID.text = '1' + str(
                        "%03d" % int(list_stages[index - 1]['stage_id']))
                elif index > 0:
                    ParentsStageID.text = '1' + str(
                        "%03d" % int(list_stages[index - 1]['stage_id']))
                InputRDDID.text = '1' + str("%03d" % int(stage['stage_id']))
                InputRDDPartitionNum.text = stage['Task_Raw']

            InputSize = etree.SubElement(RDDOperationSetting, 'InputSize')
            InputRDDLocation = etree.SubElement(RDDOperationSetting, 'InputRDDLocation')
            if stage['Shuffle_Read'] != '0':
                InputRDDLocation.text = 'ShuffleRDD'
                InputSize.text = stage['Shuffle_Read']
            else:
                InputRDDLocation.text = 'HadoopRDD'
                if stage['Input']:
                    InputSize.text = stage['Input']
                else:
                    InputSize.text = '0'
            PartitionNum = etree.SubElement(RDDOperationSetting, 'PartitionNum')
            PartitionNum.text = TaskNum.text
            ShufflePartitionNum = etree.SubElement(RDDOperationSetting, 'ShufflePartitionNum')
            ShuffleOutputRDDID = etree.SubElement(RDDOperationSetting, 'ShuffleOutputRDDID')
            ShuffleOutPutSize = etree.SubElement(RDDOperationSetting, 'ShuffleOutPutSize')

            if stage['Shuffle_Write'] != '0':
                ShuffleOutPutSize.text = stage['Shuffle_Write']
                for child_stage in self.stages_info_unskipped:
                    if len(child_stage['parent_stages']):
                        for child_stage_id in child_stage['parent_stages']:
                            if child_stage_id == stage['stage_id']:
                                if ShufflePartitionNum.text:
                                    ShufflePartitionNum.text = ShufflePartitionNum.text + ',' + \
                                                               child_stage['Task_Raw']
                                    ShuffleOutputRDDID.text = ShuffleOutputRDDID.text + ',' + '1' + str(
                                        "%03d" % int(child_stage['stage_id']))
                                else:
                                    ShufflePartitionNum.text = child_stage['Task_Raw']
                                    ShuffleOutputRDDID.text = '1' + str("%03d" % int(child_stage['stage_id']))

                                break
                # for child_stage in self.stages_info_skipped:
                #     if len(child_stage['parent_stages']):
                #         for child_stage_id in child_stage['parent_stages']:
                #             if child_stage_id == stage['stage_id']:
                #                 for child_un_stage in self.stages_info_unskipped:
                #                     if child_un_stage['stage_id'] == child_stage['equal_stage']:
                #                         if ShufflePartitionNum.text:
                #                             ShufflePartitionNum.text = ShufflePartitionNum.text + ',' + \
                #                                                        child_stage['Task_Raw']
                #                             ShuffleOutputRDDID.text = ShuffleOutputRDDID.text + ',' + '1' + str(
                #                                 "%03d" % int(child_stage['stage_id']))
                #                         else:
                #                             ShufflePartitionNum.text = child_stage['Task_Raw']
                #                             ShuffleOutputRDDID.text = '1' + str("%03d" % int(child_stage['stage_id']))
                #                         break
            else:
                ShuffleOutputRDDID.text = ShuffleOutputRDDID.text = '1' + str("%03d" % int(stage['stage_id']))
                ShufflePartitionNum.text = stage['Task_Raw']
                ShuffleOutPutSize.text = '1'
            ShuffleSortMergeLib = etree.SubElement(RDDOperationSetting, 'ShuffleSortMergeLib')
            ShuffleSortMergeLib.text = 'AppendOnlyMap'
            ShuffleOutMergeRatio = etree.SubElement(RDDOperationSetting, 'ShuffleOutMergeRatio')
            ShuffleOutMergeRatio.text = '1.0'
            ShuffleOutCompressRatio = etree.SubElement(RDDOperationSetting, 'ShuffleOutCompressRatio')
            ShuffleOutCompressRatio.text = '1.0'
            ShuffleSortMergeCost = etree.SubElement(RDDOperationSetting, 'ShuffleSortMergeCost')
            ShuffleSortMergeCost.text = '1.0'
            ShuffleCompressCost = etree.SubElement(RDDOperationSetting, 'ShuffleCompressCost')
            ShuffleCompressCost.text = '2.0'
            ShuffleSerlizeCost = etree.SubElement(RDDOperationSetting, 'ShuffleSerlizeCost')
            ShuffleSerlizeCost.text = '15.0'
            ShuffleWriter = etree.SubElement(RDDOperationSetting, 'ShuffleWriter')
            ShuffleWriter.text = 'FileShuffle'
            ShuffleWriteSize = etree.SubElement(RDDOperationSetting, 'ShuffleWriteSize')
            ShuffleWriteSize.text = ShuffleOutPutSize.text

        '''
                Generate SparkSetting
        '''
        SparkSetting = etree.SubElement(AppSetting, 'SparkSetting')
        ExecutorMem = etree.SubElement(SparkSetting, 'ExecutorMem')
        try:
            data = re.findall(r"\d+", spark_settings['spark.executor.memory'])[0]
            if len(re.findall(r"\D+", spark_settings['spark.executor.memory'])):
                metr = re.findall(r"\D+", spark_settings['spark.executor.memory'])[0]
                ExecutorMem.text = self.transfer([data + ' ' + metr])
            else:
                ExecutorMem.text = str(float(data) / 1024 / 1024)
        except KeyError:
            ExecutorMem.text = '10240'
        ExecutorCore = etree.SubElement(SparkSetting, 'ExecutorCore')
        try:
            ExecutorCore.text = spark_settings['spark.executor.cores']
        except KeyError:
            ExecutorCore.text = '4'
        DriverMem = etree.SubElement(SparkSetting, 'DriverMem')
        try:
            data_driver = re.findall(r"\d+", spark_settings['spark.driver.memory'])[0]

            if len(re.findall(r"\D+", spark_settings['spark.driver.memory'])):
                metr_driver = re.findall(r"\D+", spark_settings['spark.driver.memory'])[0]
                DriverMem.text = self.transfer([data_driver + ' ' + metr_driver])
            else:
                DriverMem.text = str(float(data_driver) / 1024 / 1024)
        except KeyError:
            DriverMem.text = '61440'

        DriverCore = etree.SubElement(SparkSetting, 'DriverCore')
        DriverCore.text = '1'
        MaxAllocContainer = etree.SubElement(SparkSetting, 'MaxAllocContainer')
        MaxAllocContainer.text = '9999999'
        MinAllocContainer = etree.SubElement(SparkSetting, 'MinAllocContainer')
        MinAllocContainer.text = '1'
        TaskCPUs = etree.SubElement(SparkSetting, 'TaskCPUs')
        TaskCPUs.text = '1'
        ShuffleMemFraction = etree.SubElement(SparkSetting, 'ShuffleMemFraction')
        ShuffleMemFraction.text = '0.3'
        ShuffleSafetyFraction = etree.SubElement(SparkSetting, 'ShuffleSafetyFraction')
        ShuffleSafetyFraction.text = '0.8'
        ShuffleFileBufferKB = etree.SubElement(SparkSetting, 'ShuffleFileBufferKB')
        ShuffleFileBufferKB.text = '64'
        ShuffleCompress = etree.SubElement(SparkSetting, 'ShuffleCompress')
        ShuffleCompress.text = 'N'
        ShuffleSpill = etree.SubElement(SparkSetting, 'ShuffleSpill')
        ShuffleSpill.text = 'N'
        ShuffleSpillCompress = etree.SubElement(SparkSetting, 'ShuffleSpillCompress')
        ShuffleSpillCompress.text = 'N'
        RDDCompress = etree.SubElement(SparkSetting, 'RDDCompress')
        RDDCompress.text = 'N'
        RDDSerialized = etree.SubElement(SparkSetting, 'RDDSerialized')
        RDDSerialized.text = 'N'
        ShuffleConsolidateFile = etree.SubElement(SparkSetting, 'ShuffleConsolidateFile')
        ShuffleConsolidateFile.text = 'N'
        StorageMemFraction = etree.SubElement(SparkSetting, 'StorageMemFraction')
        StorageMemFraction.text = '0.6'
        IOCompressCodec = etree.SubElement(SparkSetting, 'IOCompressCodec')
        IOCompressCodec.text = 'None'
        IOSnappyCompressCodec = etree.SubElement(SparkSetting, 'IOSnappyCompressCodec')
        IOSnappyCompressCodec.text = '0'
        ReducerMaxMBinFlight = etree.SubElement(SparkSetting, 'ReducerMaxMBinFlight')
        ReducerMaxMBinFlight.text = '24'
        Serializer = etree.SubElement(SparkSetting, 'Serializer')
        Serializer.text = 'Default'
        KrySerizlizerBufferMB = etree.SubElement(SparkSetting, 'KrySerizlizerBufferMB')
        KrySerizlizerBufferMB.text = '1'
        SparkDefaultParallelism = etree.SubElement(SparkSetting, 'SparkDefaultParallelism')
        try:
            SparkDefaultParallelism.text = spark_settings['spark.default.parallelism']
        except KeyError:
            SparkDefaultParallelism.text = '8'
        LocalDirDiskNum = etree.SubElement(SparkSetting, 'LocalDirDiskNum')
        LocalDirDiskNum.text = '3'
        SchedulerReviveInterval = etree.SubElement(SparkSetting, 'SchedulerReviveInterval')
        SchedulerReviveInterval.text = '1000'
        AkkaThreads = etree.SubElement(SparkSetting, 'AkkaThreads')
        AkkaThreads.text = '4'
        JVMHeapSize = etree.SubElement(SparkSetting, 'JVMHeapSize')
        try:
            data = re.findall(r"\d+", spark_settings['spark.executor.memory'])[0]
            if len(re.findall(r"\D+", spark_settings['spark.executor.memory'])):
                metr = re.findall(r"\D+", spark_settings['spark.executor.memory'])[0]
                JVMHeapSize.text = self.transfer([data + ' ' + metr])
            else:
                JVMHeapSize.text = str(float(data) / 1024 / 1024)
        except KeyError:
            JVMHeapSize.text = '10240'

        JVMOffHeapSize = etree.SubElement(SparkSetting, 'JVMOffHeapSize')
        try:
            data_heap = re.findall(r"\d+", spark_settings['spark.memory.offHeap.size'])[0]
            if len(re.findall(r"\D+", spark_settings['spark.memory.offHeap.size'])):
                metr_heap = re.findall(r"\D+", spark_settings['spark.memory.offHeap.size'])[0]
                JVMOffHeapSize.text = self.transfer([data_heap + ' ' + metr_heap])
            else:
                JVMOffHeapSize.text = str(float(data_heap) / 1024 / 1024)
        except KeyError:
            JVMOffHeapSize.text = '4096'

        JVMYoungGCDropRatio = etree.SubElement(SparkSetting, 'JVMYoungGCDropRatio')
        JVMYoungGCDropRatio.text = '0.7'
        JVMFullGCDropRatio = etree.SubElement(SparkSetting, 'JVMFullGCDropRatio')
        JVMFullGCDropRatio.text = '0.8'
        JVMYoungGCCost = etree.SubElement(SparkSetting, 'JVMYoungGCCost')
        JVMYoungGCCost.text = '0.29'
        JVMFullGCCost = etree.SubElement(SparkSetting, 'JVMFullGCCost')
        JVMFullGCCost.text = '3.53'
        JVMYoungOldRatio = etree.SubElement(SparkSetting, 'JVMYoungOldRatio')
        JVMYoungOldRatio.text = '0.33'
        JVMEdenSurvRatio = etree.SubElement(SparkSetting, 'JVMEdenSurvRatio')
        JVMEdenSurvRatio.text = '0.8'
        JVMGCInitialCost = etree.SubElement(SparkSetting, 'JVMGCInitialCost')
        JVMGCInitialCost.text = '2'
        MemoryManageMode = etree.SubElement(SparkSetting, 'MemoryManageMode')
        MemoryManageMode.text = 'Unified'

        '''
             Generate YarnSetting
        '''
        YARNSetting = etree.SubElement(root, 'YARNSetting')
        Debug = etree.SubElement(YARNSetting, 'Debug')
        Debug.text = '0'
        ContinuesScheduling = etree.SubElement(YARNSetting, 'ContinuesScheduling')
        ContinuesScheduling.text = 'Y'
        SchedulePolicy = etree.SubElement(YARNSetting, 'SchedulePolicy')
        SchedulePolicy.text = 'FAIR'
        CapacityPolicy = etree.SubElement(YARNSetting, 'CapacityPolicy')
        CapacityPolicy.text = 'RESPECT_PARTITION_EXCLUSIVITY'
        MaxAllocMemory = etree.SubElement(YARNSetting, 'MaxAllocMemory')
        MaxAllocMemory.text = '6144'
        MaxAllocVCore = etree.SubElement(YARNSetting, 'MaxAllocVCore')
        MaxAllocVCore.text = '288'
        MinMemMB = etree.SubElement(YARNSetting, 'MinMemMB')
        MinMemMB.text = '128'
        MinVCore = etree.SubElement(YARNSetting, 'MinVCore')
        MinVCore.text = '1'
        MaxAssignContainerPerNodePerHeartbeat = etree.SubElement(YARNSetting, 'MaxAssignContainerPerNodePerHeartbeat')
        MaxAssignContainerPerNodePerHeartbeat.text = '1'
        ScheduleInterval = etree.SubElement(YARNSetting, 'ScheduleInterval')
        ScheduleInterval.text = '5'

        LabelSetting = etree.SubElement(YARNSetting, 'LabelSetting')
        Name = etree.SubElement(LabelSetting, 'Name')
        Name.text = '*'
        ResourceCore = etree.SubElement(LabelSetting, 'ResourceCore')
        ResourceCore.text = '288'
        ResourceMem = etree.SubElement(LabelSetting, 'ResourceMem')
        ResourceMem.text = '6144'
        Exclusive = etree.SubElement(LabelSetting, 'Exclusive')
        Exclusive.text = 'N'

        for i in range(slaves):
            NodeSetting = etree.SubElement(YARNSetting, 'NodeSetting')
            NodeID = etree.SubElement(NodeSetting, 'NodeID')
            NodeID.text = str(i)
            MaxAllocMemory = etree.SubElement(NodeSetting, 'MaxAllocMemory')
            MaxAllocMemory.text = '1280'
            MaxAllocVCore = etree.SubElement(NodeSetting, 'MaxAllocVCore')
            MaxAllocVCore.text = '72'
            Label = etree.SubElement(NodeSetting, 'Label')
            Label.text = '*'

        QueueSetting = etree.SubElement(YARNSetting, 'QueueSetting')
        Name = etree.SubElement(QueueSetting, 'Name')
        Name.text = 'Default'
        ParentName = etree.SubElement(QueueSetting, 'ParentName')
        ParentName.text = 'Default'
        QueueType = etree.SubElement(QueueSetting, 'QueueType')
        QueueType.text = 'LEAF'
        MaxMemMB = etree.SubElement(QueueSetting, 'MaxMemMB')
        MaxMemMB.text = '786432'
        MaxVCore = etree.SubElement(QueueSetting, 'MaxVCore')
        MaxVCore.text = '288'
        MinMemMB = etree.SubElement(QueueSetting, 'MinMemMB')
        MinMemMB.text = '128'
        MinVCore = etree.SubElement(QueueSetting, 'MinVCore')
        MinVCore.text = '1'
        Priority = etree.SubElement(QueueSetting, 'Priority')
        Priority.text = '1'

        CapacityLabels = etree.SubElement(QueueSetting, 'CapacityLabels')
        Name = etree.SubElement(CapacityLabels, 'Name')
        Name.text = '*'
        PendingCore = etree.SubElement(CapacityLabels, 'PendingCore')
        PendingCore.text = '1'
        PendingMem = etree.SubElement(CapacityLabels, 'PendingMem')
        PendingMem.text = '128'
        MaxCapacity = etree.SubElement(CapacityLabels, 'MaxCapacity')
        MaxCapacity.text = '100'

        '''
             Generate ClusterSetting
        '''
        ClusterSetting = etree.SubElement(root, 'ClusterSetting')

        # ClusterSetting.ClusterItemSetting

        ClusterItemSetting = etree.SubElement(ClusterSetting, 'ClusterItemSetting')
        ClusterType = etree.SubElement(ClusterItemSetting, 'ClusterType')
        ClusterType.text = 'CLUSTER_TRADITIONAL_SERVER'
        ServerNum = etree.SubElement(ClusterItemSetting, 'ServerNum')
        ServerNum.text = str(slaves + 1)
        CardNum = etree.SubElement(ClusterItemSetting, 'CardNum')
        CardNum.text = '12'
        ProcNumPerCard = etree.SubElement(ClusterItemSetting, 'ProcNumPerCard')
        ProcNumPerCard.text = '5'
        ServerSetting = etree.SubElement(ClusterSetting, 'ServerSetting')

        # ClusterSetting.ServerSetting
        # 1. ProcessorSetting

        ProcessorSetting = etree.SubElement(ServerSetting, 'ProcessorSetting')
        ProcessorNum = etree.SubElement(ProcessorSetting, 'ProcessorNum')
        ProcessorNum.text = '2'
        ProcessorType = etree.SubElement(ProcessorSetting, 'ProcessorType')
        ProcessorType.text = 'CPU_XEON_SKYLAKE'
        CoreNum = etree.SubElement(ProcessorSetting, 'CoreNum')
        CoreNum.text = '36'
        ThreadNum = etree.SubElement(ProcessorSetting, 'ThreadNum')
        ThreadNum.text = '1'
        ProcPerfIndicator = etree.SubElement(ProcessorSetting, 'ProcPerfIndicator')
        ProcPerfIndicator.text = '1'

        # ClusterSetting.ServerSetting
        # 2. Memory Setting
        MemorySetting = etree.SubElement(ServerSetting, 'MemorySetting')
        MemDeviceType = etree.SubElement(MemorySetting, 'MemDeviceType')
        MemDeviceType.text = 'MEMORY_DEVICE_DRAM'
        MemType = etree.SubElement(MemorySetting, 'MemType')
        MemType.text = 'Memory_DDR4_2666'
        MemChannleNum = etree.SubElement(MemorySetting, 'MemChannleNum')
        MemChannleNum.text = '6'
        MemSizeMB = etree.SubElement(MemorySetting, 'MemSizeMB')
        MemSizeMB.text = '1576000'

        # ClusterSetting.ServerSetting
        # 3. DiskAdapterSetting
        DiskAdapterSetting = etree.SubElement(ServerSetting, 'DiskAdapterSetting')
        DiskAdapterType = etree.SubElement(DiskAdapterSetting, 'DiskAdapterType')
        DiskAdapterType.text = 'ADAPTER_SATAIII'
        AdapterBandwidthGB = etree.SubElement(DiskAdapterSetting, 'AdapterBandwidthGB')
        AdapterBandwidthGB.text = '6'

        # ClusterSetting.ServerSetting
        # 4. DiskSetting
        DiskSetting = etree.SubElement(ServerSetting, 'DiskSetting')
        DiskNum = etree.SubElement(DiskSetting, 'DiskNum')
        DiskNum.text = '12'
        PerDiskSizeGB = etree.SubElement(DiskSetting, 'PerDiskSizeGB')
        PerDiskSizeGB.text = '2048'
        DiskType = etree.SubElement(DiskSetting, 'DiskType')
        DiskType.text = 'DISK_HDD'
        DiskAdapterType = etree.SubElement(DiskSetting, 'DiskAdapterType')
        DiskAdapterType.text = 'ADAPTER_SATAIII'

        # ClusterSetting.ServerSetting
        # 5. OSSetting
        OSSetting = etree.SubElement(ServerSetting, 'OSSetting')
        DirtyBackgroundRatio = etree.SubElement(OSSetting, 'DirtyBackgroundRatio')
        DirtyBackgroundRatio.text = '10'
        DirtyRatio = etree.SubElement(OSSetting, 'DirtyRatio')
        DirtyRatio.text = '40'
        DirtyExpireSec = etree.SubElement(OSSetting, 'DirtyExpireSec')
        DirtyExpireSec.text = '3'

        # ClusterSetting.SwitchSetting
        SwitchSetting = etree.SubElement(ClusterSetting, 'SwitchSetting')
        SwitchNum = etree.SubElement(SwitchSetting, 'SwitchNum')
        SwitchNum.text = '1'
        SwitchType = etree.SubElement(SwitchSetting, 'SwitchType')
        SwitchType.text = 'SWITCH_INTEL_RRC'

        # ClusterSetting.NetworkSetting
        NetworkSetting = etree.SubElement(ClusterSetting, 'NetworkSetting')
        TopoType = etree.SubElement(NetworkSetting, 'TopoType')
        TopoType.text = 'TOPOTYPE_RSA_SOW'
        LinkType = etree.SubElement(NetworkSetting, 'LinkType')
        LinkType.text = 'LINK_FABRIC_10Gbps'
        AtomicPacketSizeKB = etree.SubElement(NetworkSetting, 'AtomicPacketSizeKB')
        AtomicPacketSizeKB.text = '1.5'

        # ClusterSetting.NetworkSetting
        MonitorSetting = etree.SubElement(ClusterSetting, 'MonitorSetting')
        ProbeClusterUsageEnaled = etree.SubElement(MonitorSetting, 'ProbeClusterUsageEnaled')
        ProbeClusterUsageEnaled.text = '0'
        ProbeIntervalMS = etree.SubElement(MonitorSetting, 'ProbeIntervalMS')
        ProbeIntervalMS.text = '1000'
        LogLevel = etree.SubElement(MonitorSetting, 'LogLevel')
        LogLevel.text = '1'

        self.prettify_xml(root, '\t', '\n')
        tree = etree.ElementTree(root)
        tree.write(AppName.text + '.xml', xml_declaration=True, encoding='utf-8', method="xml")
        self.generate_batch_file(str(AppName.text), batch_file)



    @staticmethod
    def generate_batch_file(filename, batch_file):
        string = 'InMemComputing.exe --cf-gui-connect=no  --cf-gui-time-scale=ns "--cf-mon-on-time=0.0 us" "--cf-sim-duration=20000.0 s" --cf-verbosity=info --cf-hpf-enable=no --cf-lic-location=28518@plxs0415.pdx.intel.com --cf-dp-values-file=use_this_cofs_dp_re.csv --cfg=' + filename + '.xml' + ' > ' + filename + '.log' + '\n'
        try:
            with open(batch_file, 'a') as f:
                f.write(string)
                f.close()
        except FileNotFoundError:
            print("Writing to the batch file failed, please check the Path: " + batch_file)

    @staticmethod
    def transfer(data):
        if len(data):
            if data[0].split(' ')[1] == 'GB' or data[0].split(' ')[1] == 'g':
                return str(math.ceil(float(data[0].split(' ')[0]) * 1024))
            if data[0].split(' ')[1] == 'MB' or data[0].split(' ')[1] == 'm':
                return str(math.ceil(float(data[0].split(' ')[0])))
            if data[0].split(' ')[1] == 'KB':
                if float(data[0].split(' ')[0]) < 1024:
                    return '1'
                else:
                    return str(math.ceil(float(data[0].split(' ')[0]) / 1024))
        else:
            return '0'

    def prettify_xml(self, element, indent, newline, level=0):
        if len(element):
            if element.text is None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        temp = list(element)
        for sub_element in temp:
            if temp.index(sub_element) < (len(temp) - 1):
                sub_element.tail = newline + indent * (level + 1)
            else:
                sub_element.tail = newline + indent * level
            self.prettify_xml(sub_element, indent, newline, level=level + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', metavar='Host:Port', type=str, help='http://host:port', required=True)
    parser.add_argument('--slaves', metavar='Slave_numbers', type=int, help='The slave Numbers', required=True)
    parser.add_argument('--start_application', metavar='Application_Range', type=str,
                        help='The range of your application, started from this one')
    parser.add_argument('--end_application', metavar='Application_Range', type=str,
                        help='The range of your application, ended to this one')
    parser.add_argument('--applications', metavar='Applications', type=str, nargs='+', help='Application[s]')
    parser.add_argument('--xml_template_file', metavar='Xml_template', type=str, nargs='+', help='Xml_Template')
    parser.add_argument('--batch_template_file', metavar='Batch_Template', type=str, help='Batch_Template')
    parser.add_argument('--batch_file', metavar='Batch_file', type=str, help='Generated batch file path and name')
    args = parser.parse_args()
    host = args.host
    start_application = args.start_application
    end_application = args.end_application
    applications = args.applications

    if args.batch_file:
        batch_file = args.batch_file
    else:
        batch_file = 'run.bat'
    application_id_range = []

    if start_application or applications:
        if start_application:
            if end_application and start_application.split("_")[1] == end_application.split("_")[1]:
                for i in range(int(start_application.split("_")[2]), int(end_application.split("_")[2]) + 1):
                    application_id_range.append(
                        start_application.split("_")[0] + '_' + start_application.split("_")[1] + '_' + ("%04d" % i))
            else:
                print("Please check --start_application and --end_application")
        if applications:
            for application in applications:
                application_id_range.append(application)
    else:
        print("No applications Input, Please check --start_application and --end_application and --applications")

    try:
        with open(batch_file, 'a') as f:
            f.seek(0)
            f.truncate()
            f.close()
    except FileNotFoundError:
        print("Please check the batch file path: " + batch_file)
    while application_id_range:
        print(application_id_range[0] + ' start')
        try:
            xml_generation = XmlGeneration()
            xml_generation.start(host, application_id_range[0], args.slaves, batch_file)
            print(application_id_range[0] + ' finished')
        except IndexError:
            print("Application_Id don't match")

            print(application_id_range[0] + ' failed')
        application_id_range.remove(application_id_range[0])


if __name__ == "__main__":
    main()
