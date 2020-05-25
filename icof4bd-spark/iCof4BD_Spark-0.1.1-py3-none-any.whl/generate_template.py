import re
import pandas as pd

from lxml import etree


def generate_xml_template(web_statics, slaves):
    """
    :param web_statics:
    :param slaves:
    :return:
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
    spark_settings = web_statics.environment_info
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
    '''
            Generate SparkSetting
    '''
    SparkSetting = etree.SubElement(AppSetting, 'SparkSetting')
    ExecutorMem = etree.SubElement(SparkSetting, 'ExecutorMem')
    try:
        data = re.findall(r"\d+", spark_settings['spark.executor.memory'])[0]
        if len(re.findall(r"\D+", spark_settings['spark.executor.memory'])):
            metr = re.findall(r"\D+", spark_settings['spark.executor.memory'])[0]
            ExecutorMem.text = web_statics.transfer([data + ' ' + metr])
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
            DriverMem.text = web_statics.transfer([data_driver + ' ' + metr_driver])
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
            JVMHeapSize.text = web_statics.transfer([data + ' ' + metr])
        else:
            JVMHeapSize.text = str(float(data) / 1024 / 1024)
    except KeyError:
        JVMHeapSize.text = '10240'

    JVMOffHeapSize = etree.SubElement(SparkSetting, 'JVMOffHeapSize')
    try:
        data_heap = re.findall(r"\d+", spark_settings['spark.memory.offHeap.size'])[0]
        if len(re.findall(r"\D+", spark_settings['spark.memory.offHeap.size'])):
            metr_heap = re.findall(r"\D+", spark_settings['spark.memory.offHeap.size'])[0]
            JVMOffHeapSize.text = web_statics.transfer([data_heap + ' ' + metr_heap])
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

    web_statics.prettify_xml(root, '\t', '\n')
    tree = etree.ElementTree(root)
    tree.write('xml_ini.xml', xml_declaration=True, encoding='utf-8', method="xml")


def generate_batch_file_template():
    string = 'InMemComputing.exe --cf-gui-connect=no  --cf-gui-time-scale=ns "--cf-mon-on-time=0.0 us" ' \
             '"--cf-sim-duration=20000.0 s" --cf-verbosity=info --cf-hpf-enable=no ' \
             '--cf-lic-location=28518@plxs0415.pdx.intel.com --cf-dp-values-file=use_this_cofs_dp.csv --cfg='  # +
    # filename + '.xml' + ' > ' + filename + '.log' + '\n '
    try:
        with open('run_ini.txt', 'w') as f:
            f.write(string)
            f.close()
    except FileNotFoundError:
        print("Writing to the batch file failed, please check")


def generate_csv_file_template(slaves):
    list_data = [['/InMemComputing', 'SlaveNum', slaves - 1], ['/InMemComputing', 'AppMasterNum', 0],
                 ['/InMemComputing', 'CopierNum', 4]]
    for slave_id in range(slaves):
        list_data.append(['/InMemComputing/Slaves[' + str(slave_id) + ']', 'TaskRunnerNum', 71])
        list_data.append(['/InMemComputing/Slaves[' + str(slave_id) + ']', 'ExecutorNum', 17])

    data = pd.DataFrame(list_data, columns=['component_name', 'design_parameter_name', 'value'])
    data.to_csv('use_this_cofs_dp.csv', index=False)


# if __name__ == '__main__':
#     # xml_generation = XmlGeneration()
#     # ml_generation.start('http://10.239.166.104:18088', 'application_1587718859083_0232', 4,  'run.bat')
#     generate_xml_template(xml_generation,4)
#     generate_batch_file_template()
#     generate_csv_file_template(4)
