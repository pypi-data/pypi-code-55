# -*- coding: utf-8 -*-
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.basicdata.IBasicDataApi import *
from iqsopenapi.models.Contract import *
from iqsopenapi.environment import *
import json
import datetime

class BasicDataApi(IBasicDataApi):
    """期货数据API"""

    def __init__(self):
        """构造函数"""
        super(BasicDataApi,self).__init__()

    def GetContract(self, symbol, exchange):
        """获取合约信息"""
        url = Environment.get_instance().get_apiurl('api/BasicData/GetContract')
        params = {'symbol':symbol,'exchange':exchange}
        strParams = json.dumps(params,ensure_ascii=False)
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            logger.error("data为空,request:" + url + "," + strParams + "response：" + resp)
            return None
        contract = self.__ToContract(data)
        return contract

    def GetMainContract(self, variety):
        """获取主力合约信息（期货）"""
        url = Environment.get_instance().get_apiurl('api/BasicData/GetMainContract')
        params = {'varietyCode':variety}
        strParams = json.dumps(params,ensure_ascii=False)
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            logger.error("data为空,request:" + url + "," + strParams + "response：" + resp)
            return None
        contract = self.__ToContract(data)
        return contract

    def GetOpenTimes(self,begin,end):
        """获取开盘时间"""
        url = Environment.get_instance().get_apiurl('api/BasicData/GetOpenTimes')
        params = {'begin':begin.strftime("%Y%m%d%H%M%S"),'end':end.strftime("%Y%m%d%H%M%S")}
        strParams = json.dumps(params,ensure_ascii=False)
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return []
        open_times = []
        for x in data:
            trade_time = self.__ToTradeTime(x)   
            open_times.append(trade_time)
        return open_times

    def __ToTradeTime(self, data):
        time_range = tradeTime()
        time_range.begin = data['begin']
        time_range.end = data['end']
        return time_range

    def __ToContract(self,data):
        """根据clientOrderID 获取订单详情"""
        if not data:
            return None
        item = Contract()
        item.contract_name = data["contractName"]
        item.contract_type = ContractType(data["contractType"])
        item.exchange = Exchange(data["exchange"])
        item.expire_date = datetime.datetime.strptime(data["expiryDate"],'%Y-%m-%d')
        item.list_date = datetime.datetime.strptime(data["listingDate"],'%Y-%m-%d')
        item.lots = data["lots"]
        item.step = data["priceStep"]
        item.right = data["right"]
        item.strike_px = data["strikePx"]
        item.symbol = data["symbol"]
        for x in data['tradeTimes']:
            time_range = self.__ToTradeTime(x)
            item.trade_times.append(time_range)
        return item

if __name__ == '__main__':

    config = {
      "runtime": "DEBUG"
    }
    environment = Environment(config)

    api = BasicDataApi()
    val1 = api.GetContract("rb2005","SHFE")
    logger.info(val1)

    val2 = api.GetMainContract("rb")
    logger.info(val2)

    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(days=1)
    val3 = api.GetOpenTimes(begin,end)
    
    pass