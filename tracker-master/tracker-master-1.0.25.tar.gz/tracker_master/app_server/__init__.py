import logging
import sys

from tracker_master import config as CFG
import tracker_master.util as util
from tracker_master.app_server.configure import ServerConfigurer
from tracker_master.app_server.configure import ProductionConfiguration

DEFAULT_PROFILE_NAME = 'development'

if __name__ == "__main__":
    # Take profile name from args
    profile_name = None
    if len(sys.argv) == 1:
        profile_name = DEFAULT_PROFILE_NAME
    else:
        profile_name = sys.argv[1]

    # Read configure with profile
    CFG.read("../conf/app_server_config.yaml", profile_name)

    # Setup loggin
    util.setup_logging()
    logger = logging.getLogger(__name__)

    # Run configure
    server_configure = ServerConfigurer(CFG.zbx_api_url(), CFG.zbx_user(), CFG.zbx_pwd(), ProductionConfiguration())
    server_configure.configure()
