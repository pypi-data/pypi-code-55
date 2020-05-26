from django.urls import path

from kaf_pas.ckk.views import item_qty_view

urlpatterns = [

    path('Item_qty_view/Fetch/', item_qty_view.Item_qty_view_Fetch),
    path('Item_qty_view/Add', item_qty_view.Item_qty_view_Add),
    path('Item_qty_view/Update', item_qty_view.Item_qty_view_Update),
    path('Item_qty_view/Remove', item_qty_view.Item_qty_view_Remove),
    path('Item_qty_view/Lookup/', item_qty_view.Item_qty_view_Lookup),
    path('Item_qty_view/Info/', item_qty_view.Item_qty_view_Info),
    path('Item_qty_view/Copy', item_qty_view.Item_qty_view_Copy),

]
