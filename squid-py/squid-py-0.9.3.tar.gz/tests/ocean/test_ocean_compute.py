#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
import uuid

from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes

from squid_py.brizo import BrizoProvider
from squid_py.brizo.brizo import Brizo

from squid_py.models.algorithm_metadata import AlgorithmMetadata
from squid_py.secret_store import SecretStoreProvider
from squid_py.secret_store.secret_store import SecretStore

from tests.resources.helper_functions import (
    get_resource_path,
)

from ocean_utils.ddo.ddo import DDO


def test_order(publisher_ocean_instance, consumer_ocean_instance):
    consumer_account = consumer_ocean_instance.main_account
    publisher_account = publisher_ocean_instance.main_account
    keeper = publisher_ocean_instance.keeper
    ocean = consumer_ocean_instance
    BrizoProvider.set_brizo_class(Brizo)

    SecretStoreProvider.set_secret_store_class(SecretStore)
    sample_ddo_path = get_resource_path('ddo', 'ddo_with_compute_service.json')
    old_ddo = DDO(json_filename=sample_ddo_path)
    metadata = old_ddo.metadata
    metadata['main']['files'][0]['checksum'] = str(uuid.uuid4())
    template_name = keeper.template_manager.SERVICE_TO_TEMPLATE_NAME[ServiceTypes.CLOUD_COMPUTE]
    service = old_ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
    brizo = BrizoProvider.get_brizo()
    compute_service = ServiceDescriptor.compute_service_descriptor(
        service.attributes,
        brizo.get_compute_endpoint(ocean.config),
        keeper.template_manager.create_template_id(template_name)
    )
    compute_ddo = publisher_ocean_instance.assets.create(
        metadata,
        publisher_account,
        providers=[],
        service_descriptors=[compute_service],
    )
    did = compute_ddo.did

    _compute_ddo = publisher_ocean_instance.assets.resolve(compute_ddo.did)
    algorithm_ddo_path = get_resource_path('ddo', 'ddo_sample_algorithm.json')
    algo_main = DDO(json_filename=algorithm_ddo_path).metadata['main']
    algo_meta_dict = algo_main['algorithm'].copy()
    algo_meta_dict['url'] = algo_main['files'][0]['url']
    algorithm_meta = AlgorithmMetadata(algo_meta_dict)

    try:
        ocean.accounts.request_tokens(publisher_account, 50*keeper.dispenser.get_scale())
    except Exception as err:
        print(f'Requesting tokens failed: {err}')

    agreement_id = ocean.compute.order(
        compute_ddo.did,
        consumer_account,
        None,
        None
    )

    assert agreement_id, f'got agreementId {agreement_id}'

    def fulfill_compute_execution(_, ocn_instance, agr_id, _did, cons_address, account):
        ocn_instance.agreements.conditions.grant_compute(
            agr_id, _did, cons_address, account)

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id,
        15,
        fulfill_compute_execution,
        (publisher_ocean_instance, agreement_id, compute_ddo.did,
         consumer_account.address, publisher_account),
        from_block=0,
        wait=True
    )
    assert event, f'lock condition event is not found.'

    print(f'processed agreement and got lockReward fulfilled: '
          f'{agreement_id}, {compute_ddo.did}, ')
    event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
        agreement_id,
        20,
        None,
        (agreement_id, compute_ddo.did, consumer_account, None, algorithm_meta),
        from_block=0,
        wait=True
    )
    assert event, f'compute execution condition event is not found.'

    job_id = consumer_ocean_instance.compute.start(agreement_id, consumer_account, algorithm_meta=algorithm_meta)
    assert job_id, f'expected a job id, got {job_id}'

    status = consumer_ocean_instance.compute.status(agreement_id, job_id, consumer_account)
    print(f'got job status: {status}')
    assert status and status['ok'], f'something not right about the compute job, got status: {status}'

    status = consumer_ocean_instance.compute.stop(agreement_id, job_id, consumer_account)
    print(f'got job status after requesting stop: {status}')
    assert status, f'something not right about the compute job, got status: {status}'

    # time.sleep(5)
    # status = consumer_ocean_instance.compute.status(agreement_id, job_id, consumer_account)
    # print(f'got job status: {status}')
    # assert status and status['statusText'] == 'Job stopped', f'something not right about the compute job, got status: {status}'
