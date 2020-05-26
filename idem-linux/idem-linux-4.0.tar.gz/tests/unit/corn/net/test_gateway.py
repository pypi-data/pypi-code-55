import idem_linux.corn.net.gateway
import pytest
import shutil
import unittest.mock as mock

IP4_DATA = """
default via 192.168.1.1 dev wlp59s0 proto dhcp metric 20600
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
192.168.1.0/24 dev wlp59s0 proto kernel scope link src 192.168.1.27 metric 600
"""
IP6_DATA = """
::1 dev lo proto kernel metric 256 pref medium
fe80::/64 dev wlp59s0 proto kernel metric 600 pref medium
"""


class TestGateway:
    @pytest.mark.asyncio
    async def test_load_default_gateway(self, c_hub):
        c_hub.exec.cmd.run.side_effect = [
            c_hub.pop.data.imap({"stdout": IP4_DATA}),
            c_hub.pop.data.imap({"stdout": IP6_DATA}),
        ]

        with mock.patch.object(shutil, "which", return_value=True):
            await idem_linux.corn.net.gateway.load_default_gateway(c_hub)

        assert c_hub.corn.CORN.ip_gw is True
        assert c_hub.corn.CORN.ip4_gw == "192.168.1.1"
        assert c_hub.corn.CORN.ip6_gw is False
