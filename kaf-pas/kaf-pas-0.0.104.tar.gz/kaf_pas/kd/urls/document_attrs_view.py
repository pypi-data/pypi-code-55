from django.urls import path

from kaf_pas.kd.views import document_attrs_view

urlpatterns = [

    path('Document_attrs_view/Fetch/', document_attrs_view.Document_attrs_view_Fetch),
    path('Document_attrs_view/Add', document_attrs_view.Document_attrs_view_Add),
    path('Document_attrs_view/Update', document_attrs_view.Document_attrs_view_Update),
    path('Document_attrs_view/Remove', document_attrs_view.Document_attrs_view_Remove),
    path('Document_attrs_view/Lookup/', document_attrs_view.Document_attrs_view_Lookup),
    path('Document_attrs_view/Info/', document_attrs_view.Document_attrs_view_Info),
    path('Document_attrs_view/Copy', document_attrs_view.Document_attrs_view_Copy),

]
