from .. import GrowWeek
from .. import ItemReserve


class SalesInventoryAPI(object):

    def __init__(self, logger):
        self.logger = logger

    def createReserveAPI(self,reserveDate, customer_id, location_id, product_id, reserved):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        newReserve = gw.create_reserve(customer_id,location_id, product_id,reserved,reserveDate)
        return newReserve.get_dict()

    def updateReserveAPI(self,reserve_id, customer_id, location_id, product_id, reserved, reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        updReserve = gw.update_reserve(reserve_id, customer_id, location_id, product_id, reserved, reserveDate)
        return updReserve.get_dict()

    def deleteReserveAPI(self,reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.delete_resp()

    def getAllReservesAPI(self,reserveDate):
        gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        irList = gw.reserves
        return [resv.get_dict() for resv in irList]

    def getReserveAPI(self,reserve_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.get_dict()