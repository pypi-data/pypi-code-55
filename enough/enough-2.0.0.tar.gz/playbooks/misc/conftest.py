def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="debian-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service-directory",
        action="store",
        default="misc",
        help="service directory"
    )
