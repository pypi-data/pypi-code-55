# Copyright (C) 2016 Red Hat
#
# relvalconsumer is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <awilliam@redhat.com>

"""fedora-messaging consumer to create release validation events."""

import logging
import smtplib
import subprocess
import sys
import time

import fedfind.exceptions
import fedfind.helpers
import fedora_messaging.config
import fedora_messaging.exceptions
import hawkey
import mwclient.errors
import wikitcms.event
import wikitcms.wiki

from urllib.error import URLError, HTTPError

__version__ = "2.2.0"


class RelvalAMIConsumer(object):
    """A fedora-messaging consumer that updates the AMI info page for
    a release validation test event when a relevant AMI is published.
    """

    def __init__(self):
        self.relvalami_prod = fedora_messaging.config.conf["consumer_config"]["relvalami_prod"]
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, message):
        """Consumer incoming message. relvalami_prod' indicates prod
        or test mode. Message should be a fedimg.image.publish.
        """
        if self.relvalami_prod:
            serv = "fedoraproject.org"
        else:
            serv = "stg.fedoraproject.org"
        site = wikitcms.wiki.Wiki(serv, "/w/")
        site.login()
        cid = message.body.get("compose")
        if not cid:
            self.logger.warning("No compose ID found, this is unexpected...")
            raise fedora_messaging.exceptions.Drop
        try:
            event = site.get_validation_event(cid=cid)
        except fedfind.exceptions.UnsupportedComposeError:
            # this is a common, expected case, not worth logging at info
            self.logger.debug("compose %s not supported by fedfind", cid)
            raise fedora_messaging.exceptions.Drop
        except ValueError:
            self.logger.info("Could not determine event for compose %s", cid)
            raise fedora_messaging.exceptions.Drop
        self.logger.info("Working on AMI %s for compose %s", message.body["extra"]["id"], cid)
        if event.result_pages:
            # this is a proxy for 'event exists for this compose'; if
            # so, we'll just re-create the AMI page from scratch, we
            # don't have the capability to smartly add a single AMI
            event.ami_page.write(createonly=None)


