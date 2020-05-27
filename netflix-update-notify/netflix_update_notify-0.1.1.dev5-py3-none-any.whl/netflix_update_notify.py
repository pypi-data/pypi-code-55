import atexit
import logging
import re
from threading import Thread

import requests
import semver

# Implementation libs
from pkg_info import get_pkg_info


class UpdateNotifier(object):
    """Loosely based on update-notipy public module"""

    pattern = r"\d+\.\d+\.\d+"

    def __init__(self, name: str, version: str):
        """Set the package and SemVer string for what to check."""
        self.name: str = name
        self.version: str = version
        # version strings are too wild - limit ourselves to the first 1.2.3 or 11.22.33
        found_parts = re.findall(UpdateNotifier.pattern, version)
        if len(found_parts) > 0:
            self.version = found_parts[0]

    def notify(self) -> None:
        """Set up a notification for the user on process exit if updates exist."""
        pkg = get_pkg_info(self.name)
        latest = pkg.version
        found_parts = re.findall(UpdateNotifier.pattern, latest)
        if len(found_parts) > 0:
            latest = found_parts[0]
        if semver.VersionInfo.parse(self.version).compare(latest) >= 0:
            return
        else:
            action, arg = (
                logging.warning,
                f"{self.name} update available {self.version} → {latest}. Run\npip install -U {self.name}",
            )
        atexit.register(action, arg) if arg else atexit.register(action)

    @staticmethod
    def _notify_version_thread(package: str, version: str):
        try:
            if package is None or package == "" or version is None or version == "":
                return
            UpdateNotifier(package, version).notify()
        except (requests.exceptions.HTTPError, ValueError) as ee:
            # early prereleases do this due to SemVer version number requirements
            logging.debug(f"Checking for updates for {package} failed, but this is not fatal\n{ee}")

    @staticmethod
    def notify_of_updates(package: str, version: str):
        update_checker = Thread(target=UpdateNotifier._notify_version_thread, kwargs={"package": package, "version": version})
        update_checker.start()
        atexit.register(update_checker.join)
