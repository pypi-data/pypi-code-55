from django.urls import path

from kaf_pas.ckk.views import item_document

urlpatterns = [

    path('Item_document/Fetch/', item_document.Item_document_Fetch),
    path('Item_document/Add', item_document.Item_document_Add),
    path('Item_document/Update', item_document.Item_document_Update),
    path('Item_document/Remove', item_document.Item_document_Remove),
    path('Item_document/Lookup/', item_document.Item_document_Lookup),
    path('Item_document/Info/', item_document.Item_document_Info),
    path('Item_document/Copy', item_document.Item_document_Copy),

]
