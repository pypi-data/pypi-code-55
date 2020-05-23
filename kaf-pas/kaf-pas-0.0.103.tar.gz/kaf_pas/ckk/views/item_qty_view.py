from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item_qty import Item_qty
from kaf_pas.ckk.models.item_qty_view import Item_qty_view, Item_qty_viewManager


@JsonResponseWithException()
def Item_qty_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_qty_view.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Item_qty_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Item_qty_view.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item_qty_view.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty_view.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
