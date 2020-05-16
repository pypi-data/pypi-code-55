# Copyright (C) 2016 Red Hat
#
# This file is part of relvalconsumer.
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

# these are all kinda inappropriate for pytest patterns
# pylint: disable=old-style-class, no-init, protected-access, no-self-use, unused-argument

import time

from fedora_messaging.api import Message
import fedora_messaging.exceptions
import mock
import pytest
import relvalconsumer
import wikitcms.event

# The test approach here is that we just recreate an entire release
# cycle with mocks, and ensure the consumer does the right thing for
# each compose that shows up.


def _fakepginit(self, site, name, info=None, extra_properties=None):
    """Stub init for mwclient Page, just make sure name and site are
    set.
    """
    self.site = site
    self.name = name


def _fakemsg(cid, status="FINISHED_INCOMPLETE"):
    return Message(
        topic="org.fedoraproject.prod.pungi.compose.status.change",
        body={"compose_id": cid, "status": status},
    )


def _fakegetsame(self, packages):
    """This is a fake 'get_current_packages' which always returns the
    same dict, so when *this* is used as the mock, the consumer will
    consider both composes to have the same packages.
    """
    return {"key": "value"}


def _fakegetdifferent(self, packages):
    """This is a fake 'get_current_packages' which returns a dict with
    time.process_time() as the 'package version'. This should mean
    that when *this* is used as the mock, the consumer will consider
    both composes to have different packages, and the 'new' compose
    (whose package list is checked second) will have 'newer' packages.
    """
    return {
        "fakepackage": "fakepackage-{0}-1.fc24.src".format(str(int(time.process_time() * 1000000)))
    }


def _fakegetolder(self, packages):
    """This is a fake 'get_current_packages' which returns a dict with
    (10 - time.process_time()) as the 'package version'. So when
    *this* is used as the mock, the consumer will consider both
    composes to have different packages, and the 'new' compose (whose
    package list is checked second) will have 'older' packages.
    """
    return {
        "fakepackage": "fakepackage-{0}-1.fc24.src".format(
            str(10 * 1000000 - int(time.process_time() * 1000000))
        )
    }


def _fakegetcurr1(branched=False):
    """A faked get_current_release which just returns static values.
    This one is for pre-branch-point, when 24 is always the result.
    """
    return 24


def _fakegetcurr2(branched=False):
    """A faked get_current_release which just returns static values.
    This one is for post-branch-point, when 25 is the current Branched
    but 24 is the current stable.
    """
    if branched:
        return 25
    else:
        return 24


def _fakegettesttypes(self, dist="Fedora"):
    """A faked get_testtypes with the Right Answers hardcoded."""
    if dist == "Fedora":
        return ["Installation", "Desktop", "Server", "Cloud", "Base"]
    if dist == "Fedora-Modular":
        return ["Installation", "Server", "Base"]
    if dist == "Fedora-IoT":
        return ["General"]


# a bunch of patches we need throughout the tests
# ALL SLEEPS MUST DIE
mock.patch("time.sleep", autospec=True).start()
# page init requires wiki trip
mock.patch("mwclient.page.Page.__init__", _fakepginit).start()
# testtypes are read from wiki
mock.patch("wikitcms.wiki.Wiki.get_testtypes", _fakegettesttypes).start()
# login hits the wiki, obviously
mock.patch("wikitcms.wiki.Wiki.login", autospec=True).start()
# so does site init
mock.patch("mwclient.client.Site.site_init", autospec=True).start()

# initialize two pairs of test consumers with different configs
PRODCONF = {
    "consumer_config": {"relval_prod": True, "relvalami_prod": True, "relval_bugzilla": True,}
}
TESTCONF = {
    "consumer_config": {"relval_prod": False, "relvalami_prod": False, "relval_bugzilla": False,}
}

with mock.patch.dict("fedora_messaging.config.conf", PRODCONF):
    CONSUMER = relvalconsumer.RelvalConsumer()
    AMICONSUMER = relvalconsumer.RelvalAMIConsumer()
with mock.patch.dict("fedora_messaging.config.conf", TESTCONF):
    TESTCONSUMER = relvalconsumer.RelvalConsumer()
    TESTAMICONSUMER = relvalconsumer.RelvalAMIConsumer()

