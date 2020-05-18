import os
import pytest
import requests_mock as requests_mock_module
import shutil

from enough import settings
from enough.common import service


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_openstack_create_or_update(tmpdir, openstack_name, requests_mock):
    shutil.copy('infrastructure_key', f'{tmpdir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{tmpdir}/infrastructure_key.pub')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    requests_mock.get(requests_mock_module.ANY, status_code=200)
    domain = f'enough.test'
    s = service.ServiceOpenStack(str(tmpdir), settings.SHARE_DIR, **{
        'driver': 'openstack',
        'playbook': os.path.abspath('tests/enough/common/test_common_service/enough-playbook.yml'),
        'domain': domain,
        'name': 'essential',
    })
    s.dotenough.set_certificate('ownca')
    s.dotenough.set_clouds_file('inventory/group_vars/all/clouds.yml')
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'
    # the second time around the hosts.yml are reused
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'


def test_service_from_host(tmpdir):
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR)
    assert s.service_from_host('bind-host') == 'essential'
    assert s.service_from_host('cloud-host') == 'cloud'
    assert s.service_from_host('unknown-host') is None
