# -*-coding:utf-8-*-
from .util import *
import shutil
import json


class Build:
    def __init__(self):
        self.author = '120901'
    
    @staticmethod
    def envCheck():
        cui.w('CHECK UPGRADE START....')
        # env
        setup_env()

    @staticmethod
    def buildTask(dir, out, biz):
        print('\r\n')
        cui.w('BUILD TASK START....')

        entry = dir
        biz_code = biz
        out_path = out
        out_path_zip = os.path.join(out_path, 'zip')

        if os.path.exists(out_path):
            shutil.rmtree(out_path)

        cui.i('out_path is {0}'.format(out_path))
        cui.i('out_path_zip is {0}'.format(out_path_zip))

        build_command = "accore1 build -p {0} -d {1}".format(entry, './temp')
        build_end = os.system(build_command)
        if build_end == 0:
            # mk output dir
            if not os.path.exists(out_path):
                os.makedirs(out_path)
                os.makedirs(out_path_zip)
            # process bin
            bin_result = get_files('./temp', '.bin')
            for binPath in bin_result:
                file_path, filename = os.path.split(binPath)
                # read json
                filename, __ignore = os.path.splitext(filename)
                json_path = os.path.join(file_path, filename + '.json')

                with open(json_path, 'r') as jsonFile:
                    json_file_content = jsonFile.read()

                json_dic = json.loads(json_file_content)
                meta_string = json_dic['meta']
                meta = json.loads(meta_string)
                version = meta['version']
                template_id = meta['name']
                # build template
                tpl_rename_path = "{0}@{1}@{2}.template".format(biz_code, template_id, version)
                os.rename(binPath, out_path + '/' + tpl_rename_path)
                # build zst
                zst_path = os.path.join(file_path, filename + '.zst')
                zstrename_path = "{0}@{1}@{2}.zip".format(biz_code, template_id, version)
                os.rename(zst_path, out_path_zip + '/' + zstrename_path)
                cui.s('MD5' + '(' + zstrename_path + '):' + fmd5(out_path_zip + '/' + zstrename_path))
        shutil.rmtree('./temp')
        cui.w('BUILD TASK  END....')
