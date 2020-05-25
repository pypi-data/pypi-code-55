# -*- coding:utf-8 -*-
import os
import datetime

from django.views import generic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .configs import MDConfig

# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')


class BaseUploadView(generic.View):
    """ base class for upload file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BaseUploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs.get('type') == 'file':
            upload_file = request.FILES.get("editormd-upload-file", None)
            upload_folder = MDEDITOR_CONFIGS['file_folder']
            upload_formats = MDEDITOR_CONFIGS['upload_file_formats']
        else:
            upload_file = request.FILES.get("editormd-image-file", None)
            upload_folder = MDEDITOR_CONFIGS['image_folder']
            upload_formats = MDEDITOR_CONFIGS['upload_image_formats']

        media_root = settings.MEDIA_ROOT

        # file none check
        if not upload_file:
            return JsonResponse({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            })

        # file format check
        file_name_list = upload_file.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension.lower() not in upload_formats:
            return JsonResponse({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    upload_formats),
                'url': ""
            })

        # file floder check
        file_path = os.path.join(media_root, upload_folder)
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return JsonResponse({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                })

        # save file
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),
                                       file_extension)
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        return JsonResponse({'success': 1,
                             'message': "上传成功！",
                             'url': os.path.join(settings.MEDIA_URL,
                                                 upload_folder,
                                                 file_full_name)})


class UploadView(BaseUploadView):
    """ image upload class """
    def post(self, request, *args, **kwargs):
        kwargs['type'] = 'image'
        return super(UploadView, self).post(request, *args, **kwargs)


class FileUploadView(BaseUploadView):
    """ file upload class """
    def post(self, request, *args, **kwargs):
        kwargs['type'] = 'file'
        return super(FileUploadView, self).post(request, *args, **kwargs)
