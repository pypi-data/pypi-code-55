from os import path


def test_init_function():
    File1 = path.exists("./mypackage_wsc/infra_builder_terraform.py")
    File2 = path.exists("./mypackage_wsc/infra_bootstrap.py")
    File3 = path.exists("./mypackage_wsc/install_nginx.py")
    assert File1
    assert File2
    assert File3