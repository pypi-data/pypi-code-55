import platform
from os import path
from subprocess import Popen, PIPE, STDOUT
import os
from time import sleep
from pathlib import Path

import requests
import zipfile

"""
implements the CBT tunnels binary as a Python object
example:
from cbttunnels.cbt_tunnels import CBTtunnel
tunnel = cbttunnels.CbtTunnel(username="you@email.com", authkey="yourauthkey")
//add delete_after=True to always ensure the newest tunnel binary
//add tunnel_location="path" to place the binary outside the local directory
//add ready_file="filename" to use a different ready file (this might be helpful for multiple tunnels)
//add kill_file="filename" to use a different kill file (this might be helpful for multiple tunnels)
tunnel.start_tunnel()
do_things()
tunnel.kill_tunnel()
"""
class CBTtunnel:
    def __init__(self,
                 username="",
                 authkey="",
                 delete_after=False,
                 tunnel_location=".",
                 ready_file="ready.check",
                 kill_file="kill.check"):
        self.TunnelBin = None
        self.Username = username
        self.Authkey = authkey
        self.ReadyFile = ready_file
        self.KillFile = kill_file
        self.FileName = get_file_name()
        self.DeleteAfter = delete_after
        self.TunnelLocation = tunnel_location
        self.Started = False
        if self.TunnelLocation == "." and platform.system == "Windows":
            self.FileLocation = self.FileName
        else:
            self.FileLocation = "%s/%s" % (self.TunnelLocation, self.FileName)
        self.BaseCmdString = "%s --username %s --authkey %s --ready %s --kill %s" % (self.FileLocation,
                                                                                     self.Username,
                                                                                     self.Authkey,
                                                                                     self.ReadyFile,
                                                                                     self.KillFile)
        self.ExtraCmdString = ""
        self.HTTPSProxy = None
        self.HTTPProxy = None
        self.Bypass = False
        self.TunnelName = None
        self.PACFile = None
        self.LocalHTMLPath = None
        self.ProxyServer = None
        self.ProxyUser = None
        self.ProxyPort = None
        self.ProxyPass = None
        self.AcceptAllCerts = False
        if self.check_file() is False:
            print("Could not find file %s in %s - downloading now" % (self.FileName, self.TunnelLocation))
            self.download_and_extract()

    def download_and_extract(self):
        self.download()
        self.extract()
    """
    downloads the zip file for the tunnel binary
    """
    def download(self):
        download_url = "https://crossbrowsertesting.com/downloads/%s.zip" % self.FileName
        r = requests.get(download_url)
        open("%s.zip" % self.FileLocation, 'wb').write(r.content)

    """
    extracts the zip file
    """
    def extract(self):
        with zipfile.ZipFile("%s.zip" % self.FileLocation) as tunnelzip:
            tunnelzip.extract(self.FileName, path=self.TunnelLocation)
        stat = os.stat(self.FileLocation)
        os.chmod(self.FileLocation, stat.st_mode | 0o0111 )

    """
    start the tunnel
    example: tunnel.start_tunnel()
    """
    def start_tunnel(self):
        if self.check_file() is False:
            self.download_and_extract()
        try:
            os.remove(self.KillFile)
        except OSError:
            print("kill file already removed")
        if self.Started is True:
            print("tunnel already started (or attempted)")
            return
        self.generate_extra_cmd()
        full_cmd = "%s %s" % (self.BaseCmdString, self.ExtraCmdString)
        print("running command %s" % full_cmd)
        self.TunnelBin = Popen(full_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if self.TunnelBin.poll() is not None:
            print("couldn't start")
            stdout, stderr = self.TunnelBin.communicate()
            print(stderr)
        self.wait_for_tunnel()

    """
    internal function to wait for a tunnel to create a ready file
    """
    def wait_for_tunnel(self):

        loop = 0
        while path.exists(self.ReadyFile) is not True:
            loop += 1
            if loop > 60:
                print("failed")

            sleep(3)
    """
    kill a tunnel cleanly
    example: tunnel.kill_tunnel()
    """
    def kill_tunnel(self):
        Path(self.KillFile).touch()
        stdout, stderr = self.TunnelBin.communicate()
        self.Started = False
        if self.DeleteAfter is True:
            os.remove(self.FileLocation)

    """
    builds the extra options used beyond the bare minimum
    """
    def generate_extra_cmd(self):
        build_string = []
        if self.HTTPSProxy is not None:
            build_string.append("--httpsProxy %s" % self.HTTPSProxy)
        if self.HTTPProxy is not None:
            build_string.append("--httpProxy %s" % self.HTTPProxy)
        if self.TunnelName is not None:
            build_string.append("--tunnelname %s" % self.TunnelName)
        if self.PACFile is not None:
            build_string.append("--pac %s" % self.PACFile)
        if self.LocalHTMLPath is not None:
            build_string.append("--dir %s" % self.LocalHTMLPath)
        if self.ProxyServer is not None and self.ProxyPort is not None:
            build_string.append("--proxyIp %s --proxyPort %s" % (self.ProxyServer, self.ProxyPort))
            if self.ProxyUser is not None and self.ProxyPass is not None:
                build_string.append("--proxyUser %s --proxyPass %s" % (self.ProxyUser, self.ProxyPass))
        if self.AcceptAllCerts is True:
            build_string.append("--acceptAllCerts")
        build_string.append("--bypass %s" % self.Bypass)
        self.ExtraCmdString = " ".join(build_string)

    """
    sets bypass settings (equivalent of --bypass)
    example: tunnel.bypass(True)
    only sets if passed a bool
    """
    def bypass(self, setting):
        if isinstance(setting, bool):
            self.Bypass = setting

    """
    sets the HTTPS proxy (--httpsProxy)
    example: tunnel.set_https_proxy("https://proxy.com")
    """
    def set_https_proxy(self, proxy):
        self.HTTPSProxy = proxy

    """
    sets the HTTP proxy (--httpProxy)
    example: tunnel.set_http_proxy("https://proxy.com")
    """
    def set_http_proxy(self, proxy):
        self.HTTPProxy = proxy

    """
    sets the tunnel name
    example: tunnel.set_tunnel_name("tunnel1")
    """
    def set_tunnel_name(self, tunnel_name):
        self.TunnelName = tunnel_name

    """
    sets the PAC file to use for resolution
    example: tunnel.set_pac_file("path")
    """
    def set_pac_file(self, path):
        self.PACFile = path

    """
    sets the local path to serve HTML files from
    example: tunnel.set_html_path("/path/to/html")
    """
    def set_html_path(self, path):
        self.LocalHTMLPath = path

    """
    sets a proxy to use for tunnel traffic
    example: tunnel.set_proxy(host="host", port="port", username=None, password=None)
    username and password can be blank or filled in and will only be added when they are both filled
    """
    def set_proxy(self, host="", port="", username=None, password=None):
        self.ProxyServer = host
        self.ProxyPort = port
        self.ProxyUser = username
        self.ProxyPass = password
    """
    set the acceptAllCerts option to setting
    example: tunnel.set_accept_all_certs(setting=True)
    this will turn on acceptAllCerts 
    """
    def set_accept_all_certs(self, setting=False):
        self.AcceptAllCerts = setting
    """
    check to see if the binary exists
    """
    def check_file(self):
        return path.exists(self.FileLocation)

"""
gets the filename to use for a given platform and architecture
"""
def get_file_name():
    system = platform.system()
    os = None
    suffix = ""
    prefix = "cbt_tunnel"
    if system == "Windows":
        os = "win"
        suffix = ".exe"
    elif system == "Darwin":
        os = "macos"
    else:
        os = "linux"
    arch = None
    if os == "win":
        prefix = "cbttunnels"
        reported_arch = platform.machine()
        if reported_arch == "AMD64":
            arch = "x64"
        else:
            arch = "x86"
    else:
        arch = "x64"
    return "%s-%s-%s%s" % (prefix, os, arch, suffix)
