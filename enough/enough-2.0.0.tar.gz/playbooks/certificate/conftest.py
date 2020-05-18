def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,letsencryptstaging-host,owncanotweb-host,client-host,ownca-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service-directory",
        action="store",
        default="certificate",
        help="service directory"
    )
