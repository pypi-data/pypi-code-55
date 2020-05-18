def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",
        default="infrastructure1-host,infrastructure2-host,infrastructure3-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service-directory",
        action="store",
        default="infrastructure",
        help="service directory"
    )
