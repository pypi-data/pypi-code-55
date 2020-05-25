from .sales_inv_utils import SalesInvBase
from datetime import datetime
import jmespath

from . import GetInstance
from .item_week import ItemWeek

class ReserveSummary(SalesInvBase):
    """ The summary of reserves for this grow week"""

    ext_fields = ['summary','id','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self,fsClient, **kwargs):
        self.summary = kwargs.get('summary',[])
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self._item_reserves_tot = {}  # {"Plants":{"Belita":5,"Bonita":8},"Vase":{"CoolX":3}}
        self._item_reserves = {}  # {"Plants":{"Belita":5,"Bonita":8},"Vase":{"CoolX":3}}
        super(ReserveSummary,self).__init__(fsClient,**kwargs)

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_doc_path)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    def base_path(self):
        return self._growWeekParent.path+'/ReservesSummary/'

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = ReserveSummary.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ReserveSummary(ReserveSummary.get_firestore_client(),**docDict)

    def getReserveItemAmts(self,item_type):
        item_reserves = self._item_reserves.get(item_type   ,{})
        if len(item_reserves.keys()) == 0:
            item_reserves_tot = self._item_reserves_tot.get(item_type,{})
            item_singular = ItemWeek.CleanItemType(item_type)
            item_key = item_singular+"s"
            for resv in self.summary:
                c = resv['customer']
                l = resv['location']
                i = resv['item_name']
                n = resv['num_reserved']
                _id = resv['id']

                if resv.get(item_key,None) is not None:
                    for item in resv.get(item_key,[]):
                        _key = ItemWeek.CleanItemName(item[item_singular])
                        amt = item_reserves_tot.get(_key,0)
                        num_items = resv.get('num_reserved',0) * item['qty']
                        amt = amt + num_items
                        item_reserves_tot[_key] = amt
                        iRsvs = item_reserves.get(_key,[])
                        iRsvs.append({'id':_id,'customer':c,'location':l,'item':i,'num_reserved':n,_key+"_qty":num_items})
                        item_reserves[_key] = iRsvs
            self._item_reserves[item_type] = item_reserves
            self._item_reserves_tot[item_type] = item_reserves_tot
        return {'total':self._item_reserves_tot[item_type],'by_item':self._item_reserves[item_type]}
    
    def getReserveAmtByItem(self,item_type, item_name):
        pltSumm = self.getReserveItemAmts(item_type)
        return pltSumm['total'].get(item_name,0)

    def getItemReserves(self,item_type, item_name):
        pltSumm = self.getReserveItemAmts(item_type)
        return pltSumm['by_item'][item_name]