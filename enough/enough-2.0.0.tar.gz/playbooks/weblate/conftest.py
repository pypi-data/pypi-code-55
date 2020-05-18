def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,postfix-host,icinga-host,weblate-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service-directory",
        action="store",
        default="weblate",
        help="service directory"
    )