# These are all fake IDs for various composes, in the order we'll test them.
RAWHIDE1 = "Fedora-Rawhide-20160601.n.0"
UPDATE1 = "Fedora-25-updates-20180312.0"
RAWHIDE2 = "Fedora-Rawhide-20160601.n.1"
RAWHIDE3 = "Fedora-Rawhide-20160605.n.0"
RAWHIDE4 = "Fedora-Rawhide-20160620.n.0"
BRANCHED1 = "Fedora-25-20160621.n.0"
BRANCHED2 = "Fedora-25-20160629.n.0"
ALPHA1 = "Fedora-25-20160629.0"
ALPHA2 = "Fedora-25-20160629.1"
BRANCHED3 = "Fedora-25-20160630.n.0"
BRANCHED4 = "Fedora-25-20160705.n.0"
ALPHA3 = "Fedora-25-20160706.0"
BRANCHED5 = "Fedora-25-20160710.n.0"
RAWHIDE5 = "Fedora-Rawhide-20160714.n.0"
BETA1 = "Fedora-25-20160714.0"
FINAL1 = "Fedora-25-20160721.1"
ATOMIC1 = "Fedora-Atomic-25-20160725.1"
MODBRANCHED1 = "Fedora-Modular-27-20171030.n.0"
MODBRANCHED2 = "Fedora-Modular-27-20171031.n.0"
MODBRANCHED3 = "Fedora-Modular-27-20171106.n.0"
MODBETA1 = "Fedora-Modular-27-20171108.2"
MODBRANCHED4 = "Fedora-Modular-27-20171125.n.0"
MODFINAL1 = "Fedora-Modular-27-20171126.1"
IOT1 = "Fedora-IoT-25-20160621.0"
IOT2 = "Fedora-IoT-25-20160625.0"
IOT3 = "Fedora-IoT-25-20160714.0"

# expected email texts
RAWHIDE1MAIL = """From: rawhide@fedoraproject.org
To: test-announce@lists.fedoraproject.org
Subject: Fedora 25 Rawhide 20160601.n.0 nightly compose nominated for testing

Announcing the creation of a new nightly release validation test event
for Fedora 25 Rawhide 20160601.n.0. Please help run some tests for this
nightly compose if you have time. For more information on nightly
release validation testing, see:
https://fedoraproject.org/wiki/QA:Release_validation_test_plan

Test coverage information for the current release can be seen at:
https://www.happyassassin.net/testcase_stats/25

You can see all results, find testing instructions and image download
locations, and enter results on the Summary page:

https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Summary

The individual test result pages are:

https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Installation
https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Desktop
https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Server
https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Cloud
https://fedoraproject.org/wiki/Test_Results:Fedora_25_Rawhide_20160601.n.0_Base

Thank you for testing!
-- 
Mail generated by relvalconsumer: https://pagure.io/fedora-qa/relvalconsumer
"""

IOT1MAIL = """From: rawhide@fedoraproject.org
To: test-announce@lists.fedoraproject.org
Subject: Fedora-IoT 25 RC 20160621.0 nightly compose nominated for testing

Announcing the creation of a new nightly release validation test event
for Fedora-IoT 25 RC 20160621.0. Please help run some tests for this
nightly compose if you have time. For more information on nightly
release validation testing, see:
https://fedoraproject.org/wiki/QA:Release_validation_test_plan

Test coverage information for the current release can be seen at:
https://www.happyassassin.net/testcase_stats/25iot

You can see all results, find testing instructions and image download
locations, and enter results on the Summary page:

https://fedoraproject.org/wiki/Test_Results:Fedora-IoT_25_RC_20160621.0_Summary

The individual test result pages are:

https://fedoraproject.org/wiki/Test_Results:Fedora-IoT_25_RC_20160621.0_General

Thank you for testing!
-- 
Mail generated by relvalconsumer: https://pagure.io/fedora-qa/relvalconsumer
"""


