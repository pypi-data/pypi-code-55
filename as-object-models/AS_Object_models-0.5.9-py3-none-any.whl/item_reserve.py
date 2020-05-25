from .sales_inv_utils import SalesInvBase

from datetime import datetime

from . import GetInstance

class ItemReserve(SalesInvBase):
    """ This is the plant that is being reserved by a customer 
    {
            customer: {
                id: customer-79164,
                name: Test Customer,
                type: Legacy, ## Can be either legacy or item_tracking
                path: application_data/Color_Orchids/....
            },
            id: ProductReserve-459726,
            finish_week: 2019_49,
            num_reserved: 485,
            item: {
                id: Product-4791597, # Or in the future will be Cust_Plant_Item-2976,
                name: Bonita X Umbra,
                type: Legacy, ## can be either legacy or item_tracking
                path: application_data/Color_orchids/....
            },
            plants: [  # copied from ProductPlant or from now on from the Recipe
                {
                    plant: {
                        id: Plant-197111, ## in the future will be Recipe_Costing-4975
                        name: Bonita
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 2   
                },
                {
                    plant: {
                        id: Plant-197411, ## in the future will be Recipe_Costing-4975
                        name: Mini Succulent,
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 1
                }
            ]
        }
    
    """

    ext_fields = ['customer','location','finish_week', 'reserve_date','num_reserved','item','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    NAME = 'Reserves'

    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.customer = kwargs.get('customer',{}) 
        self.location = kwargs.get('location',{})
        self.finish_week = kwargs.get('finish_week','')
        self._reserve_date = kwargs.get('reserve_date','')
        self.num_reserved = kwargs.get('num_reserved','') 
        self.item = kwargs.get('item',{}) 
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        super(ItemReserve, self).__init__(fsClient, **kwargs)
    
    def base_path(self):
        return ItemReserve.basePath()
    
    @classmethod
    def basePath(cls):
        return ItemReserve.__basePath(ItemReserve.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return cls.__growWeekBasePath+'/Reserves'

    @classmethod
    def __growWeekBasePath(cls):
        return ItemReserve.COLLECTION_NAME+'/'+ItemReserve.get_client().company+'/Sales_Inventory/Converted/GrowWeek'

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(ItemReserve.__growWeekBasePath()+'/'+self.finish_week)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    @property
    def reserve_date(self):
        '''
        If the reserve date is set.. use it.. otherwise default to monday of the GrowWeek
        '''
        if self._reserve_date is None or self._reserve_date == '':
            self._reserve_date = self._growWeekParent.week_monday
        if isinstance(self._reserve_date, datetime):
            self._reserve_date = self._reserve_date.isoformat()
        return self._reserve_date

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = ItemReserve.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ItemReserve(ItemReserve.get_firestore_client(),**docDict)

    @classmethod
    def getItemReserveInstance(cls,reserveId):
        pr = ItemReserve.GetByDNL(reserveId,ItemReserve)
        return pr

    @classmethod
    def get_active(cls):
        return ItemReserve.GetActive('Reserves',ItemReserve)

    def get_schema(self):
        schema = self.get_bq_schema()
        schema['fields'].append({'field_name':'customer_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'finish_week_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'product_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'num_reserved','field_type':'int'})
        #schema['fields'].append({'field_name':'shipped','field_type':'boolean'})
        ## Extra Fields from DB Stuff ##
        schema['fields'].append({'field_name':'plant_name','field_type':'string'}) ## saved as "plant"
        schema['fields'].append({'field_name':'vase_name','field_type':'string'}) ## saved as "plant"
        schema['fields'].append({'field_name':'product_name','field_type':'string'}) ## saved as "product"
        schema['fields'].append({'field_name':'customer_name','field_type':'string'}) ## saved as "customer"
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        values['customer_id'] = self.customer
        values['finish_week_id'] = self.finish_week
        values['product_id'] = self.item
        values['num_reserved'] = self.num_reserved
        #values['shipped'] = self.shipped
        ## get db fields ##
        dbDict = self.get_db_reserve2()
        values['plant_name'] = dbDict['plant']
        values['vase_name'] = dbDict['vase']
        values['product_name'] = dbDict['product']
        values['customer_name'] = dbDict['customer']
        return values

    def get_reserved(self):
        if self.num_reserved:
            return self.num_reserved
        return 0

    @classmethod
    def get_db_reserve(cls, res_id):
        '''
        During conversion, we need to register the id in DataNumberLookup.... to avoid collection collisions.. prefix with "DNL"
        i.e. DNL_Plant_Item
        This will make finding things faster... which we will use to implement "Get By ID" methodology
        '''
        pr = SalesInvBase.GetByDNL(res_id,ItemReserve)
        if pr:
            return pr.get_db_reserve2()
        return None

    @classmethod
    def get_reserves_for_week(cls,argWeek):
        col = ItemReserve.get_firestore_client().collection(argWeek.path+'/'+ItemReserve.NAME)
        docRefs = col.list_documents()
        return [ItemReserve.getInstance(x) for x in docRefs]

    def get_db_reserve2(self):
        prdb = {}
        prdb['_id'] = self.id
        prdb['plant'] = self.plants[0]['name']
        prdb['vase'] = self.vase['name']
        prdb['product'] = self.item['name']
        prdb['plant_id'] = self.plants[0]['id']
        prdb['vase_id'] = self.vase['id']
        prdb['product_id'] = self.item['id']
        prdb['num_reserved'] = self.num_reserved
        prdb['week_id'] = self.finish_week
        prdb['customer'] = self.customer['name']
        prdb['customer_id'] = self.customer['id']
        prdb['sales_rep'] = self.added_by
        prdb['add_date'] = self.timestamp
        prdb['soft_delete'] = "Y" if self.soft_delete and (self.soft_delete == True) else "N"
        return prdb

    @classmethod
    def hardDelete(cls,argId):
        pr = SalesInvBase.GetByDNL(argId,ItemReserve)
        SalesInvBase.DeleteByDNL(pr.id)
        pr.delete_resp()
        return True

    @classmethod
    def delete(cls, argId):
        pr = SalesInvBase.GetByDNL(argId,ItemReserve)
        if pr:
            pr.soft_delete = True
            return pr.update_ndb()
        else:
            resp = {'status':'not applicable','msg':'Entity does not exist... nothing to delete'}
            return resp

    @classmethod
    def update(cls,argId, argCustId, argLocId, argWeekId, argItemId, argReserved=0):
        """ pr = DataNumberLookup.get_obj_by_dnl(argId,ItemReserve)
        
        if pr:
            if pr.finish_week != argWeek.id:
                if ItemReserve.hardDelete(argId):
                    return  ItemReserve.add(argCustomer,argLocation,argWeek,argItem,argReserved,argId)
                else:
                    raise Exception("Could not delete reserve: "+argId)

            pr.customer = {}
            pr.customer['name'] = argCustomer.customer_name
            pr.customer['id'] = argCustomer.data_number_lookup
            pr.customer['path'] = argCustomer.path
            pr.customer['type'] = "Item_Tracking"

            pr.location = {}
            pr.location['name'] = argLocation.location_name
            pr.location['id'] = argLocation.data_number_lookup
            pr.location['path'] = argLocation.path
            pr.location['type'] = "Item_Tracking"

            pr.item = {}
            pr.item['name'] = argItem.Product_Name
            pr.item['id'] = argItem.data_number_lookup
            pr.item['path'] = argItem.path
            pr.item['type'] = "Item_Tracking"

            pr.num_reserved = int(argReserved)
        return pr.update_ndb() """
        raise Exception("Item Reserve: update not implemented")

    @classmethod
    def add(cls,argCustomer, argLocation, argWeek, argItem, argReserved=0, argDnl=None):
        dnl = argDnl
        if dnl is None:
            dnl = SalesInvBase.GetNextDNL(ItemReserve.NAME)

        data = {}
        data['customer'] = {}
        data['customer']['name'] = argCustomer.customer_name
        data['customer']['id'] = argCustomer.data_number_lookup
        data['customer']['path'] = argCustomer.path
        data['customer']['type'] = "Item_Tracking"

        data['location'] = {}
        data['location']['name'] = argLocation.location_name
        data['location']['id'] = argLocation.data_number_lookup
        data['location']['path'] = argLocation.path
        data['location']['type'] = "Item_Tracking"

        data['finish_week'] = argWeek.id

        data['item'] = {}
        data['item']['name'] = argItem.Product_Name
        data['item']['id'] = argItem.data_number_lookup
        data['item']['path'] = argItem.path
        data['item']['type'] = "Item_Tracking"

        data['num_reserved'] = int(argReserved)

        path = argWeek.path+'/'+ItemReserve.NAME+'/'+dnl
        docRef = ItemReserve.get_firestore_client().document(path)

        data['fs_docRef'] = docRef

        pr = ItemReserve(ItemReserve.get_firestore_client(),**data)
        resp = pr.update_ndb(True)

        SalesInvBase.AddDNL(dnl, docRef.path)
        
        return resp