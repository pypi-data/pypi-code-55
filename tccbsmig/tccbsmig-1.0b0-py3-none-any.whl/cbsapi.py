from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cbs.v20170312 import cbs_client, models
import json

def create_cbs(SecrectID, SecrectKey, Region, Zone, DiskType, DiskSize, ProjectId="", DiskName="", Tags=""):
    try:
        cred = credential.Credential(SecrectID, SecrectKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cbs.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cbs_client.CbsClient(cred, Region, clientProfile)

        req = models.CreateDisksRequest()
        PID, DName, T = '', '', ''
        #print(DiskName)
        if ProjectId:
            PID = ',"ProjectId":%s'%ProjectId
        if DiskName:
            DName = ',"DiskName":"%s"'%DiskName
        if Tags:
            T = ',"Tags":%s'%Tags
        #print(DName)
        params = '{"DiskType":"%s","DiskChargeType":"POSTPAID_BY_HOUR","DiskSize":%s,"Encrypt":"ENCRYPT","Placement":{"Zone":"%s"%s}%s%s}'%(DiskType, DiskSize, Zone, PID, DName, T)
        #print(params)
        req.from_json_string(params)

        resp = client.CreateDisks(req)
        print(resp.to_json_string())
        resp = json.loads(resp.to_json_string())
        return resp

    except TencentCloudSDKException as err:
        print(err)

def mount_cbs(SecrectID, SecrectKey, Region, DiskIds, InstanceId):
    try:
        cred = credential.Credential(SecrectID, SecrectKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cbs.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cbs_client.CbsClient(cred, Region, clientProfile)

        req = models.AttachDisksRequest()
        params = '{"DiskIds":["%s"],"InstanceId":"%s"}'%(DiskIds, InstanceId)
        req.from_json_string(params)

        resp = client.AttachDisks(req)
        print(resp.to_json_string())



    except TencentCloudSDKException as err:
        print(err)

def unmount_cbs(SecrectID, SecrectKey, Region, DiskIds, InstanceId):
    try:
        cred = credential.Credential(SecrectID, SecrectKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cbs.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cbs_client.CbsClient(cred, Region, clientProfile)

        req = models.DetachDisksRequest()
        params = '{"DiskIds":["%s"],"InstanceId":"%s"}'%(DiskIds, InstanceId)
        req.from_json_string(params)

        resp = client.DetachDisks(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