# we don't really want to run size_check
@mock.patch("subprocess.call", autospec=True, return_value=0)
# get_current_release requires a network trip
@mock.patch("fedfind.helpers.get_current_release", _fakegetcurr1)
# obviously we don't really want to create the event...
@mock.patch("wikitcms.event.ValidationEvent.create", autospec=True)
# ditto sending emails.
@mock.patch("smtplib.SMTP", autospec=True)
class TestRelvalConsumerPreBranch:
    """All the pre-branch tests that use the first fake_get_current
    mock are here. In a class so we can share mock patch decorators.
    """

    # this obviously hits mirrors; we have a couple of functions for faking
    # 'same' and 'different' package sets, for different tests
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    # this needs mocking when the current event is a ComposeEvent; it's
    # used to figure out how many days it's been since 'current' event.
    # For nightly events this doesn't need a remote trip, but for
    # candidate events it does
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160530")
    # this always needs mocking, as whatever the 'current' event ought
    # to be in our fake release series.
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "24", "Final", "1.4"),
    )
    def test_rawhide1_doomed(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """We would otherwise create an event for this message -
        that's the next test - but if the status is DOOMED, we should
        not.
        """
        CONSUMER(_fakemsg(RAWHIDE1, status="DOOMED"))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0
        assert fakesubproc.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160530")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "24", "Final", "1.4"),
    )
    def test_rawhide1(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Creating first Rawhide nightly for next release."""
        CONSUMER(_fakemsg(RAWHIDE1))
        assert fakecreate.call_args[1]["check"] is True
        # check size-check got run
        assert fakesubproc.call_count == 1
        assert fakesubproc.call_args[0][0] == [
            "relval",
            "size-check",
            "--cid",
            "Fedora-Rawhide-20160601.n.0",
            "--bugzilla",
        ]
        smtp = fakesmtp.return_value
        assert smtp.sendmail.call_args[0][0] == "rawhide@fedoraproject.org"
        assert smtp.sendmail.call_args[0][1] == ["test-announce@lists.fedoraproject.org"]
        assert smtp.sendmail.call_args[0][2] == RAWHIDE1MAIL
        fakesubproc.reset_mock()

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160601.n.0"),
    )
    def test_rawhide2(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Another Rawhide nightly one day later should not produce an
        event, even if there are package differences.
        """
        CONSUMER(_fakemsg(RAWHIDE2))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0
        assert fakesubproc.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160601.n.0"),
    )
    def test_rawhide3_same(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Another Rawhide nightly four days later should not produce an
        event if the packages are the same...
        """
        CONSUMER(_fakemsg(RAWHIDE3))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160601.n.0"),
    )
    def test_rawhide3_different(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """...but the same four days later nightly should produce an
        event if the packages are different.
        """
        CONSUMER(_fakemsg(RAWHIDE3))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160605.n.0"),
    )
    def test_unsupported_compose(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """When we encounter a compose that fedfind doesn't support
        (and raises a specific exception for), we shouldn't crash, we
        should just create no event and go on our merry way."""
        CONSUMER(_fakemsg(UPDATE1))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0
        assert fakesubproc.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160605.n.0"),
    )
    def test_rawhide4(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Another Rawhide nightly 15 days later should produce an event
        even if the packages are the same.
        """
        CONSUMER(_fakemsg(RAWHIDE4))
        assert fakecreate.call_args[1]["check"] is True


@mock.patch("subprocess.call", autospec=True, return_value=0)
@mock.patch("fedfind.helpers.get_current_release", _fakegetcurr2)
@mock.patch("wikitcms.event.ValidationEvent.create", autospec=True)
@mock.patch("smtplib.SMTP", autospec=True)
# BRANCH POINT, switch to the other get_current_release mock
class TestRelvalConsumerPostBranch:
    """All the post-branch tests that use the other fake_get_current
    mock are here. In a class so we can share mock patch decorators.
    """

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160620.n.0"),
    )
    def test_branched1(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """First Branched nightly shouldn't produce an event as it's only
        one day after the Rawhide nightly.
        """
        mock.patch("fedfind.helpers.get_current_release", _fakegetcurr2).start()
        CONSUMER(_fakemsg(BRANCHED1))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160620.n.0"),
    )
    def test_branched2(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Second branched compose some days later should create an event.
        """
        CONSUMER(_fakemsg(BRANCHED2))
        assert fakecreate.call_args[1]["check"] is True

    # this has to be mocked when the 'new' event is a production one;
    # to find the correct event from the compose ID, wikitcms gets a
    # Production instance from fedfind and checks its label property,
    # then parses that
    @mock.patch("fedfind.release.Production.label", "Alpha-1.1")
    # We also have to patch the CID of the event to avoid a round trip
    # for the CID cross-check that was added in fedfind 4
    @mock.patch("fedfind.release.Production.cid", ALPHA1)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Branched", "20160629.n.0"),
    )
    def test_alpha1(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """First Alpha candidate should produce an event even though it's
        for the same date and package set as BRANCHED2.
        """
        CONSUMER(_fakemsg(ALPHA1))
        assert fakecreate.call_args[1]["check"] is True

    # this has to be mocked whenever the current event is a candidate IDed
    # by milestone and compose; wikitcms asks fedfind for the compose for
    # the current event, fedfind will return a Compose if it exists.
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Production.label", "Alpha-1.2")
    @mock.patch("fedfind.release.Production.cid", ALPHA2)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160629")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.1"),
    )
    def test_alpha2(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """Second Alpha candidate should produce an event even though it's
        for the same date and package set as ALPHA1 (somewhat unrealistic,
        but it's what ought to happen).
        """
        CONSUMER(_fakemsg(ALPHA2))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160629")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.2"),
    )
    def test_branched3(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """Branched nightly shortly after candidate compose should not
        create event even if package set is different.
        """
        CONSUMER(_fakemsg(BRANCHED3))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160629")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.2"),
    )
    def test_branched4_same(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """Branched nightly a few days later with same package set should
        not create event...
        """
        CONSUMER(_fakemsg(BRANCHED4))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetolder)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160629")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.2"),
    )
    def test_branched4_older(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """...nor should same few-days-later Branched nightly with *older*
        packages...
        """
        CONSUMER(_fakemsg(BRANCHED4))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160629")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.2"),
    )
    def test_branched4_newer(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """...but same few-days-later Branched nightly with newer
        packages should create event.
        """
        CONSUMER(_fakemsg(BRANCHED4))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Production.label", "Alpha-1.3")
    @mock.patch("fedfind.release.Production.cid", ALPHA3)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Branched", "20160705.n.0"),
    )
    def test_alpha3(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Another Alpha candidate came along! Event should be created
        even though it's only been one day.
        """
        CONSUMER(_fakemsg(ALPHA3))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160706")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Alpha", "1.3"),
    )
    def test_branched5(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """OK, say Alpha 1.3 went out as Alpha. Now another Branched
        comes along. This isn't testing anything new but I wanna go
        from Branched to Beta then Beta to Final. We should get an event
        here.
        """
        CONSUMER(_fakemsg(BRANCHED5))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Branched", "20160710.n.0"),
    )
    def test_rawhide5(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Meanwhile, a Rawhide compose shows up (this is a thing that
        happens all the time). We should NOT create any event for it -
        we never create events for the release after the next (i.e. for
        Rawhide when there is a Branched).
        """
        CONSUMER(_fakemsg(RAWHIDE5))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Production.label", "Beta-1.1")
    @mock.patch("fedfind.release.Production.cid", BETA1)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Branched", "20160710.n.0"),
    )
    def test_beta1(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """OK, here comes Beta. We should get an event, of course."""
        CONSUMER(_fakemsg(BETA1))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Production.label", "RC-1.1")
    @mock.patch("fedfind.release.Production.cid", FINAL1)
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160714")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "Beta", "1.1"),
    )
    def test_final1(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """Finally, here comes Final! Testing going straight from one
        candidate compose to another milestone candidate compose, though
        this is unlikely ever to happen. We should get an event.
        """
        CONSUMER(_fakemsg(FINAL1))
        assert fakecreate.call_args[1]["check"] is True

    @mock.patch("fedfind.release.Production.label", "RC-20161120.0")
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch("wikitcms.event.ComposeEvent.creation_date", "20160721")
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.ComposeEvent(None, "25", "RC", "1.1"),
    )
    def test_atomic1(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """We may get two-week Atomic composes for the release starting
        up before it goes final; make sure we don't get events for these.
        """
        CONSUMER(_fakemsg(ATOMIC1))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(
            None, "27", "Branched", "20171001.n.0", dist="Fedora-Modular"
        ),
    )
    def test_modular_branched1(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Now a Modular compose shows up! We should NOT get an event,
        because we don't do events for modular composes any more.
        """
        CONSUMER(_fakemsg(MODBRANCHED1))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.IoTNightly.cid", IOT1)
    @mock.patch("fedfind.release.IoTNightly.label", "RC-20160621.0")
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("wikitcms.wiki.Wiki.get_current_event", return_value=None)
    def test_iot1(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """An IoT compose shows up, and we have never done an IoT event
        before, so get_current_event returns None. We should create an
        event in this case.
        """
        CONSUMER(_fakemsg(IOT1))
        assert fakecreate.call_args[1]["check"] is True
        assert fakecreate.call_args[0][0].dist == "Fedora-IoT"
        smtp = fakesmtp.return_value
        assert smtp.sendmail.call_args[0][0] == "rawhide@fedoraproject.org"
        assert smtp.sendmail.call_args[0][1] == ["test-announce@lists.fedoraproject.org"]
        assert smtp.sendmail.call_args[0][2] == IOT1MAIL

    @mock.patch("fedfind.release.IoTNightly.cid", IOT2)
    @mock.patch("fedfind.release.IoTNightly.label", "RC-20160625.0")
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(
            None, "25", "Branched", "20160621.n.0", dist="Fedora-IoT"
        ),
    )
    def test_iot2_same(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """A second IoT compose shows up a few days later, with the
        same packages. We should not create an event.
        """
        CONSUMER(_fakemsg(IOT2))
        assert fakecreate.call_count == 0
        assert fakesmtp.call_count == 0

    @mock.patch("fedfind.release.IoTNightly.cid", IOT2)
    @mock.patch("fedfind.release.IoTNightly.label", "RC-20160625.0")
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(
            None, "25", "Branched", "20160621.n.0", dist="Fedora-IoT"
        ),
    )
    def test_iot2_different(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """But if it showed up with different packages, we should.
        """
        CONSUMER(_fakemsg(IOT2))
        assert fakecreate.call_args[1]["check"] is True
        assert fakecreate.call_args[0][0].dist == "Fedora-IoT"

    @mock.patch("fedfind.release.IoTNightly.cid", IOT3)
    @mock.patch("fedfind.release.IoTNightly.label", "RC-20160714.0")
    @mock.patch("fedfind.release.Compose.exists", return_value=True)
    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetsame)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(
            None, "25", "Branched", "20160625.n.0", dist="Fedora-IoT"
        ),
    )
    def test_iot3_same(self, fakecurrev, fakecompexists, fakesmtp, fakecreate, fakesubproc):
        """A third IoT compose shows up some time later, with the
        same packages. We should create an event.
        """
        CONSUMER(_fakemsg(IOT3))
        assert fakecreate.call_args[1]["check"] is True
        assert fakecreate.call_args[0][0].dist == "Fedora-IoT"

    def test_badcid(self, fakesmtp, fakecreate, fakesubproc):
        """On a non-parseable compose ID, we should log errors and
        raise the fedora_messaging Drop exception.
        """
        with pytest.raises(fedora_messaging.exceptions.Drop):
            # FIXME: check log messages
            CONSUMER(_fakemsg("PLAYGROUND-8-20190730.n.0"))

    @mock.patch("fedfind.release.Pungi4Release.get_package_nvras", _fakegetdifferent)
    @mock.patch(
        "wikitcms.wiki.Wiki.get_current_event",
        return_value=wikitcms.event.NightlyEvent(None, "25", "Rawhide", "20160620.n.0"),
    )
    def test_testconsumer(self, fakecurrev, fakesmtp, fakecreate, fakesubproc):
        """Creating second Branched nightly again with test consumer,
        to make sure that works.
        """
        TESTCONSUMER(_fakemsg(BRANCHED2))
        assert fakecreate.call_args[1]["check"] is True
        # check size-check got run
        assert fakesubproc.call_count == 1
        assert fakesubproc.call_args[0][0] == [
            "relval",
            "size-check",
            "--cid",
            "Fedora-25-20160629.n.0",
            "--test",
        ]
        # check we didn't send a mail
        assert fakesmtp.call_count == 0
        # FIXME we should check we used stg wiki, but it's a bit tricky
        # with these mocks
        fakesubproc.reset_mock()


