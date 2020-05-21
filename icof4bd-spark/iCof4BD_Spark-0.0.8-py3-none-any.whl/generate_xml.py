from lxml import etree

from iCof4BD_Spark.web_crawl import WebCrawl


def generate_xml(web_statics, slaves):
    """
    generating xml file
    :param web_statics:
    :param slaves: slave numbers
    """
    template_tree = etree.ElementTree(file='xml_ini.xml')
    template_tree_root = template_tree.getroot()
    root = etree.Element('Configuration')
    DebugLevel = etree.SubElement(root, 'DebugLevel')
    DebugLevel.text = list(template_tree_root.iter(tag='DebugLevel'))[0].text
    SimuationGranularity = etree.SubElement(root, 'SimuationGranularity')
    SimuationGranularity.text = list(template_tree_root.iter(tag='SimuationGranularity'))[0].text
    DiskReadGranularity = etree.SubElement(root, 'DiskReadGranularity')
    DiskReadGranularity.text = list(template_tree_root.iter(tag='DiskReadGranularity'))[0].text
    DiskWriteGranularity = etree.SubElement(root, 'DiskWriteGranularity')
    DiskWriteGranularity.text = list(template_tree_root.iter(tag='DiskWriteGranularity'))[0].text
    TaskLogLevel = etree.SubElement(root, 'TaskLogLevel')
    TaskLogLevel.text = list(template_tree_root.iter(tag='TaskLogLevel'))[0].text
    TaskLogModule = etree.SubElement(root, 'TaskLogModule')
    TaskLogModule.text = list(template_tree_root.iter(tag='TaskLogModule'))[0].text
    AppSetting = etree.SubElement(root, 'AppSetting')
    '''
         Generate AppSetting_header
    '''
    AppName = etree.SubElement(AppSetting, 'AppName')
    spark_settings = web_statics.environment_info
    AppName.text = spark_settings['Application_Name']
    QueueName = etree.SubElement(AppSetting, 'QueueName')
    QueueName.text = template_tree_root[6][1].text
    UserName = etree.SubElement(AppSetting, 'UserName')
    UserName.text = template_tree_root[6][2].text
    AppID = etree.SubElement(AppSetting, 'AppID')
    AppID.text = template_tree_root[6][3].text
    ClientID = etree.SubElement(AppSetting, 'ClientID')
    ClientID.text = template_tree_root[6][4].text
    AppType = etree.SubElement(AppSetting, 'AppType')
    AppType.text = template_tree_root[6][5].text
    RunMode = etree.SubElement(AppSetting, 'RunMode')
    RunMode.text = template_tree_root[6][6].text
    Priority = etree.SubElement(AppSetting, 'Priority')
    Priority.text = template_tree_root[6][7].text
    MaxCoreNumUsed = etree.SubElement(AppSetting, 'MaxCoreNumUsed')
    MaxCoreNumUsed.text = template_tree_root[6][8].text
    MaxMemUsed = etree.SubElement(AppSetting, 'MaxMemUsed')
    MaxMemUsed.text = template_tree_root[6][9].text
    list_stages = list(reversed(web_statics.stages_info_unskipped))
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
            for parent_stage_id in stage['parent_stages']:  # each parent stage
                if parent_stage_id in web_statics.stages_skipped:
                    for parent_real_stage in web_statics.stages_info_skipped:
                        if parent_real_stage['stage_id'] == parent_stage_id:
                            if type(parent_real_stage['equal_stage']) is list:
                                if ParentsStageID.text:
                                    ParentsStageID.text = ParentsStageID.text + ',' + '1' + str(
                                        "%03d" % int(list_stages[index - 1]['stage_id']))
                                    InputRDDID.text = InputRDDID.text + ',' + '1' + str(
                                        "%03d" % int(list_stages[index - 1]['stage_id']))
                                    InputRDDPartitionNum.text = InputRDDPartitionNum.text + ',' + \
                                                                list_stages[index - 1]['Task_Raw']

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
                                for real_stage in web_statics.stages_info_unskipped:
                                    if real_stage['stage_id'] == parent_real_stage['equal_stage']:
                                        if InputRDDPartitionNum.text:
                                            InputRDDPartitionNum.text = InputRDDPartitionNum.text + ',' + \
                                                                        real_stage['Task_Raw']
                                        else:
                                            InputRDDPartitionNum.text = real_stage['Task_Raw']
                                        break
                                break
                else:
                    for parent_stage in web_statics.stages_info_unskipped:
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
            for child_stage in web_statics.stages_info_unskipped:
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
            # for child_stage in web_statics.stages_info_skipped:
            #     if len(child_stage['parent_stages']):
            #         for child_stage_id in child_stage['parent_stages']:
            #             if child_stage_id == stage['stage_id']:
            #                 for child_un_stage in web_statics.stages_info_unskipped:
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
    ExecutorMem.text = template_tree_root[6][10][0].text
    ExecutorCore = etree.SubElement(SparkSetting, 'ExecutorCore')
    ExecutorCore.text = template_tree_root[6][10][1].text
    DriverMem = etree.SubElement(SparkSetting, 'DriverMem')
    DriverMem.text = template_tree_root[6][10][2].text
    DriverCore = etree.SubElement(SparkSetting, 'DriverCore')
    DriverCore.text = template_tree_root[6][10][3].text
    MaxAllocContainer = etree.SubElement(SparkSetting, 'MaxAllocContainer')
    MaxAllocContainer.text = template_tree_root[6][10][4].text
    MinAllocContainer = etree.SubElement(SparkSetting, 'MinAllocContainer')
    MinAllocContainer.text = template_tree_root[6][10][5].text
    TaskCPUs = etree.SubElement(SparkSetting, 'TaskCPUs')
    TaskCPUs.text = template_tree_root[6][10][6].text
    ShuffleMemFraction = etree.SubElement(SparkSetting, 'ShuffleMemFraction')
    ShuffleMemFraction.text = template_tree_root[6][10][7].text
    ShuffleSafetyFraction = etree.SubElement(SparkSetting, 'ShuffleSafetyFraction')
    ShuffleSafetyFraction.text = template_tree_root[6][10][8].text
    ShuffleFileBufferKB = etree.SubElement(SparkSetting, 'ShuffleFileBufferKB')
    ShuffleFileBufferKB.text = template_tree_root[6][10][9].text
    ShuffleCompress = etree.SubElement(SparkSetting, 'ShuffleCompress')
    ShuffleCompress.text = template_tree_root[6][10][10].text
    ShuffleSpill = etree.SubElement(SparkSetting, 'ShuffleSpill')
    ShuffleSpill.text = template_tree_root[6][10][11].text
    ShuffleSpillCompress = etree.SubElement(SparkSetting, 'ShuffleSpillCompress')
    ShuffleSpillCompress.text = template_tree_root[6][10][12].text
    RDDCompress = etree.SubElement(SparkSetting, 'RDDCompress')
    RDDCompress.text = template_tree_root[6][10][13].text
    RDDSerialized = etree.SubElement(SparkSetting, 'RDDSerialized')
    RDDSerialized.text = template_tree_root[6][10][14].text
    ShuffleConsolidateFile = etree.SubElement(SparkSetting, 'ShuffleConsolidateFile')
    ShuffleConsolidateFile.text = template_tree_root[6][10][15].text
    StorageMemFraction = etree.SubElement(SparkSetting, 'StorageMemFraction')
    StorageMemFraction.text = template_tree_root[6][10][16].text
    IOCompressCodec = etree.SubElement(SparkSetting, 'IOCompressCodec')
    IOCompressCodec.text = template_tree_root[6][10][17].text
    IOSnappyCompressCodec = etree.SubElement(SparkSetting, 'IOSnappyCompressCodec')
    IOSnappyCompressCodec.text = template_tree_root[6][10][18].text
    ReducerMaxMBinFlight = etree.SubElement(SparkSetting, 'ReducerMaxMBinFlight')
    ReducerMaxMBinFlight.text = template_tree_root[6][10][19].text
    Serializer = etree.SubElement(SparkSetting, 'Serializer')
    Serializer.text = template_tree_root[6][10][20].text
    KrySerizlizerBufferMB = etree.SubElement(SparkSetting, 'KrySerizlizerBufferMB')
    KrySerizlizerBufferMB.text = template_tree_root[6][10][21].text
    SparkDefaultParallelism = etree.SubElement(SparkSetting, 'SparkDefaultParallelism')
    SparkDefaultParallelism.text = template_tree_root[6][10][22].text
    LocalDirDiskNum = etree.SubElement(SparkSetting, 'LocalDirDiskNum')
    LocalDirDiskNum.text = template_tree_root[6][10][23].text
    SchedulerReviveInterval = etree.SubElement(SparkSetting, 'SchedulerReviveInterval')
    SchedulerReviveInterval.text = template_tree_root[6][10][24].text
    AkkaThreads = etree.SubElement(SparkSetting, 'AkkaThreads')
    AkkaThreads.text = template_tree_root[6][10][25].text
    JVMHeapSize = etree.SubElement(SparkSetting, 'JVMHeapSize')
    JVMHeapSize.text = template_tree_root[6][10][26].text
    JVMOffHeapSize = etree.SubElement(SparkSetting, 'JVMOffHeapSize')
    JVMOffHeapSize.text = template_tree_root[6][10][27].text
    JVMYoungGCDropRatio = etree.SubElement(SparkSetting, 'JVMYoungGCDropRatio')
    JVMYoungGCDropRatio.text = template_tree_root[6][10][28].text
    JVMFullGCDropRatio = etree.SubElement(SparkSetting, 'JVMFullGCDropRatio')
    JVMFullGCDropRatio.text = template_tree_root[6][10][29].text
    JVMYoungGCCost = etree.SubElement(SparkSetting, 'JVMYoungGCCost')
    JVMYoungGCCost.text = template_tree_root[6][10][30].text
    JVMFullGCCost = etree.SubElement(SparkSetting, 'JVMFullGCCost')
    JVMFullGCCost.text = template_tree_root[6][10][31].text
    JVMYoungOldRatio = etree.SubElement(SparkSetting, 'JVMYoungOldRatio')
    JVMYoungOldRatio.text = template_tree_root[6][10][32].text
    JVMEdenSurvRatio = etree.SubElement(SparkSetting, 'JVMEdenSurvRatio')
    JVMEdenSurvRatio.text = template_tree_root[6][10][33].text
    JVMGCInitialCost = etree.SubElement(SparkSetting, 'JVMGCInitialCost')
    JVMGCInitialCost.text = template_tree_root[6][10][34].text
    MemoryManageMode = etree.SubElement(SparkSetting, 'MemoryManageMode')
    MemoryManageMode.text = template_tree_root[6][10][35].text

    '''
         Generate YarnSetting
    '''
    YARNSetting = etree.SubElement(root, 'YARNSetting')
    Debug = etree.SubElement(YARNSetting, 'Debug')
    Debug.text = template_tree_root[7][0].text
    ContinuesScheduling = etree.SubElement(YARNSetting, 'ContinuesScheduling')
    ContinuesScheduling.text = template_tree_root[7][1].text
    SchedulePolicy = etree.SubElement(YARNSetting, 'SchedulePolicy')
    SchedulePolicy.text = template_tree_root[7][2].text
    CapacityPolicy = etree.SubElement(YARNSetting, 'CapacityPolicy')
    CapacityPolicy.text = template_tree_root[7][3].text
    MaxAllocMemory = etree.SubElement(YARNSetting, 'MaxAllocMemory')
    MaxAllocMemory.text = template_tree_root[7][4].text
    MaxAllocVCore = etree.SubElement(YARNSetting, 'MaxAllocVCore')
    MaxAllocVCore.text = template_tree_root[7][5].text
    MinMemMB = etree.SubElement(YARNSetting, 'MinMemMB')
    MinMemMB.text = template_tree_root[7][6].text
    MinVCore = etree.SubElement(YARNSetting, 'MinVCore')
    MinVCore.text = template_tree_root[7][7].text
    MaxAssignContainerPerNodePerHeartbeat = etree.SubElement(YARNSetting, 'MaxAssignContainerPerNodePerHeartbeat')
    MaxAssignContainerPerNodePerHeartbeat.text = template_tree_root[7][8].text
    ScheduleInterval = etree.SubElement(YARNSetting, 'ScheduleInterval')
    ScheduleInterval.text = template_tree_root[7][9].text

    LabelSetting = etree.SubElement(YARNSetting, 'LabelSetting')
    Name = etree.SubElement(LabelSetting, 'Name')
    Name.text = template_tree_root[7][10][0].text
    ResourceCore = etree.SubElement(LabelSetting, 'ResourceCore')
    ResourceCore.text = template_tree_root[7][10][1].text
    ResourceMem = etree.SubElement(LabelSetting, 'ResourceMem')
    ResourceMem.text = template_tree_root[7][10][2].text
    Exclusive = etree.SubElement(LabelSetting, 'Exclusive')
    Exclusive.text = template_tree_root[7][10][3].text

    for i in range(slaves):
        NodeSetting = etree.SubElement(YARNSetting, 'NodeSetting')
        NodeID = etree.SubElement(NodeSetting, 'NodeID')
        NodeID.text = str(i)
        MaxAllocMemory = etree.SubElement(NodeSetting, 'MaxAllocMemory')
        MaxAllocMemory.text = template_tree_root[7][11 + i][1].text
        MaxAllocVCore = etree.SubElement(NodeSetting, 'MaxAllocVCore')
        MaxAllocVCore.text = template_tree_root[7][11 + i][2].text
        Label = etree.SubElement(NodeSetting, 'Label')
        Label.text = template_tree_root[7][11 + i][3].text

    QueueSetting = etree.SubElement(YARNSetting, 'QueueSetting')
    Name = etree.SubElement(QueueSetting, 'Name')
    Name.text = template_tree_root[7][11 + slaves][0].text
    ParentName = etree.SubElement(QueueSetting, 'ParentName')
    ParentName.text = template_tree_root[7][11 + slaves][1].text
    QueueType = etree.SubElement(QueueSetting, 'QueueType')
    QueueType.text = template_tree_root[7][11 + slaves][2].text
    MaxMemMB = etree.SubElement(QueueSetting, 'MaxMemMB')
    MaxMemMB.text = template_tree_root[7][11 + slaves][3].text
    MaxVCore = etree.SubElement(QueueSetting, 'MaxVCore')
    MaxVCore.text = template_tree_root[7][11 + slaves][4].text
    MinMemMB = etree.SubElement(QueueSetting, 'MinMemMB')
    MinMemMB.text = template_tree_root[7][11 + slaves][5].text
    MinVCore = etree.SubElement(QueueSetting, 'MinVCore')
    MinVCore.text = template_tree_root[7][11 + slaves][6].text
    Priority = etree.SubElement(QueueSetting, 'Priority')
    Priority.text = template_tree_root[7][11 + slaves][7].text

    CapacityLabels = etree.SubElement(QueueSetting, 'CapacityLabels')
    Name = etree.SubElement(CapacityLabels, 'Name')
    Name.text = template_tree_root[7][11 + slaves][8][0].text
    PendingCore = etree.SubElement(CapacityLabels, 'PendingCore')
    PendingCore.text = template_tree_root[7][11 + slaves][8][1].text
    PendingMem = etree.SubElement(CapacityLabels, 'PendingMem')
    PendingMem.text = template_tree_root[7][11 + slaves][8][2].text
    MaxCapacity = etree.SubElement(CapacityLabels, 'MaxCapacity')
    MaxCapacity.text = template_tree_root[7][11 + slaves][8][3].text

    '''
         Generate ClusterSetting
    '''
    ClusterSetting = etree.SubElement(root, 'ClusterSetting')

    # ClusterSetting.ClusterItemSetting

    ClusterItemSetting = etree.SubElement(ClusterSetting, 'ClusterItemSetting')
    ClusterType = etree.SubElement(ClusterItemSetting, 'ClusterType')
    ClusterType.text = template_tree_root[8][0][0].text
    ServerNum = etree.SubElement(ClusterItemSetting, 'ServerNum')
    ServerNum.text = str(slaves + 1)
    CardNum = etree.SubElement(ClusterItemSetting, 'CardNum')
    CardNum.text = template_tree_root[8][0][2].text
    ProcNumPerCard = etree.SubElement(ClusterItemSetting, 'ProcNumPerCard')
    ProcNumPerCard.text = template_tree_root[8][0][3].text
    ServerSetting = etree.SubElement(ClusterSetting, 'ServerSetting')

    # ClusterSetting.ServerSetting
    # 1. ProcessorSetting

    ProcessorSetting = etree.SubElement(ServerSetting, 'ProcessorSetting')
    ProcessorNum = etree.SubElement(ProcessorSetting, 'ProcessorNum')
    ProcessorNum.text = template_tree_root[8][1][0][0].text
    ProcessorType = etree.SubElement(ProcessorSetting, 'ProcessorType')
    ProcessorType.text = template_tree_root[8][1][0][1].text
    CoreNum = etree.SubElement(ProcessorSetting, 'CoreNum')
    CoreNum.text = template_tree_root[8][1][0][2].text
    ThreadNum = etree.SubElement(ProcessorSetting, 'ThreadNum')
    ThreadNum.text = template_tree_root[8][1][0][3].text
    ProcPerfIndicator = etree.SubElement(ProcessorSetting, 'ProcPerfIndicator')
    ProcPerfIndicator.text = template_tree_root[8][1][0][4].text

    # ClusterSetting.ServerSetting
    # 2. Memory Setting
    MemorySetting = etree.SubElement(ServerSetting, 'MemorySetting')
    MemDeviceType = etree.SubElement(MemorySetting, 'MemDeviceType')
    MemDeviceType.text = template_tree_root[8][1][1][0].text
    MemType = etree.SubElement(MemorySetting, 'MemType')
    MemType.text = template_tree_root[8][1][1][1].text
    MemChannleNum = etree.SubElement(MemorySetting, 'MemChannleNum')
    MemChannleNum.text = template_tree_root[8][1][1][2].text
    MemSizeMB = etree.SubElement(MemorySetting, 'MemSizeMB')
    MemSizeMB.text = template_tree_root[8][1][1][3].text

    # ClusterSetting.ServerSetting
    # 3. DiskAdapterSetting
    DiskAdapterSetting = etree.SubElement(ServerSetting, 'DiskAdapterSetting')
    DiskAdapterType = etree.SubElement(DiskAdapterSetting, 'DiskAdapterType')
    DiskAdapterType.text = template_tree_root[8][1][2][0].text
    AdapterBandwidthGB = etree.SubElement(DiskAdapterSetting, 'AdapterBandwidthGB')
    AdapterBandwidthGB.text = template_tree_root[8][1][2][1].text

    # ClusterSetting.ServerSetting
    # 4. DiskSetting
    DiskSetting = etree.SubElement(ServerSetting, 'DiskSetting')
    DiskNum = etree.SubElement(DiskSetting, 'DiskNum')
    DiskNum.text = template_tree_root[8][1][3][0].text
    PerDiskSizeGB = etree.SubElement(DiskSetting, 'PerDiskSizeGB')
    PerDiskSizeGB.text = template_tree_root[8][1][3][1].text
    DiskType = etree.SubElement(DiskSetting, 'DiskType')
    DiskType.text = template_tree_root[8][1][3][2].text
    DiskAdapterType = etree.SubElement(DiskSetting, 'DiskAdapterType')
    DiskAdapterType.text = template_tree_root[8][1][3][3].text

    # ClusterSetting.ServerSetting
    # 5. OSSetting
    OSSetting = etree.SubElement(ServerSetting, 'OSSetting')
    DirtyBackgroundRatio = etree.SubElement(OSSetting, 'DirtyBackgroundRatio')
    DirtyBackgroundRatio.text = template_tree_root[8][1][4][0].text
    DirtyRatio = etree.SubElement(OSSetting, 'DirtyRatio')
    DirtyRatio.text = template_tree_root[8][1][4][1].text
    DirtyExpireSec = etree.SubElement(OSSetting, 'DirtyExpireSec')
    DirtyExpireSec.text = template_tree_root[8][1][4][2].text

    # ClusterSetting.SwitchSetting
    SwitchSetting = etree.SubElement(ClusterSetting, 'SwitchSetting')
    SwitchNum = etree.SubElement(SwitchSetting, 'SwitchNum')
    SwitchNum.text = template_tree_root[8][2][0].text
    SwitchType = etree.SubElement(SwitchSetting, 'SwitchType')
    SwitchType.text = template_tree_root[8][2][1].text

    # ClusterSetting.NetworkSetting
    NetworkSetting = etree.SubElement(ClusterSetting, 'NetworkSetting')
    TopoType = etree.SubElement(NetworkSetting, 'TopoType')
    TopoType.text = template_tree_root[8][3][0].text
    LinkType = etree.SubElement(NetworkSetting, 'LinkType')
    LinkType.text = template_tree_root[8][3][1].text
    AtomicPacketSizeKB = etree.SubElement(NetworkSetting, 'AtomicPacketSizeKB')
    AtomicPacketSizeKB.text = template_tree_root[8][3][2].text

    # ClusterSetting.NetworkSetting
    MonitorSetting = etree.SubElement(ClusterSetting, 'MonitorSetting')
    ProbeClusterUsageEnaled = etree.SubElement(MonitorSetting, 'ProbeClusterUsageEnaled')
    ProbeClusterUsageEnaled.text = template_tree_root[8][4][0].text
    ProbeIntervalMS = etree.SubElement(MonitorSetting, 'ProbeIntervalMS')
    ProbeIntervalMS.text = template_tree_root[8][4][1].text
    LogLevel = etree.SubElement(MonitorSetting, 'LogLevel')
    LogLevel.text = template_tree_root[8][4][2].text

    web_statics.prettify_xml(root, '\t', '\n')
    tree = etree.ElementTree(root)
    tree.write(AppName.text + '.xml', xml_declaration=True, encoding='utf-8', method="xml")
    generate_batch_file(str(AppName.text))


def generate_batch_file(AppName):
    string = ''
    try:
        with open('run_ini.txt', 'r') as f:
            string = f.read()
            f.close()
    except FileNotFoundError:

        print("Reading the template file failed, please check the file: run_template.txt")

    string = string + AppName + '.xml' + ' > ' + AppName + '.log' + '\n '
    try:
        with open('run.bat', 'a') as f:
            f.write(string)
            f.close()
    except FileNotFoundError:
        print("Writing to the batch file failed, please check the Path: ")

# if __name__ == '__main__':
#     wc = WebCrawl()
#     wc.get_start_page('http://10.239.166.104:18088', '/1/jobs', 'application_1587718859083_0232')
#     try:
#         generate_xml(wc, 4)
#     except OSError:
#         print("Failed to load file: template.xml")
