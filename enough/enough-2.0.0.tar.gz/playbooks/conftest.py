import os
import pytest
import shutil
import textwrap

from enough.common import Enough


def pytest_addoption(parser):
    parser.addoption(
        "--enough-no-create",
        action="store_true",
        help="Do not run the create step"
    )
    parser.addoption(
        "--enough-no-tests",
        action="store_true",
        help="Do not run the tests step"
    )
    parser.addoption(
        "--enough-no-destroy",
        action="store_true",
        help="Do not run the destroy step"
    )


def pytest_configure(config):
    pass


def prepare_config_dir(domain):
    os.environ['ENOUGH_DOMAIN'] = domain
    config_dir = os.path.expanduser(f'~/.enough/{domain}')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    shutil.copy('infrastructure_key', f'{config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{config_dir}/infrastructure_key.pub')
    all_dir = f'{config_dir}/inventory/group_vars/all'
    if not os.path.exists(all_dir):
        os.makedirs(all_dir)
    shutil.copyfile('inventory/group_vars/all/clouds.yml', f'{all_dir}/clouds.yml')
    shutil.copyfile('inventory/group_vars/all/provision.yml', f'{all_dir}/provision.yml')
    open(f'{all_dir}/certificate.yml', 'w').write(textwrap.dedent(f"""\
    ---
    certificate_authority: letsencrypt_staging
    """))
    return config_dir


def pytest_sessionstart(session):
    if session.config.getoption("--enough-no-create"):
        return

    service_directory = session.config.getoption("--enough-service-directory")
    domain = f'{service_directory}.test'
    config_dir = prepare_config_dir(domain)

    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               inventory=[f'playbooks/{service_directory}/inventory'])
    names = session.config.getoption("--enough-hosts")
    public_key = f'{e.config_dir}/infrastructure_key.pub'
    r = e.heat.create_missings(names.split(','), public_key)
    if len(r) > 0:
        e.heat.create_test_subdomain('enough.community')
    e.playbook.run([
        '--private-key', f'{e.config_dir}/infrastructure_key',
        '-i', f'playbooks/{service_directory}/inventory',
        f'--limit={names},localhost',
        f'playbooks/{service_directory}/playbook.yml',
    ])


def pytest_runtest_setup(item):
    if item.config.getoption("--enough-no-tests"):
        pytest.skip("--enough-no-tests specified, skipping all tests")


def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption("--enough-no-destroy"):
        return

    if exitstatus != 0:
        return

    service_directory = session.config.getoption("--enough-service-directory")
    names = session.config.getoption("--enough-hosts").split(',')
    domain = f'{service_directory}.test'
    config_dir = os.path.expanduser(f'~/.enough/{domain}')
    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               name=names,
               inventory=[f'playbooks/{service_directory}/inventory'])
    e.host.delete()


def pytest_unconfigure(config):
    pass
