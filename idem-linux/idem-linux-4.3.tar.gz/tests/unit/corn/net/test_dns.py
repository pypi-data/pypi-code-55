import dns.resolver
import idem_linux.corn.net.dns
import io
import pytest
import unittest.mock as mock

RESOLV_CONF = """
domain test.domain
options rotate timeout:1 retries:1
search example.com company.net
nameserver 10.0.0.1
nameserver 10.0.0.2
nameserver fe80::1
"""


class TestDns:
    @pytest.mark.asyncio
    async def test_load_dns(self, c_hub):
        mocK_resolv = dns.resolver.Resolver(io.StringIO(RESOLV_CONF), configure=True)
        mocK_resolv.read_resolv_conf = lambda x: 0

        with mock.patch.object(dns.resolver, "Resolver", return_value=mocK_resolv):
            await idem_linux.corn.net.dns.load_dns(c_hub)

        assert c_hub.corn.CORN.dns.nameservers == ("10.0.0.1", "10.0.0.2", "fe80::1")
        assert c_hub.corn.CORN.dns.ip4_nameservers == ("10.0.0.1", "10.0.0.2")
        assert c_hub.corn.CORN.dns.ip6_nameservers == ("fe80::1",)
        assert c_hub.corn.CORN.dns.sortlist == (
            "10.0.0.0/8",
            "10.0.0.0/8",
            "fe80::1/128",
        )
        assert c_hub.corn.CORN.dns.domain == "test.domain."
        assert c_hub.corn.CORN.dns.search == ("example.com.", "company.net.")
        assert c_hub.corn.CORN.dns.options.rotate is True
