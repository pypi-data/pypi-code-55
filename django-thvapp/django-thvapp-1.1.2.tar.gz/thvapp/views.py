import json
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed
from .thvisual import THVClient
# Create your views here.

def visualApps(request):
    return render(request,"thvapps.html",{})

def openApp(request):
    if request.method == "POST":
        pData = json.loads(request.body)
        vapp = pData.get('vapp')
        version = pData.get('version')
        gpu = pData.get('gpu')
        winWidth = pData.get('winWidth')
        winHeight = pData.get('winHeight','')

        if not winHeight == '':
            winWidth = int(winWidth * (winHeight - settings.TH_VISUALAPP_CONFIG.get("FOOTER_HEIGHT",80)) / winHeight)
            winHeight = int(winHeight - settings.TH_VISUALAPP_CONFIG.get("FOOTER_HEIGHT",80))
            winWidth = int(winHeight * settings.TH_VISUALAPP_CONFIG.get("SCREEN_RATIO"))
        print(winWidth)
        print(winHeight)
        server = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_HOST")
        appid = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPID")
        appkey = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPKEY")

        cluster = request.session.get('cluster', '')
        user = request.session.get('systemUsername', '')

        client = THVClient(appid, appkey, server, cluster, user)
        try:
            res = client.launchApp(vapp, gpu, version, winWidth, winHeight)
            vncToken = res.get("token")
            wsURI = "ws://%s/visual/v1/%s/%s/visual/%s/ws?token=%s" % (request.META['HTTP_HOST'],
                cluster, user, vapp, vncToken)
            vncPassword = res.get("vncPassword")
        except Exception as e:
            return JsonResponse({"success": "no", "error": e})
        return JsonResponse({"success": "yes", "wsURI": wsURI, 'vncYao': vncPassword})

def closeApp(request):
    if request.method == "POST":
        pData = json.loads(request.body)
        vapp = pData.get('vapp')
        version = pData.get('version')
        gpu = pData.get('gpu')

        server = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_HOST")
        appid = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPID")
        appkey = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPKEY")

        cluster = request.session.get('cluster', '')
        user = request.session.get('systemUsername', '')

        client = THVClient(appid, appkey, server, cluster, user)
        try:
            client.closeApp(vapp, gpu, version)
        except Exception as e:
            return JsonResponse({"success": "no", "error": e})
        return JsonResponse({"success": "yes"})

def listApp(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed("method not allowed")

    server = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_HOST")
    appid = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPID")
    appkey = settings.TH_VISUALAPP_CONFIG.get("VAPP_BACKEND_APPKEY")

    cluster = request.session.get('cluster', '')
    user = request.session.get('systemUsername', '')
    appIconsJson = request.session.get('vapp_icons')
    appIcons = json.loads(appIconsJson).get(cluster,{})

    client = THVClient(appid, appkey, server, cluster, user)
    try:
        res = client.listApps()
        apps = []
        appNames = list(set(list(map(lambda x: x.get("app"), res.get("vapps")))))
        defaultImage = settings.TH_VISUALAPP_CONFIG.get('VAPP_DEFAULT_IMGAGE_URL')
        for appName in appNames:
            newApp = {"name":"visual","app":appName}
            versions = []
            defaultVersion = ""
            defaultGPU = "no"
            gpus = []
            for a in res.get("vapps"):
                if a.get("app") == appName:
                    if a.get("version") not in versions:
                        versions.append(a.get("version"))
                    if a.get("default"):
                        defaultVersion = a.get('version')
                    if a.get("gpu",False):
                        gl = "GPU加速"
                        gk = "1"
                        gv = "yes"
                        defaultGPU = "yes"
                    else:
                        gl = "非GPU加速"
                        gk = "0"
                        gv = "no"
                    gpus.append({"key":gk,"val":gv,"lab":gl})
            newApp["versions"] = versions
            newApp["gpus"] = gpus
            newApp["defaultVersion"] = defaultVersion
            newApp["defaultGPU"] = defaultGPU
            newApp["value"] = appName
            apps.append(newApp)
            for key,appsAdv in appIcons.items():
                appIcons[key] = appsAdv
            if appIcons.get(appName,"") == "":
                newApp["image"] = defaultImage
            else:
                if appIcons.get(appName).get("video","") == "":
                    newApp["image"] = defaultImage
                else:
                    newApp["video"] = appIcons.get(appName).get("video")
                    newApp["showVideo"] = True
        apps.sort(key=lambda x:x.get("app"))
    except Exception as e:
        return JsonResponse({"success": "no", "error": e})
    return JsonResponse({"success":"yes","apps":apps})