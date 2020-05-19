import logging

from ocean_keeper.account import Account
from ocean_keeper.web3_provider import Web3Provider
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.agreements.service_agreement import ServiceAgreement
from ocean_utils.did import id_to_did

from squid_py.brizo import BrizoProvider
from squid_py.models.algorithm_metadata import AlgorithmMetadata
from squid_py.agreement_events.accessSecretStore import refund_reward
from squid_py import ConfigProvider

logger = logging.getLogger('ocean')


class OceanCompute:
    """Ocean assets class."""

    def __init__(self, keeper, ocean_agreements, ocean_auth, did_resolver):
        self._keeper = keeper
        self._agreements = ocean_agreements
        self._auth = ocean_auth
        self._did_resolver = did_resolver

    @staticmethod
    def build_cluster_attributes(cluster_type, url):
        """

        :param cluster_type:
        :param url:
        :return:
        """
        return {
            "type": cluster_type,
            "url": url
        }

    @staticmethod
    def build_container_attributes(image, tag, checksum):
        """

        :param image:
        :param tag:
        :param checksum:
        :return:
        """
        return {
            "image": image,
            "tag": tag,
            "checksum": checksum
        }

    @staticmethod
    def build_server_attributes(
            server_id, server_type, cpu, gpu, memory, disk, max_run_time
    ):
        """

        :param server_id:
        :param server_type:
        :param cpu:
        :param gpu:
        :param memory:
        :param disk:
        :param max_run_time:
        :return:
        """
        return {
            "serverId": server_id,
            "serverType": server_type,
            "cpu": cpu,
            "gpu": gpu,
            "memory": memory,
            "disk": disk,
            "maxExecutionTime": max_run_time
        }

    @staticmethod
    def build_service_provider_attributes(
            provider_type, description, cluster, containers, servers
    ):
        """

        :param provider_type:
        :param description:
        :param cluster:
        :param containers:
        :param servers:
        :return:
        """
        return {
            "type": provider_type,
            "description": description,
            "environment": {
                "cluster": cluster,
                "supportedContainers": containers,
                "supportedServers": servers
            }
        }

    @staticmethod
    def create_compute_service_attributes(
            price, timeout, creator, date_published, provider_attributes):
        """

        :param price:
        :param timeout:
        :param creator:
        :param date_published:
        :param provider_attributes:
        :return:
        """
        return {
            "main": {
                "name": "dataAssetComputingServiceAgreement",
                "creator": creator,
                "datePublished": date_published,
                "price": str(price),
                "timeout": timeout,
                "provider": provider_attributes
            }
        }

    @staticmethod
    def _status_from_job_info(job_info):
        return {
            'ok': job_info['status'] not in (31, 32),
            'status': job_info['status'],
            'statusText': job_info['statusText']
        }

    @staticmethod
    def check_output_dict(output_def, consumer_account):
        config = ConfigProvider.get_config()
        default_output_def = {
            'nodeUri': config.keeper_url,
            'brizoUri': BrizoProvider.get_brizo().get_brizo_url(config),
            'brizoAddress': config.provider_address,
            'metadata': dict(),
            'metadataUri': config.aquarius_url,
            'secretStoreUri': config.secret_store_url,
            'owner': consumer_account.address,
            'publishOutput': 0,
            'publishAlgorithmLog': 0,
            'whitelist': [],
        }

        output_def = output_def if isinstance(output_def, dict) else dict()
        default_output_def.update(output_def)
        return default_output_def

    def create_compute_service_descriptor(self, attributes):
        """

        :param attributes:
        """
        brizo = BrizoProvider.get_brizo()
        config = ConfigProvider.get_config()
        compute_endpoint = brizo.get_compute_endpoint(config)
        template_id = self._keeper.get_agreement_template_id(ServiceTypes.CLOUD_COMPUTE)
        return ServiceDescriptor.compute_service_descriptor(attributes=attributes,
                                                            service_endpoint=compute_endpoint,
                                                            template_id=template_id)

    def order(self, did, consumer_account, algorithm_did=None, algorithm_meta=None, output=None, provider_address=None):
        """

        :param did:
        :param consumer_account:
        :param algorithm_did: str -- the asset did (of `algorithm` type) which consist of `did:op:` and
            the assetId hex str (without `0x` prefix)
        :param algorithm_meta: `AlgorithmMetadata` instance -- metadata about the algorithm being run if
            `algorithm` is being used. This is ignored when `algorithm_did` is specified.
        :param output: Output object to be used in publishing mechanism
        :param provider_address: ethereum account address of provider (optional)
        :return:
        """
        assert isinstance(consumer_account, Account), \
            f'Expected `consumer_account` of type `Account`, ' \
            f'got type `{type(consumer_account)}` and value `{consumer_account}'

        if algorithm_meta:
            assert isinstance(algorithm_meta, AlgorithmMetadata), \
                f'Expected `algorithm_meta` of type `AlgorithmMetadata`, ' \
                f'got type `{type(algorithm_meta)}` and value `{algorithm_meta}`.'
            assert algorithm_meta.is_valid(), f'`algorithm_meta` seems invalid'

        ddo = self._did_resolver.resolve(did)
        service = ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
        if not service:
            raise ValueError(f'order of compute service on asset {did} failed: '
                             f'this asset does not have a service of type {ServiceTypes.CLOUD_COMPUTE}.')
        agreement_id = self._agreements.new()
        logger.debug(f'about to request create `{service.type}` service agreement: {agreement_id}')
        # creating agreement will automatically fulfill the LockRewardCondition if the agreement is successful
        self._agreements.create(
            did,
            service.index,
            agreement_id,
            None,
            consumer_account.address,
            consumer_account,
            provider_address,
            auto_consume=False
        )

        if agreement_id and (algorithm_meta or algorithm_did):
            def _refund_callback(_price, _publisher_address, _condition_ids, _service_agreement):
                def do_refund(_agreement_id, _did, _consumer_account, *_):
                    refund_reward(
                        None, _agreement_id, _did, _service_agreement, _price,
                        _consumer_account, _publisher_address, _condition_ids, _condition_ids[2]
                    )

                return do_refund

            def run_compute_job(_, _agreement_id, _did, _account, _algo_did, _algo_meta, _output):
                if _algo_did or _algo_meta:
                    return self.start(_agreement_id, _account, _algo_did, _algo_meta, _output)

            publisher_address = Web3Provider.get_web3().toChecksumAddress(ddo.publisher)
            condition_ids = service.generate_agreement_condition_ids(
                agreement_id, ddo.asset_id, consumer_account.address, publisher_address, self._keeper)

            self._keeper.compute_execution_condition.subscribe_condition_fulfilled(
                agreement_id,
                max(service.condition_by_name['computeExecution'].timeout, 300),
                run_compute_job,
                (agreement_id, did, consumer_account, algorithm_did, algorithm_meta, output),
                timeout_callback=_refund_callback(
                    service.get_price(), publisher_address, condition_ids, service
                )
            )

        return agreement_id

    def start(self, agreement_id, consumer_account, algorithm_did=None,
              algorithm_meta=None, output=None, job_id=None):
        """

        :param agreement_id: hexstr -- representation of `bytes32` id
        :param consumer_account: Account instance of the consumer ordering the service
        :param algorithm_did: str -- the asset did (of `algorithm` type) which consist of `did:op:` and
            the assetId hex str (without `0x` prefix)
        :param algorithm_meta: `AlgorithmMetadata` instance -- metadata about the algorithm being run if
            `algorithm` is being used. This is ignored when `algorithm_did` is specified.
        :param output: dict object to be used in publishing mechanism, must define
        :param job_id: str identifier of a compute job that was previously started and
            stopped (if supported by the provider's  backend)
        :return: str -- id of compute job being executed
        """
        assert algorithm_did or algorithm_meta, 'either an algorithm did or an algorithm meta must be provided.'

        output = OceanCompute.check_output_dict(output, consumer_account)
        service_endpoint = self._get_service_endpoint_from_agreement(agreement_id)

        job_info = BrizoProvider.get_brizo().start_compute_job(
            agreement_id,
            service_endpoint,
            consumer_account.address,
            self._auth.get(consumer_account),
            algorithm_did,
            algorithm_meta,
            output,
            job_id
        )
        return job_info['jobId']

    def status(self, agreement_id, job_id, account):
        return OceanCompute._status_from_job_info(
            BrizoProvider.get_brizo().compute_job_status(
                agreement_id,
                job_id,
                self._get_service_endpoint_from_agreement(agreement_id),
                account.address,
                self._auth.get(account)
            )
        )

    def result(self, agreement_id, job_id, account):
        info_dict = BrizoProvider.get_brizo().compute_job_result(
            agreement_id,
            job_id,
            self._get_service_endpoint_from_agreement(agreement_id),
            account.address,
            self._auth.get(account),
        )
        return {
            'did': info_dict.get('resultsDid', ''),
            'urls': info_dict.get('resultsUrls', []),
            'logs': info_dict.get('algorithmLogUrl', [])
        }

    def stop(self, agreement_id, job_id, account):
        return self._status_from_job_info(
            BrizoProvider.get_brizo().stop_compute_job(
                agreement_id,
                job_id,
                self._get_service_endpoint_from_agreement(agreement_id),
                account.address,
                self._auth.get(account)
            )
        )

    def restart(self, agreement_id, job_id, account):
        return self._status_from_job_info(
            BrizoProvider.get_brizo().restart_compute_job(
                agreement_id,
                job_id,
                self._get_service_endpoint_from_agreement(agreement_id),
                account.address,
                self._auth.get(account),
            )
        )

    def delete(self, agreement_id, job_id, account):
        return self._status_from_job_info(
            BrizoProvider.get_brizo().delete_compute_job(
                agreement_id,
                job_id,
                self._get_service_endpoint_from_agreement(agreement_id),
                account.address,
                self._auth.get(account),
            )
        )

    def _get_service_endpoint_from_agreement(self, agreement_id, ddo=None):
        agreement = self._keeper.agreement_manager.get_agreement(agreement_id)
        _type = self._keeper.get_agreement_type(agreement.template_id)

        if not ddo:
            ddo = self._did_resolver.resolve(id_to_did(agreement.did))
        service = ServiceAgreement.from_ddo(_type, ddo)
        assert service, f'Using agreement_id {agreement_id}, the service type {_type} does not ' \
                        f'have a matching service in the DDO with DID {agreement.did}.'

        compute_service = ServiceAgreement.from_ddo(ServiceTypes.CLOUD_COMPUTE, ddo)
        assert service.service_endpoint == compute_service.service_endpoint, \
            f'`Expecting agreement of type `{ServiceTypes.CLOUD_COMPUTE}`, but `agreement_id` {agreement_id} ' \
            f'seems to have type {_type}.'

        return service.service_endpoint