class RelvalConsumer(object):
    """A fedora-messaging consumer that creates release validation
    test events for new composes when appropriate.
    """

    def __init__(self):
        self.relval_prod = fedora_messaging.config.conf["consumer_config"]["relval_prod"]
        self.relval_bugzilla = fedora_messaging.config.conf["consumer_config"]["relval_bugzilla"]
        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, message):
        """Consume incoming message. 'relval_prod' indicates prod or
        test mode.
        """
        # only run on completed composes
        status = message.body.get("status", "")
        cid = message.body.get("compose_id")
        if "FINISHED" not in status or not cid:
            return

        # some compose info we'll use
        try:
            (dist, rel, date, typ, _) = fedfind.helpers.parse_cid(cid, dist=True)
        except ValueError as err:
            self.logger.error("fedfind could not parse cid %s:", cid)
            self.logger.error(err)
            raise fedora_messaging.exceptions.Drop

        # these are the only dists we want to create events for ATM
        if dist not in ("Fedora", "Fedora-IoT"):
            return

        if self.relval_prod:
            serv = "fedoraproject.org"
        else:
            serv = "stg.fedoraproject.org"
        site = wikitcms.wiki.Wiki(("https", serv), "/w/")
        site.login()

        # get the validation event instance
        try:
            event = site.get_validation_event(cid=cid)
        except fedfind.exceptions.UnsupportedComposeError:
            # this is a common, expected case, not worth logging at info
            self.logger.debug("compose %s not supported by fedfind", cid)
            return
        except ValueError:
            self.logger.info("Could not determine event for compose %s", cid)
            return
        self.logger.info("Working on compose %s", cid)

        # FIXME: we might want to put some 'are there sufficient
        # images for testing' heuristic in here, or even wait for
        # openQA results and bail if they all failed

        # at present we should only ever create events for exactly the
        # release after the current stable release; this prevents us
        # creating Rawhide events during Branched periods. Note we have
        # to handle the case of creating the *first* Rawhide nightly
        # after a stable release, so we cannot just require release to
        # equal wiki.current_compose['release']
        curr = fedfind.helpers.get_current_release()
        if not int(event.release) == curr + 1:
            self.logger.info("Compose %s is not for the next release!", cid)
            return

        currev = site.get_current_event(dist=dist)
        if currev:
            try:
                newdate = fedfind.helpers.date_check(date, out="obj")
                currdate = fedfind.helpers.date_check(currev.creation_date, out="obj")
            except ValueError:
                self.logger.warning("Could not determine date of current or new event!")
                return

        if typ not in ("nightly", "production"):
            self.logger.warning("Unexpected compose type %s for compose %s", typ, cid)
            return

        # FLOW NOTE: at this point if the event release is newer than
        # the current event release, we do no further checks and just
        # create the event. This should occur once per cycle just
        # after GA and create the first Rawhide nightly event for the
        # next release.
        diff = ""

        if typ == "production" and currev and event.release == currev.release:
            # just check we're actually newer than the current event as a
            # sanity check
            ok = True
            if newdate < currdate:
                ok = False
            # for same date, check the sorttuple as a tie-breaker, so
            # two 'production' events on the same day *do* get created
            if newdate == currdate and event.sorttuple <= currev.sorttuple:
                ok = False
            if not ok:
                self.logger.warning(
                    "New event %s would not be newer than " "current event %s!",
                    event.version,
                    currev.version,
                )
                return

        # if we're proposing a nightly event for the same release, do the
        # date check / package comparison stuff. We treat IoT composes as
        # nightlies always, even though their type is production
        if (
            (typ == "nightly" or dist == "Fedora-IoT")
            and currev
            and event.release == currev.release
        ):
            delta = newdate - currdate
            if delta.days < 3:
                # we never create an event if it's been < 3 days.
                self.logger.info("Less than three days since current event.")
                return
            elif delta.days > 14:
                # we *always* create an event if it's been > 14 days.
                self.logger.debug("More than two weeks since current event!")
            else:
                # between 3 and 14 we check if important packages have changed.
                self.logger.debug("Comparing package versions...")
                packages = ["anaconda", "python-blivet", "pyparted", "parted", "pykickstart"]
                if dist != "Fedora-Modular":
                    # we can't find these in modular composes for now
                    packages.extend(["lorax", "pungi"])
                # this is awful, but there's a race between PDC fedmsg
                # emission and database commit (per threebean) so we
                # should sleep a bit before trying to talk to PDC.
                time.sleep(10)
                try:
                    currpacks = currev.ff_release.get_package_nvras(packages)
                    newpacks = event.ff_release.get_package_nvras(packages)
                except (ValueError, URLError, HTTPError):
                    self.logger.info("Package version check failed!")
                    return
                if not currpacks:
                    self.logger.info("Could not do package version check on current compose!")
                    return
                if not newpacks:
                    self.logger.info("Could not do package version check on new compose!")
                    return
                for key in list(currpacks.keys()):
                    if not currpacks[key] or not newpacks[key]:
                        self.logger.info(
                            "Could not find versions for all significant "
                            "packages in both composes!"
                        )
                        return
                if currpacks == newpacks:
                    self.logger.info("No significant package changes since current event.")
                    return
                else:
                    # check that packages are *newer*, not older (this is to
                    # guard against creating a nightly event after a candidate
                    # event with older packages; it's not perfect, though)
                    for package in list(currpacks.keys()):
                        currnevra = hawkey.split_nevra(currpacks[package])
                        newnevra = hawkey.split_nevra(newpacks[package])
                        if newnevra < currnevra:
                            self.logger.info(
                                "Package %s older in new event! New: %s " "Old: %s",
                                package,
                                newpacks[package],
                                currpacks[package],
                            )
                            return
                    self.logger.info("Significant package updates since current event!")
                    # this means we're carrying on.
                    diff = ""
                    for key in list(currpacks.keys()):
                        if currpacks[key] != newpacks[key]:
                            diff += "{0} - {1}: {2}, {3}: {4}\n".format(
                                key, currev.compose, currpacks[key], event.compose, newpacks[key]
                            )

        self.logger.info("Creating validation event %s", event.version)
        try:
            event.create(check=True)
        except mwclient.errors.APIError as err:
            self.logger.warning("Mediawiki error creating event!")
            self.logger.debug("Error: %s", err)
            return
        except ValueError:
            self.logger.warning("Existing page found for event! Aborting.")
            return

        # Run the image size check (this is as good a place as any)
        # FIXME: don't do this for IoT yet, we don't have a place to
        # report the results...
        if dist == "Fedora":
            args = ["relval", "size-check", "--cid", cid]
            if self.relval_bugzilla:
                # submit bug reports for oversize images
                args.append("--bugzilla")
            if not self.relval_prod:
                # edit stg wiki, submit bugs to partner-bugzilla
                args.append("--test")
            try:
                ret = subprocess.call(args)
                if ret > 0:
                    self.logger.warning("Size check failed")
                else:
                    self.logger.debug("Size check completed")
            except OSError:
                self.logger.warning("Attempt to run size check caused error - relval missing?")

        # send the announcement mail
        self.logger.debug("Sending announcement email")
        dest = "test-announce@lists.fedoraproject.org"
        urltmpl = "https://fedoraproject.org/wiki/{0}"
        summurl = urltmpl.format(event.summary_page.name.replace(" ", "_"))
        pageurls = [
            urltmpl.format(pag.name.replace(" ", "_"))
            for pag in event.valid_pages
            if "Summary" not in pag.name
        ]
        if diff:
            difftext = "\nNotable package version changes:\n{0}".format(diff)
        else:
            difftext = ""
        # this is the final part of the testcase_stats link; we want it
        # to be e.g. '27' for non-modular, '27modular' for modular
        tcstext = event.release
        shortdist = dist[7:].lower()
        if shortdist:
            tcstext += shortdist
        nighttmpl = """From: rawhide@fedoraproject.org
To: {0}
Subject: {1} {2} nightly compose nominated for testing

Announcing the creation of a new nightly release validation test event
for {1} {2}. Please help run some tests for this
nightly compose if you have time. For more information on nightly
release validation testing, see:
https://fedoraproject.org/wiki/QA:Release_validation_test_plan
{3}
Test coverage information for the current release can be seen at:
https://www.happyassassin.net/testcase_stats/{4}

You can see all results, find testing instructions and image download
locations, and enter results on the Summary page:

{5}

The individual test result pages are:

{6}

Thank you for testing!
-- 
Mail generated by relvalconsumer: https://pagure.io/fedora-qa/relvalconsumer
"""
        prodtmpl = """From: rawhide@fedoraproject.org
To: {0}
Subject: {1} {2} Candidate {3}-{4} Available Now!

According to the schedule [1], {1} {2} Candidate {3}-{4} is now
available for testing. Please help us complete all the validation
testing! For more information on release validation testing, see:
https://fedoraproject.org/wiki/QA:Release_validation_test_plan
{5}
Test coverage information for the current release can be seen at:
https://www.happyassassin.net/testcase_stats/{6}

You can see all results, find testing instructions and image download
locations, and enter results on the Summary page:

{7}

The individual test result pages are:

{8}

All {3} priority test cases for each of these test pages [2] must
pass in order to meet the {3} Release Criteria [3].

Help is available on #fedora-qa on irc.freenode.net [4], or on the
test list [5].

Current Blocker and Freeze Exception bugs:
http://qa.fedoraproject.org/blockerbugs/current

[1] http://fedorapeople.org/groups/schedule/f-{2}/f-{2}-quality-tasks.html
[2] https://fedoraproject.org/wiki/QA:Release_validation_test_plan
[3] https://fedoraproject.org/wiki/Fedora_{2}_{3}_Release_Criteria
[4] irc://irc.freenode.net/fedora-qa
[5] https://lists.fedoraproject.org/archives/list/test@lists.fedoraproject.org/
"""
        if typ == "nightly" or dist == "Fedora-IoT":
            msg = nighttmpl.format(
                dest, dist, event.version, difftext, tcstext, summurl, "\n".join(pageurls)
            )
        else:
            msg = prodtmpl.format(
                dest,
                dist,
                event.release,
                event.milestone,
                event.compose,
                difftext,
                tcstext,
                summurl,
                "\n".join(pageurls),
            )
        if self.relval_prod:
            server = smtplib.SMTP("localhost")
            server.sendmail("rawhide@fedoraproject.org", [dest], msg)
        else:
            self.logger.info(msg)


# vim: set textwidth=120 ts=8 et sw=4:
