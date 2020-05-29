import boto3
import shutil
import subprocess

from awsdeployer.__util import *


class LayerHandler:
    def __init__(self, aws_config, layer_name, requirements_file):
        self.aws = aws_config
        self.client = boto3.client('lambda',
                                   region_name=self.aws['region'],
                                   aws_access_key_id=self.aws['access_key'],
                                   aws_secret_access_key=self.aws['secret_key'])
        self.layer_name = layer_name
        self.requirements_file = requirements_file

    def __get_version_list(self):
        response = self.client.list_layer_versions(
            CompatibleRuntime=self.aws['runtime'],
            LayerName=self.layer_name
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise RuntimeError

        return response['LayerVersions']

    def __get_last_version(self, versions=None):
        if not versions:
            versions = self.__get_version_list()

        # check if layer does not exist
        if len(versions) == 0:
            return None

        max_version = versions[0]
        for version in versions:
            if version['Version'] > max_version['Version']:
                max_version = version

        return max_version['Version'], max_version['LayerVersionArn']

    def get_arn(self):
        return self.__get_last_version()[1] if self.__get_last_version() else None

    def cleanup_old_versions(self):
        versions = self.__get_version_list()
        latest_layer = self.__get_last_version(versions)[0]

        for layer_version in versions:
            if layer_version['Version'] != latest_layer:
                print('Delete layer {0}:{1}'.format(self.layer_name, layer_version['Version']))

                response = self.client.delete_layer_version(
                    LayerName=self.layer_name,
                    VersionNumber=layer_version['Version']
                )

                if response['ResponseMetadata']['HTTPStatusCode'] != 204:
                    raise RuntimeError

        print('Deleted old versions of layer {0}, latest is {1}'.format(self.layer_name, latest_layer))

    def compile_new_version(self):
        tmp_dir = 'tmp-' + random_string(32)

        if not self.aws['runtime'].startswith('python'):
            raise ValueError('Unsupported runtime')

        package_dir_name = 'python'

        os.mkdir(tmp_dir)
        os.mkdir(tmp_dir + '/' + package_dir_name)

        shutil.copyfile(self.requirements_file, tmp_dir + '/requirements.txt')

        os.chdir(tmp_dir)

        # compile layer in docker
        command = '''docker run --rm -v {0}:/foo -w /foo lambci/lambda:build-{1} \
                        pip install -r requirements.txt --no-deps -t {2}'''.format(os.getcwd(), self.aws['runtime'], package_dir_name)

        comp = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
        if comp.returncode != 0:
            print('Could not compile new layer')
            raise RuntimeError

        # create package zip
        zip_name = 'temp.zip'
        zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

        for root, _, files in os.walk(package_dir_name):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()

        # read the zip into memory and send to aws
        content = read_file(zip_name)
        self.client.publish_layer_version(
            LayerName=self.layer_name,
            Content={
                'ZipFile': content
            },
            CompatibleRuntimes=[
                self.aws['runtime']
            ]
        )

        # cleanup
        os.chdir('..')
        shutil.rmtree(tmp_dir)
