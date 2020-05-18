"""This module acts as wrapper for the nqc binary."""

import subprocess

from pynqc.raw_functions import RawFunctions

NQC_BIN = "nqc"


def _exec_nqc(cmds):
    """Execute nqc binary with provided commands."""
    nqc_cmds = [NQC_BIN]
    nqc_cmds.extend(cmds)
    err = None
    data = None
    try:
        data = subprocess.check_output(nqc_cmds, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        err = e

    if err:
        msg = None
        if err.returncode == 238:
            msg = f"{err.stderr}\nFirmware incompatible, install compatible version"
        if err.returncode == 239:
            msg = f"{err.stderr}\nCompilation error\n{err}"
        if err.returncode == 252:
            msg = f"{err.stderr}\nInvalid opcode format"
        if err.returncode == 253:
            msg = (
                f"{err.stderr}\nDevice too far away\nnot turned on"
                f"\nbad channel\nor firmware not installed/supporting request"
            )
        if err.returncode == 255:
            msg = f"{err.stderr}\nConnect IR tower"
        raise IOError(err.returncode, msg)

    return data


class Nqc:
    """This class provides a python api for the nqc binary.

    It stores the serial device as internal state.
    """

    def __init__(self, serial_type="usb", device="/dev/usb/legousbtower0"):
        """Initialize nqc wrapper with serial type."""
        self.serial_type = serial_type
        self.device = device

    def _get_device(self):
        return f"-S{self.serial_type}:{self.device}"

    def exec_raw(self, payload):
        """Execute raw commands."""
        cmds = [self._get_device(), "-raw", f"{payload}"]
        data = _exec_nqc(cmds)
        return data

    def send_msg(self, payload):
        """Send message, accepted values between 0 and 255."""
        data = _exec_nqc([self._get_device(), "-msg", f"{payload}"])
        return True if data == b"" else False

    def set_program_slot(self, slot):
        """Activeate a program slot."""
        if slot > 5 or slot < 1:
            raise ValueError(
                f"slot {slot} was given, only values between 1 and 5 accepted"
            )
        cmds = [self._get_device(), "-pgm", f"{slot}"]
        data = _exec_nqc(cmds)
        return True if data == b"" else False

    def flash_firmware(self, path, fast=False):
        """Download firmware to device."""
        cmd = "-firmware"
        if fast:
            cmd = "-firmfast"
        data = _exec_nqc([self._get_device(), cmd, path])
        return True if data == b"" else False

    def flash_and_exec_application(self, path, flags=[]):
        """Download application the current program slot and run it."""
        download_pgm = "-d"
        cmds = [self._get_device(), *flags, download_pgm, path, "-run"]
        data = _exec_nqc(cmds)
        return True if data == b"" else False

    def get_raw_functions(self):
        """Return an api object for executing op codes on the device."""
        return RawFunctions(self)
