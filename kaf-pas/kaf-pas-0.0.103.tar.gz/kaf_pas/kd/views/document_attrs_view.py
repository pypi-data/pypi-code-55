from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from kaf_pas.kd.models.document_attrs_view import Document_attrs_view, Document_attrs_viewManager


@JsonResponseWithException()
def Document_attrs_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Document_attrs_view.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Document_attrs_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Document_attrs_view.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Document_attrs_view.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Document_attrs_view.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Document_attrs_view.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Document_attrs_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Document_attrs_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Document_attrs_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
