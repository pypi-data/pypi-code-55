import pytest

from dscitools import ipython as ip

def test_me(monkeypatch):
    def mock_now():
        return "abc"
    monkeypatch.setattr(ip, "now", mock_now)
    ip.print_status("hello")
    assert False

def test_other():
    ip.print_status("hello")
    assert False