# get_current_release requires a network trip
@mock.patch("fedfind.helpers.get_current_release", _fakegetcurr1)
# don't actually write anything
@mock.patch("wikitcms.page.AMIPage.write", autospec=True)
class TestRelvalAMIConsumer:
    """All tests for the AMI consumer."""

    amimsg = Message(
        topic="org.fedoraproject.prod.fedimg.image.publish",
        body={"compose": "Fedora-Rawhide-20191109.n.0", "extra": {"id": "ami-0f4c7283a18abbc53"},},
    )

    # make consumer believe event 'exists' (real return value would be
    # a list of Page instances, but meh)
    @mock.patch("wikitcms.event.ValidationEvent.result_pages", return_value=[1])
    def test_ami_exists(self, fakeres, fakewrite):
        """We should write the AMI page when the event exists."""
        AMICONSUMER(self.amimsg)
        assert fakewrite.call_count == 1
        fakewrite.reset_mock()
        TESTAMICONSUMER(self.amimsg)
        assert fakewrite.call_count == 1

    # make consumer believe event does not 'exist'
    @mock.patch("wikitcms.event.ValidationEvent.result_pages", [])
    def test_ami_not_exists(self, fakewrite):
        """We shouldn't write the AMI page when the event doesn't
        exist.
        """
        AMICONSUMER(self.amimsg)
        assert fakewrite.call_count == 0
