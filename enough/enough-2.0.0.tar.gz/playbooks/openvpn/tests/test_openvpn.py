testinfra_hosts = ['ansible://openvpnclient-host']


def test_vpn_route(host):
    cmd = host.run("ip route")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert '10.11.12' in cmd.stdout
