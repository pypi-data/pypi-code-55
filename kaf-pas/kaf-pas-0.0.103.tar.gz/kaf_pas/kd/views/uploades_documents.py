import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from kaf_pas.kd.models.uploades_documents import Uploades_documents
from kaf_pas.kd.models.uploades_documents_view import Uploades_documents_view, Uploades_documentsViewManager


@JsonResponseWithException()
def Uploades_documents_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Uploades_documents_view.objects.
                select_related('document', 'upload').
                get_range_rows1(
                request=request,
                function=Uploades_documentsViewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Add(request):
    return JsonResponse(DSResponseAdd(data=Uploades_documents.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Update(request):
    return JsonResponse(DSResponseUpdate(data=Uploades_documents.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Remove(request):
    ws_channel = request.session.get('ws_channel')
    ws_port = settings.WS_PORT
    host = settings.WS_HOST

    _request = DSRequest(request=request)
    ids = _request.get_tuple_ids()
    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/Uploades_documents/Remove', params=dict(ids=ids, port=ws_port, ws_channel=ws_channel, host=host))
    HttpResponseRedirect(r.url)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Uploades_documents.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Info(request):
    return JsonResponse(DSResponse(request=request, data=Uploades_documents_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Uploades_documents_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Uploades_documents.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
