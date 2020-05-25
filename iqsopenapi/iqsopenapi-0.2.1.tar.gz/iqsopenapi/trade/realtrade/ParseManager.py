# -*- coding: utf-8 -*-
import datetime
import time
from iqsopenapi.trade.realtrade.Models import *
from iqsopenapi.models.Account import *
from iqsopenapi.models.Trade import *
from iqsopenapi.models.Order import *
from iqsopenapi.models.Position import *
from iqsopenapi.util.logutil import *

def __ParseBaseModelCore(model, json):
    if (model == None): model = ReposeModelBase()
    model.Json = json
    model.ErrorInfo = json['error_info']
    model.ErrorNo = json['error_no']
    return model

def ParseBaseModel(json):
    if not json: return None
    return __ParseBaseModelCore(None, json)

def ParseFuturesCompanysModel(json):
    if not json: return None
    model = FuturesCompanysModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    model.ArgeementTip = json['argeementTip']
    model.ArgeementHerfText = json['argeementHerfText']
    model.ArgeementHerf = json['argeementHerf']
    model.AppQRImage = json['appQRImg']
    data = json['data']
    for item in data:
        info = CompanyInfo()
        info.CompanyId = item['companyID']
        info.BrokerType = item['brokerType']
        info.CompanyName = item['brokerName']
        info.Description = item['desc']
        info.Phone = item['phone']
        info.Icon = item['ico']
        info.IsOnLine = item['isOnline']
        info.OpenAccountAddress = item['hkUrl']
        counter = item.get('tradingCounter')
        if (counter != None): info.TradeCounter = TradeCounterType(counter)
        model.CompanyInfos.append(info)
    return model

def ParseTradeCounterModel(json):
    if not json: return None
    model = TradeCounterModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    for item in json['counterList']:
        entity = TradeCounterEntity()
        entity.CounterId = item['counterID']
        entity.CounterName = item['counterName']
        counter = item.get('tradingCounter')
        if (counter != None): entity.TradeCounter = TradeCounterType(counter)
        for api in item['apiList']:
            api_entity = TradeApiEntity()
            api_entity.ApiAddr = api['apiAddr']
            api_entity.ApiName = api['apiName']
            api_entity.ApiInfoId = api['apiInfoId']
            api_entity.wsAddr = api['wsAddr']
            entity.ApiList.append(api_entity)
        model.CounterList.append(entity)
    return model

def ParseLoginResult(json):
    if not json: return None
    model = LoginResult()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    model.TradeToken = json['tradeToken']
    model.IsSigned = json['isSigned'] != 0
    return model

def ParseConOrderModel(json):
    if not json: return None
    model = ConOrderModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not ('data' in json)): return model
    for item in json['data']:
        info = ConditionOrderEntity()
        info.ConditionId = item['conditionID']
        info.Symbol = item['symbol']
        info.ContractId = item['contractID']
        info.Status = item['status']
        info.StatusStr = item['statusStr']
        info.OrderSide = OrderSide(item['orderSide']);
        info.OrderSideStr = item['orderSideStr']
        info.Offset = Offset(item['offset'])
        info.OffSetStr = item['offsetStr']
        info.OrderType = OrderType(item['orderType'])
        info.OrderTypeStr = item['orderTypeStr']
        info.Price = item['price']
        info.Quantity = item['quantity']
        info.ExpireType = ConOrderTimeValidTypeEnum(item['expireType'])
        info.AddTimeStr = item['addTimeStr']
        info.ExpireTimeStr = item['expireTimeStr']
        for ckv in item['condiValues']:
            kvi = kv()
            kvi.Key = ckv['k']
            kvi.Value = ckv['v']
            info.CondiValues.append(kvi)
        info.CondiValueStr = item['condiValueStr']
        info.OrderNo = item['orderNo']
        info.OrderRet = item['orderRet']
        info.OrderNote = item['orderNote']
        info.TriggerTimeStr = item['triggerTimeStr']
        model.Data.append(info)
    return model

def ParseStopOrderNotTriggerModel(json):
    if not json: return None
    model = StopOrderNotTriggerModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not ('data' in json)): return model
    for item in json['data']:
        info = StopOrderNotTrigger()
        info.StopId = item['stopID']
        info.Symbol = item['symbol']
        info.Name = item['name']
        info.PosSide = PosSide(item['posSide'])
        info.PosSideStr = item['posSideStr']
        info.StopType = item['stopType']
        info.StopTypeStr = item['stopTypeStr']
        info.TriggerPrice = item['stopPrice']
        info.OrderType = item['orderType']
        info.OrderTypeStr = item['orderTypeStr']
        info.Quantity = item['quantity']
        info.StatusStr = item['statusStr']
        model.Data.append(info)
    return model

def ParseUserAssetsModel(json):
    if not json: return None
    model = UserAssetsModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    info = Account()
    info.account_id = json['accountID']
    info.total_value = float(json['total'])
    info.available = float(json['available'])
    info.frozen_cash = float(json['frozenBalance'])
    info.market_value = float(json['marketBalance'])
    info.margin = float(json['margin'])
    info.begin_balance = float(json['beginBalance'])
    info.withdraw = float(json['withdraw'])
    info.currency = Currency[json['currency']]
    model.AssetInfo = info
    return model

def ParseEntrustModel(json):
    if not json: return None
    model = EntrustModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    for item in json['data']:
        info = Order()
        info.order_id = item['orderID']
        info.symbol = item['symbol']
        info.exchange = Exchange(item['exchange'])
        info.side = OrderSide[item['orderSide']]
        info.price = float(item['price'])
        info.offset = Offset(item['offset'])
        info.quantity = int(item['quantity'])
        info.order_time = datetime.strptime(item['orderTime'],'%Y%m%d%H%M%S')
        #委托类型 写死限价
        info.order_type = OrderType.LMT
        info.status = OrderStatus(item['orderStatus'])
        info.filled = int(item['filled'])
        info.note = item['errorMsg']
        model.EntrustInfos.append(info)
    return model

def ParsePositionModel(json):
    if not json: return None
    model = PositionModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not ('data' in json)): return model
    for item in json['data']:
        info = Position()
        info.symbol = item['symbol']
        info.exchange = Exchange(item['exchange'])
        info.last_px = float(item['lastPx'])
        quantity = int(item['volume'])
        info.quantity = quantity
        info.frozen = quantity - int(item['canCloseVol'])
        info.cost = float(item['positionCost'])
        info.side = PosSide(item['posSide'])
        info.margin = float(item['margin'])
        info.value = float(item['marketValue'])
        info.profit = float(item['dropIncome'])
        info.today_qty = int(item['todayVol'])
        info.today_avl = int(item['todayEnableVol'])
        model.Positions.append(info)
    return model

def ParseDoneModel(json):
    if not json: return None
    model = DoneModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not ('data' in json)): return model
    for item in json['data']:
        info = Trade()
        info.trade_id = item['executionID']
        if (not ('orderID' in item)): logger.info('成交接口没有orderID!')
        else: info.order_id = item['orderID']
        info.symbol = item['symbol']
        info.exchange = Exchange(item['exchange'])
        info.side = OrderSide[item['orderSide']]
        info.price = float(item['price'])
        info.offset = Offset(item['offset'])
        info.quantity = quantity = int(item['volume'])
        info.filled_time = datetime.strptime(item['executionTime'],'%Y%m%d%H%M%S')
        model.Dones.append(info)
    return model

def ParseSendOrderModel(json):
    if not json: return None
    model = SendOrderModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    model.OrderID = json['orderID']
    return model