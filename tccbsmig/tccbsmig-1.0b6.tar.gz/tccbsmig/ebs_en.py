import json
import paramiko
from time import sleep
import tccbsmig.cbsapi as cbsapi
import argparse

parser = argparse.ArgumentParser(prog="tccbsmig", description='''\
Tccbsmig is designed to batch transfer all the data on an unencrypted CBS\
to an encrypted CBS for Tencent Cloud. To use it, you need to prepare a JSON file as an input, \
which includes your account SecrectID, SecrectKey, and all related CVM Instances and storages information.

For each disk needs to be encrypted, tccbsmig automatically calls CBS APIs to create a new encrypted CBS disk and mount it on the instance where unencrypted disk is attached, and then copies the data from unencrypted disk to the encrypted, and detaches the unencrypted disk after data transfer has been completed, and the new encrypted disk will be mounted at the same file path as the unencrypted disk in the end. 
''',
epilog="""
For more information about Tencent Cloud, please visit: https://intl.cloud.tencent.com
Cloud Virtual Machine: https://intl.cloud.tencent.com/product/cvm
Cloud Block Storage: https://intl.cloud.tencent.com/product/cbs

""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-f', '--file', nargs=1, type=argparse.FileType('r'), required=True, metavar='JSON file',
                    help='''A JSON file that contains CVM Instances and storages details.

Attributes' value share the same rules of the APIs that used in this program if applicable.
API used in this program:
CreateDisks: https://intl.cloud.tencent.com/document/api/362/16312
AttachDisks: https://intl.cloud.tencent.com/document/api/362/16313
DetachDisks: https://intl.cloud.tencent.com/document/api/362/16316

==========================================================
******An example of qualified JSON file is on the package info.******
==========================================================

JSON file structure explaination:
Credentials - this attribute is used to store credentials
  SecrectID - your account SecrectID
  SecrectKey - your account SecrectKey
CBS_Cases - stores all instances and block storages details
  CBS_1 - the name of each case. You can modify case's name to whatever you want.
    InstanceDetail - instance Detail
      InstanceId (String)- instance ID of your instance
      InstancePublicIP (String)- public IP address of your instance
      InstanceName (String)- your instance's name
      Region (String)- the region your instance is in
      Zone (String)- the availability zone your instance is in
      ProjectId (Int)- the project ID of your instance.
      Username (String)- username that used to log in your instance
      SSHKeyPath (String)- SSH Key file location
    CBSDetail - CBS detail
      DiskId (String)- the disk ID of your CBS
      DiskType (String)- the disk type of your CBS
      DiskSize (Int)- the size of your disk
      CBSPathOnCVM (String)- mount point of your disk
      FileSystem (String)- the file system your disk uses
      DiskName (String)- your disk name
      Tags (String)- tag of your disk. If you don't have it, leave an empty string here.''')

parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0b')
args = parser.parse_args()

data = json.load(args.file[0])

SecrectID, SecrectKey = data['Credentials']['SecrectID'], data['Credentials']['SecrectKey']
cases = data['CBS_Cases']

#connect to instance

#cbs migration function
def cbs_migration(case):
    #unpack case arguments
    InstanceDetail, CBSDetail = case["InstanceDetail"], case["CBSDetail"]

    host = InstanceDetail["InstancePublicIP"]
    user = InstanceDetail["Username"]
    KeyFilePath = InstanceDetail["SSHKeyPath"]
    InstanceName = InstanceDetail["InstanceName"]
    Region = InstanceDetail["Region"]
    Zone = InstanceDetail["Zone"]
    ProjectId = InstanceDetail["ProjectId"]
    InstanceId = InstanceDetail["InstanceId"]

    DiskId = CBSDetail["DiskId"]
    DiskType = CBSDetail["DiskType"]
    DiskSize = CBSDetail["DiskSize"]
    Ori_Disk_Path = CBSDetail["CBSPathOnCVM"]
    FileSystem = CBSDetail["FileSystem"]
    DiskName = CBSDetail["DiskName"]
    Tags = CBSDetail["Tags"]
    NewDiskPath = "/en-cbs-disk"

    sshkey = paramiko.RSAKey.from_private_key_file(KeyFilePath)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to Instance " + InstanceName + ' (' + host + ')')
    sleep(1)
    client.connect( hostname = host, username = user, pkey = sshkey )
    print("Connected")

#check available volumes and
    stdin, stdout, stderr = client.exec_command("lsblk")
    print("Block devices on instance " + InstanceName + ":")
    Ori_Disks = []
    for line in stdout.readlines():
        print(line[:-2])
        Ori_Disks += line.split()[0],

    if stderr.read():
        print(stderr.read())
        client.close()
        print("Migration failed: Error - can't find block devices")
        return 1

    #create and mount the encrypted disk
    if DiskName:
        NewDiskName = 'en-' + DiskName

    NewDiskId = cbsapi.create_cbs(SecrectID, SecrectKey, Region, Zone, DiskType, DiskSize, ProjectId=ProjectId, DiskName=NewDiskName, Tags=Tags)
    NewDiskId = NewDiskId['DiskIdSet'][0]
    print(NewDiskId, InstanceId, Region)
    print("Generating new encrypted disk...")
    sleep(20)
    cbsapi.mount_cbs(SecrectID, SecrectKey, Region, NewDiskId, InstanceId)
    print("Mounting new encrypted disk...")
    sleep(20)
    #find the device name of new added disk
    stdin, stdout, stderr = client.exec_command("lsblk")

    New_Device_Path = ""
    #print(Ori_Disks)
    for line in stdout.readlines():
        #print(line.split()[0])
        if line.split()[0] not in Ori_Disks:
            New_Device_Path = "/dev/" + line.split()[0]
            break

    print(New_Device_Path)
    #make directory for new disk
    stdin, stdout, stderr = client.exec_command("sudo mkdir " + NewDiskPath)

    #set the file system of new disk
    stdin, stdout, stderr = client.exec_command("sudo mkfs -t " + FileSystem + " " + New_Device_Path)

    print("Initiating file system...")
    sleep(15)

    stdin, stdout, stderr = client.exec_command("sudo file -s " + New_Device_Path)
    if stderr.read():
        print(stderr.read())
        client.close()
        print("Migration failed: Error - can't verify new device's file system")
        return 1

    for line in stdout.readlines():
        print(line[:-2])

    #mount the block device
    stdin, stdout, stderr = client.exec_command("sudo mount " + New_Device_Path + " " + NewDiskPath)
    if stderr.read():
        print(stderr.read())
        client.close()
        print("Migration failed: Error - can't mount new device")
        return 1

    #copy Data
    stdin, stdout, stderr = client.exec_command("sudo rsync -aAXv " + Ori_Disk_Path + "/ " + NewDiskPath)
    if stderr.read():
        print(stderr.read())
        client.close()
        print("Migration failed: An error occurred during migration")
        return 1

    print("Migrating data...")
    for line in stdout.readlines():
        print(line[:-2])

    #unmount old & new device
    stdin, stdout, stderr = client.exec_command("sudo umount " + Ori_Disk_Path)

    stdin, stdout, stderr = client.exec_command("sudo umount " + NewDiskPath)

    #unmount the old disk
    print("Umounting original data disk...")
    cbsapi.unmount_cbs(SecrectID, SecrectKey, Region, DiskId, InstanceId)
    sleep(15)
    print("Original data disk umounted")

    #mount new device to old device path
    stdin, stdout, stderr = client.exec_command("sudo mount " + New_Device_Path + " " + Ori_Disk_Path)

    print("Instance " + InstanceName + ' (' + host + ')' + "Migration Complete")
    print("Close connection to " + host)
    #close current session
    if client is not None:
        client.close()
        del client, stdin, stdout, stderr

    print("")
    sleep(5)
    return 0

#migrate cbs case by case
for case in cases:
    print("Start processing " + case + ":")
    result = cbs_migration(cases[case])
    if result: break
