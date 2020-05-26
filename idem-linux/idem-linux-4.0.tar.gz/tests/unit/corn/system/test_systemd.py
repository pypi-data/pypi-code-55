import idem_linux.corn.system.systemd
import io
import pytest
import unittest.mock as mock

SYSTEMD_DATA = """
systemd 245 (245.4-2-manjaro)
+PAM +AUDIT -SELINUX -IMA -APPARMOR +SMACK -SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD +IDN2 -IDN +PCRE2 default-hierarchy=hybrid
"""


@pytest.mark.asyncio
class TestSystemd:
    async def test_load_systemd(self, c_hub):
        c_hub.exec.cmd.run.return_value = c_hub.pop.data.imap({"stdout": SYSTEMD_DATA})
        await idem_linux.corn.system.systemd.load_systemd(c_hub)
        assert c_hub.corn.CORN.systemd.version == "245"
        assert (
            c_hub.corn.CORN.systemd.features
            == "+PAM +AUDIT -SELINUX -IMA -APPARMOR +SMACK -SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD +IDN2 -IDN +PCRE2 default-hierarchy=hybrid"
        )

    async def test_load_init_systemd(self, c_hub):
        with mock.patch("shutil.which", return_value=False):
            with mock.patch("os.path.exists", return_value=True):
                with mock.patch("os.stat", return_value=True):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "systemd"

    async def test_load_init_upstart(self, c_hub):
        c_hub.OPT = {}
        with mock.patch("shutil.which", return_value="/bin/init"):
            with mock.patch("os.path.exists", side_effect=[False, True]):
                with mock.patch(
                    "aiofiles.threadpool.sync_open",
                    side_effect=[
                        io.StringIO("1\x00"),
                        io.StringIO("this is an upstart\x00init"),
                    ],
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "upstart"

    async def test_load_init_sysvinit(self, c_hub):
        c_hub.OPT = {}
        with mock.patch("shutil.which", return_value="/bin/init"):
            with mock.patch("os.path.exists", side_effect=[False, True]):
                with mock.patch(
                    "aiofiles.threadpool.sync_open",
                    side_effect=[
                        io.StringIO("1\x00"),
                        io.StringIO("this is an sysvinit\x00init"),
                    ],
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "sysvinit"

    async def test_load_init_systemdb(self, c_hub):
        c_hub.OPT = {}
        with mock.patch("shutil.which", return_value="/bin/init"):
            with mock.patch("os.path.exists", side_effect=[False, True]):
                with mock.patch(
                    "aiofiles.threadpool.sync_open",
                    side_effect=[
                        io.StringIO("1\x00"),
                        io.StringIO("this is an systemd\x00init"),
                    ],
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "systemd"

    async def test_load_init_supervisord(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /test/bin/supervisord\x00"),
            ):
                with mock.patch("shutil.which", return_value="/test/bin/supervisord"):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "supervisord"

    async def test_load_init_dumb_init(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /test/bin/dumb-init\x00"),
            ):
                with mock.patch(
                    "shutil.which", side_effect=["", "", "/test/bin/dumb-init"]
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "dumb-init"

    async def test_load_init_tini(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /test/bin/tini\x00"),
            ):
                with mock.patch(
                    "shutil.which", side_effect=["", "", "", "/test/bin/tini"]
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "tini"

    async def test_load_init_runit(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /test/bin/init\x00runit"),
            ):
                with mock.patch(
                    "shutil.which", side_effect=["", "", "", "", "/test/bin/runit"]
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "runit"

    async def test_load_init_my_init(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /sbin/my_init\x00"),
            ):
                with mock.patch(
                    "shutil.which", side_effect=["", "", "", "", "", "/sbin/my_init"]
                ):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "runit"

    async def test_load_init(self, c_hub):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO("init /test/bin/unknown\x00"),
            ):
                with mock.patch("shutil.which", return_value=""):
                    await idem_linux.corn.system.systemd.load_init(c_hub)
        assert c_hub.corn.CORN.init == "unknown"
