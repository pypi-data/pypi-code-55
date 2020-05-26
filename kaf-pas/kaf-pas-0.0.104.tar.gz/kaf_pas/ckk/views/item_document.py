from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from kaf_pas.ckk.models.item_document import Item_document, Item_documentManager


@JsonResponseWithException()
def Item_document_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_document.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Item_documentManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Add(request):
    return JsonResponse(DSResponseAdd(data=Item_document.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item_document.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item_document.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item_document.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_document.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_document_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_document.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
