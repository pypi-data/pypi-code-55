#  Copyright (c) 2020 Netflix.
#  All rights reserved.
from typing import Dict

# Implementation libs
from ntscli_cloud_lib.device_identifier import DeviceIdentifier
from ntscli_cloud_lib.log import logger


class TestPlanChecker:
    """
    Check the format of a test plan run request.

    This is a convenience class and not strictly required,
    but helps shortcut failed requests to the cloud.
    """

    @staticmethod
    def sanity_check(plan: Dict) -> bool:
        """Perform a basic sanity check on a dict to see if it's mostly the right shape for a request."""
        results = [DeviceIdentifier.sanity_check(plan)]

        try:
            if "testplan" in plan:
                if "testcases" not in plan["testplan"]:
                    logger.error("The testplan is missing the key 'testcases'")
                results.append("testcases" in plan["testplan"])

                if not type(plan["testplan"]["testcases"]) is list:
                    logger.error("The test plan member 'testcases' is not a list")
                results.append(type(plan["testplan"]["testcases"]) is list)

                if len(plan["testplan"]["testcases"]) <= 0:
                    logger.error("The test cases list is present, but empty")
                results.append(len(plan["testplan"]["testcases"]) > 0)
            else:
                logger.error("The key 'testplan' is missing in the request to the automator")
                results.append(False)
        except KeyError:
            results.append(False)
        except TypeError:
            results.append(False)
        except ValueError:
            results.append(False)

        return all(results)
