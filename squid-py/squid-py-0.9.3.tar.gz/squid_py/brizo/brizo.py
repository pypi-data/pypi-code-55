"""Brizo module."""

#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
import re
from json import JSONDecodeError

from ocean_keeper.utils import add_ethereum_prefix_and_hash_msg
from ocean_utils.exceptions import OceanEncryptAssetUrlsError
from ocean_utils.http_requests.requests_session import get_requests_session

from squid_py.models.algorithm_metadata import AlgorithmMetadata
from squid_py.ocean.keeper import SquidKeeper as Keeper

logger = logging.getLogger(__name__)


class Brizo:
    """
    `Brizo` is the name chosen for the asset service provider.

    The main functions available are:
    - consume_service
    - run_compute_service (not implemented yet)

    """
    _http_client = get_requests_session()

    @staticmethod
    def set_http_client(http_client):
        """Set the http client to something other than the default `requests`"""
        Brizo._http_client = http_client

    @staticmethod
    def encrypt_files_dict(files_dict, encrypt_endpoint, asset_id, account_address, signed_did):
        payload = json.dumps({
            'documentId': asset_id,
            'signedDocumentId': signed_did,
            'document': json.dumps(files_dict),
            'publisherAddress': account_address
        })
        response = Brizo._http_client.post(
            encrypt_endpoint, data=payload,
            headers={'content-type': 'application/json'}
        )
        if response and hasattr(response, 'status_code'):
            if response.status_code != 201:
                msg = (f'Encrypt file urls failed at the encryptEndpoint '
                       f'{encrypt_endpoint}, reason {response.text}, status {response.status_code}'
                       )
                logger.error(msg)
                raise OceanEncryptAssetUrlsError(msg)

            logger.info(
                f'Asset urls encrypted successfully, encrypted urls str: {response.text},'
                f' encryptedEndpoint {encrypt_endpoint}')

            return response.text

    @staticmethod
    def consume_service(agreement_id, service_endpoint, account, files,
                        destination_folder, index=None):
        """
        Call the brizo endpoint to get access to the different files that form the asset.

        :param agreement_id: Service Agreement Id, hex str
        :param service_endpoint: Url to consume, str
        :param account: Account instance of the consumer signing this agreement, hex-str
        :param files: List containing the files to be consumed, list
        :param index: Index of the document that is going to be downloaded, int
        :param destination_folder: Path, str
        :return: True if was downloaded, bool
        """
        signature = Keeper.get_instance().sign_hash(
            add_ethereum_prefix_and_hash_msg(agreement_id),
            account)

        if index is not None:
            assert isinstance(index, int), logger.error('index has to be an integer.')
            assert index >= 0, logger.error('index has to be 0 or a positive integer.')
            assert index < len(files), logger.error(
                'index can not be bigger than the number of files')
            consume_url = Brizo._create_consume_url(service_endpoint, agreement_id, account,
                                                    None, signature, index)
            logger.info(f'invoke consume endpoint with this url: {consume_url}')
            response = Brizo._http_client.get(consume_url, stream=True)
            file_name = Brizo._get_file_name(response)
            Brizo.write_file(response, destination_folder, file_name)
        else:
            for i, _file in enumerate(files):
                consume_url = Brizo._create_consume_url(service_endpoint, agreement_id,
                                                        account, _file,
                                                        signature, i)
                logger.info(f'invoke consume endpoint with this url: {consume_url}')
                response = Brizo._http_client.get(consume_url, stream=True)
                file_name = Brizo._get_file_name(response)
                Brizo.write_file(response, destination_folder, file_name or f'file-{i}')

    @staticmethod
    def start_compute_job(agreement_id, service_endpoint, account_address, signature,
                          algorithm_did=None, algorithm_meta=None, output=None, job_id=None):
        """

        :param agreement_id: Service Agreement Id, hex str
        :param service_endpoint:
        :param account_address: hex str the ethereum address of the consumer executing the compute job
        :param signature: hex str signed message to allow the provider to authorize the consumer
        :param algorithm_did: str -- the asset did (of `algorithm` type) which consist of `did:op:` and
            the assetId hex str (without `0x` prefix)
        :param algorithm_meta: see `OceanCompute.execute`
        :param output: see `OceanCompute.execute`
        :param job_id: str id of compute job that was started and stopped (optional, use it
            here to start a job after it was stopped)

        :return: job_info dict with jobId, status, and other values
        """
        assert algorithm_did or algorithm_meta, 'either an algorithm did or an algorithm meta must be provided.'

        payload = Brizo._prepare_compute_payload(
            agreement_id,
            account_address,
            signature,
            algorithm_did,
            algorithm_meta,
            output,
            job_id
        )
        logger.info(f'invoke start compute endpoint with this url: {payload}')
        response = Brizo._http_client.post(
            service_endpoint,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )
        logger.debug(f'got brizo execute response: {response.content} with status-code {response.status_code} ')
        if response.status_code not in (201, 200):
            raise Exception(response.content.decode('utf-8'))

        try:
            job_info = json.loads(response.content.decode('utf-8'))
            if isinstance(job_info, list):
                return job_info[0]
            return job_info

        except KeyError as err:
            logger.error(f'Failed to extract jobId from response: {err}')
            raise KeyError(f'Failed to extract jobId from response: {err}')
        except JSONDecodeError as err:
            logger.error(f'Failed to parse response json: {err}')
            raise

    @staticmethod
    def stop_compute_job(agreement_id, job_id, service_endpoint, account_address, signature):
        """

        :param agreement_id: hex str Service Agreement Id
        :param job_id: str id of compute job that was returned from `start_compute_job`
        :param service_endpoint: str url of the provider service endpoint for compute service
        :param account_address: hex str the ethereum address of the consumer's account
        :param signature: hex str signed message to allow the provider to authorize the consumer

        :return: bool whether the job was stopped successfully
        """
        return Brizo._send_compute_request(
            'put', agreement_id, job_id, service_endpoint, account_address, signature)

    @staticmethod
    def restart_compute_job(agreement_id, job_id, service_endpoint, account_address, signature):
        """

        :param agreement_id: hex str Service Agreement Id
        :param job_id: str id of compute job that was returned from `start_compute_job`
        :param service_endpoint: str url of the provider service endpoint for compute service
        :param account_address: hex str the ethereum address of the consumer's account
        :param signature: hex str signed message to allow the provider to authorize the consumer

        :return: bool whether the job was restarted successfully
        """
        Brizo.stop_compute_job(agreement_id, job_id, service_endpoint, account_address, signature)
        return Brizo.start_compute_job(agreement_id, service_endpoint, account_address, signature, job_id=job_id)

    @staticmethod
    def delete_compute_job(agreement_id, job_id, service_endpoint, account_address, signature):
        """

        :param agreement_id: hex str Service Agreement Id
        :param job_id: str id of compute job that was returned from `start_compute_job`
        :param service_endpoint: str url of the provider service endpoint for compute service
        :param account_address: hex str the ethereum address of the consumer's account
        :param signature: hex str signed message to allow the provider to authorize the consumer

        :return: bool whether the job was deleted successfully
        """
        return Brizo._send_compute_request(
            'delete', agreement_id, job_id, service_endpoint, account_address, signature)

    @staticmethod
    def compute_job_status(agreement_id, job_id, service_endpoint, account_address, signature):
        """

        :param agreement_id: hex str Service Agreement Id
        :param job_id: str id of compute job that was returned from `start_compute_job`
        :param service_endpoint: str url of the provider service endpoint for compute service
        :param account_address: hex str the ethereum address of the consumer's account
        :param signature: hex str signed message to allow the provider to authorize the consumer

        :return: dict of job_id to status info. When job_id is not provided, this will return
            status for each job_id that exist for the agreement_id
        """
        return Brizo._send_compute_request(
            'get', agreement_id, job_id, service_endpoint, account_address, signature)

    @staticmethod
    def compute_job_result(agreement_id, job_id, service_endpoint, account_address, signature):
        """

        :param agreement_id: hex str Service Agreement Id
        :param job_id: str id of compute job that was returned from `start_compute_job`
        :param service_endpoint: str url of the provider service endpoint for compute service
        :param account_address: hex str the ethereum address of the consumer's account
        :param signature: hex str signed message to allow the provider to authorize the consumer

        :return: dict of job_id to result urls. When job_id is not provided, this will return
            result for each job_id that exist for the agreement_id
        """
        return Brizo._send_compute_request(
            'get', agreement_id, job_id, service_endpoint, account_address, signature
        )

    @staticmethod
    def get_brizo_url(config):
        """
        Return the Brizo component url.

        :param config: Config
        :return: Url, str
        """
        brizo_url = 'http://localhost:8030'
        if config.has_option('resources', 'brizo.url'):
            brizo_url = config.get('resources', 'brizo.url') or brizo_url

        brizo_path = '/api/v1/brizo'
        return f'{brizo_url}{brizo_path}'

    @staticmethod
    def get_consume_endpoint(config):
        """
        Return the url to consume the asset.

        :param config: Config
        :return: Url, str
        """
        return f'{Brizo.get_brizo_url(config)}/services/consume'

    @staticmethod
    def get_compute_endpoint(config):
        """
        Return the url to execute the asset.

        :param config: Config
        :return: Url, str
        """
        return f'{Brizo.get_brizo_url(config)}/services/compute'

    @staticmethod
    def get_encrypt_endpoint(config):
        """
        Return the url to encrypt the asset.

        :param config: Config
        :return: Url, str
        """
        return f'{Brizo.get_brizo_url(config)}/services/publish'

    @staticmethod
    def write_file(response, destination_folder, file_name):
        """
        Write the response content in a file in the destination folder.
        :param response: Response
        :param destination_folder: Destination folder, string
        :param file_name: File name, string
        :return: bool
        """
        if response.status_code == 200:
            with open(os.path.join(destination_folder, file_name), 'wb') as f:
                for chunk in response.iter_content(chunk_size=None):
                    f.write(chunk)
            logger.info(f'Saved downloaded file in {f.name}')
        else:
            logger.warning(f'consume failed: {response.reason}')

    @staticmethod
    def _send_compute_request(http_method, agreement_id, job_id, service_endpoint, account_address, signature):
        compute_url = (
            f'{service_endpoint}'
            f'?signature={signature}'
            f'&serviceAgreementId={agreement_id}'
            f'&consumerAddress={account_address}'
            f'&jobId={job_id or ""}'
        )
        logger.info(f'invoke compute endpoint with this url: {compute_url}')
        method = getattr(Brizo._http_client, http_method)
        response = method(compute_url)
        print(f'got brizo execute response: {response.content} with status-code {response.status_code} ')
        if response.status_code != 200:
            raise Exception(response.content.decode('utf-8'))

        resp_content = json.loads(response.content.decode('utf-8'))
        if isinstance(resp_content, list):
            return resp_content[0]
        return resp_content

    @staticmethod
    def _get_file_name(response):
        try:
            return re.match(r'attachment;filename=(.+)',
                            response.headers.get('content-disposition'))[1]
        except Exception as e:
            logger.warning(f'It was not possible to get the file name. {e}')

    @staticmethod
    def _create_consume_url(service_endpoint, agreement_id, account, _file=None,
                            signature=None, index=None):
        if _file is not None and 'url' in _file:
            url = _file['url']
            if url.startswith('"') or url.startswith("'"):
                url = url[1:-1]
            return (f'{service_endpoint}'
                    f'?url={url}'
                    f'&serviceAgreementId={agreement_id}'
                    f'&consumerAddress={account.address}'
                    )
        else:
            return (f'{service_endpoint}'
                    f'?signature={signature}'
                    f'&serviceAgreementId={agreement_id}'
                    f'&consumerAddress={account.address}'
                    f'&index={index}'
                    )

    @staticmethod
    def _prepare_compute_payload(
            agreement_id, account_address,
            signature=None, algorithm_did=None, algorithm_meta=None,
            output=None, job_id=None):
        assert algorithm_did or algorithm_meta, 'either an algorithm did or an algorithm meta must be provided.'

        if algorithm_meta:
            assert isinstance(algorithm_meta, AlgorithmMetadata), f'expecting a AlgorithmMetadata type ' \
                                                                  f'for `algorithm_meta`, got {type(algorithm_meta)}'
            algorithm_meta = algorithm_meta.as_dictionary()

        return {
            'signature': signature,
            'serviceAgreementId': agreement_id,
            'consumerAddress': account_address,
            'algorithmDID': algorithm_did,
            'algorithmMeta': algorithm_meta,
            'output': output or dict(),
            'jobId': job_id or ""
        }
