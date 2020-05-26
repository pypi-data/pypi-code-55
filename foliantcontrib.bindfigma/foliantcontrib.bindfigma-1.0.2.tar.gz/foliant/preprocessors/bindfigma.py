'''
Preprocessor for Foliant documentation authoring tool.
Downloads design layout images from Figma
using its REST API, resizes these images
and binds them with the documentation project.
'''

import re
import json
from os import getenv
from pathlib import Path
from hashlib import md5
from subprocess import run, PIPE, STDOUT, CalledProcessError
from urllib import request
from urllib.error import HTTPError
from urllib.parse import quote
from typing import Dict
OptionValue = int or float or bool or str

from foliant.utils import output
from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'cache_dir': Path('.bindfigmacache'),
        'api_caching': 'disabled',
        'convert_path': 'convert',
        'caption': '',
        'hyperlinks': True,
        'multi_delimeter': '\n\n',
        'resize': None,
        'access_token': None,
        'file_key': None,
        'ids': None,
        'scale': None,
        'format': None,
        'svg_include_id': None,
        'svg_simplify_stroke': None,
        'use_absolute_bounds': None,
        'version': None
    }

    tags = 'figma',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cache_dir_path = (self.project_path / self.options['cache_dir']).resolve()

        self.logger = self.logger.getChild('bindfigma')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def _http_request(
        self,
        request_url: str,
        request_method: str = 'GET',
        request_headers: dict or None = None,
        request_data: bytes or None = None
    ) -> dict:
        http_request = request.Request(request_url, method=request_method)

        if request_headers:
            http_request.headers = request_headers

        if request_data:
            http_request.data = request_data

        try:
            with request.urlopen(http_request) as http_response:
                response_status = http_response.getcode()
                response_headers = http_response.info()
                response_data = http_response.read()

        except HTTPError as http_response_not_ok:
            response_status = http_response_not_ok.getcode()
            response_headers = http_response_not_ok.info()
            response_data = http_response_not_ok.read()

        return {
            'status': response_status,
            'headers': response_headers,
            'data': response_data
        }

    def _download_and_resize(self, image_url: str, resized_image_width: str or None, format: str) -> Path or None:
        image_hash = f'{md5(image_url.encode()).hexdigest()}'
        downloaded_image_path = (self._cache_dir_path / f'downloaded_{image_hash}.{format}').resolve()

        self.logger.debug(f'Downloaded image path: {downloaded_image_path}')

        if downloaded_image_path.exists():
            self.logger.debug('Downloaded image found in cache')

        else:
            self.logger.debug(f'Downloading the image, URL: {image_url}')

            download_response = self._http_request(image_url)

            self.logger.debug(f'Response received, status: {download_response["status"]}')
            self.logger.debug(f'Response headers: {download_response["headers"]}')

            if download_response['status'] == 200:
                self._cache_dir_path.mkdir(parents=True, exist_ok=True)

                with open(downloaded_image_path, 'wb') as downloaded_image_file:
                    downloaded_image_file.write(download_response['data'])

                self.logger.debug('Response data written to the file')

            else:
                error_message = f'Failed to download the image, URL: {image_url}, source: {self.markdown_file_path}'

                output(error_message, self.quiet)

                self.logger.error(error_message)

                return None

        if resized_image_width and (format == 'png' or format == 'jpg'):
            self.logger.debug(f'Resize needed, image format: {format}, image width: {resized_image_width}')

            resized_image_path = (
                self._cache_dir_path / f'resized_{resized_image_width}_{image_hash}.{format}'
            ).resolve()

            self.logger.debug(f'Resized image path: {resized_image_path}')

            if resized_image_path.exists():
                self.logger.debug('Resized image found in cache')

            else:
                try:
                    self.logger.debug('Performing resize')

                    command = (
                        f'{self.options["convert_path"]} ' +
                        f'"{downloaded_image_path}" ' +
                        f'-resize {resized_image_width} ' +
                        f'"{resized_image_path}"'
                    )

                    run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

                except CalledProcessError as exception:
                    error_message = f'Failed to perform resize: {str(exception)}, source: {self.markdown_file_path}'

                    output(error_message, self.quiet)

                    self.logger.error(error_message)

                    return None

            return resized_image_path

        else:
            self.logger.debug('Do not perform resize')

            return downloaded_image_path

    def _process_figma(self, options: Dict[str, OptionValue]) -> str:
        api_request_params = {}
        downloaded_image_params = {}

        for option_name in self.options.keys():
            if option_name in [
                'access_token',
                'file_key',
                'ids',
                'scale',
                'format',
                'svg_include_id',
                'svg_simplify_stroke',
                'use_absolute_bounds',
                'version'
            ]:
                if options.get(option_name, None) is not None:
                    api_request_params[option_name] = options[option_name]

                else:
                    api_request_params[option_name] = self.options[option_name]

            elif option_name in [
                'caption',
                'hyperlinks',
                'multi_delimeter',
                'resize'
            ]:
                if options.get(option_name, None) is not None:
                    downloaded_image_params[option_name] = options[option_name]

                else:
                    downloaded_image_params[option_name] = self.options[option_name]

        downloaded_image_params['format_extension'] = api_request_params['format'] or 'png'
        downloaded_image_params['file_key'] = api_request_params['file_key']

        self.logger.debug(f'Figma definition found. API request parameters: {api_request_params}')

        if not (
            api_request_params['access_token']
            and
            api_request_params['file_key']
            and
            api_request_params['ids']
        ):
            error_message = (
                'Error: access_token, file_key, or ids not specified, skipping; ' +
                f'source: {self.markdown_file_path}'
            )

            output(error_message, self.quiet)

            self.logger.error(error_message)

            return ''

        token_header = {'X-Figma-Token': api_request_params.pop('access_token')}

        api_request_url = 'https://api.figma.com/v1/images/' + api_request_params.pop('file_key')

        if isinstance(api_request_params['ids'], list):
            api_request_params['ids'] = ','.join(api_request_params['ids'])

        api_request_url += '?ids=' + quote(api_request_params.pop('ids'), encoding='utf-8', safe='%')

        for param_name in api_request_params.keys():
            if api_request_params[param_name]:
                api_request_url += f'&{param_name}={api_request_params[param_name]}'

        self.logger.debug(
            f'Figma API to get images URLs, URL: {api_request_url}, custom header: {token_header}'
        )

        api_request_hash = md5(api_request_url.encode())
        api_request_hash.update(str(token_header).encode())
        api_response_cache_path = self._cache_dir_path / f'api_response_{api_request_hash.hexdigest()}.json'

        if api_response_cache_path.exists() and (
            self.options['api_caching'] == 'enabled' or (
                self.options['api_caching'] == 'env' and getenv('FOLIANT_FIGMA_CACHING') is not None
            )
        ):
            self.logger.debug('API responses caching is switched on, response data found in cache')

            with open(api_response_cache_path, encoding='utf8') as api_response_cache:
                api_response_data = json.load(api_response_cache)

            self.logger.debug(f'API response data restored from cache: {api_response_data}')

        else:
            self.logger.debug('Performing API request')

            api_response = self._http_request(api_request_url, 'GET', token_header)

            api_response_str = api_response['data'].decode('utf-8')
            api_response_data = json.loads(api_response_str)

            self.logger.debug(f'Response received, status: {api_response["status"]}')
            self.logger.debug(f'Response headers: {api_response["headers"]}')
            self.logger.debug(f'Response data: {api_response_data}')

            if api_response['status'] != 200 or api_response_data.get('err', None):
                error_message = (
                    f'Failed to perform API request, URL: {api_request_url}, ' +
                    f'source: {self.markdown_file_path}'
                )

                output(error_message, self.quiet)

                self.logger.error(error_message)

                return ''

            self.logger.debug('Storing received response in cache')

            with open(api_response_cache_path, 'w', encoding='utf8') as api_response_cache:
                api_response_cache.write(api_response_str)

        self.logger.debug(f'Parameters to apply to downloaded image: {downloaded_image_params}')

        image_references = []

        for image_id in api_response_data['images'].keys():
            image_url = api_response_data['images'][image_id]

            self.logger.debug(f'Image ID: {image_id}, image URL: {image_url}')

            if image_url:
                image_path = self._download_and_resize(
                    image_url,
                    downloaded_image_params['resize'],
                    downloaded_image_params['format_extension']
                )

                if image_path:
                    caption = downloaded_image_params['caption'].replace('{{image_id}}', image_id)
                    image_reference = f'![{caption}]({image_path})'

                    if downloaded_image_params['hyperlinks']:
                        image_reference = (
                            '[' + image_reference + '](https://www.figma.com/file/' +
                            downloaded_image_params['file_key'] +
                            '/?node-id=' + quote(image_id, encoding='utf-8', safe='%') + ')'
                        )

                    image_references.append(image_reference)

                else:
                    error_message = (
                        f'Failed to get path for the image, URL: {image_url}, ' +
                        f'source: {self.markdown_file_path}'
                    )

                    output(error_message, self.quiet)

                    self.logger.error(error_message)

            else:
                error_message = f'Failed to get URL for the image, ID: {image_id}, source: {self.markdown_file_path}'

                output(error_message, self.quiet)

                self.logger.error(error_message)

        return downloaded_image_params['multi_delimeter'].join(image_references)

    def process_figma(self, markdown_content: str) -> str:
        def _sub(figma_definition) -> str:
            return self._process_figma(self.get_options(figma_definition.group('options')))

        return self.pattern.sub(_sub, markdown_content)

    def apply(self):
        self.logger.info('Applying preprocessor')

        for self.markdown_file_path in self.working_dir.rglob('*.md'):
            self.logger.debug(f'Processing the file: {self.markdown_file_path}')

            with open(self.markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            processed_content = self.process_figma(content)

            if processed_content:
                with open(self.markdown_file_path, 'w', encoding='utf8') as markdown_file:
                    markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied')
