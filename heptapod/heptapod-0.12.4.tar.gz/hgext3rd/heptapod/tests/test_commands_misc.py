# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import

from mercurial import (
    error,
    scmutil,
)
import pytest

from heptapod.testhelpers import (
    LocalRepoWrapper,
)
from .utils import common_config


def test_hpd_unique_successor(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    wrapper = LocalRepoWrapper.init(repo_path, config=common_config())
    ctx = wrapper.write_commit('foo', message="default0",
                               return_ctx=True)
    repo_path.join('foo').write('amend 1')
    wrapper.command('amend', message='amend1')
    repo_path.join('foo').write('amend 2')
    wrapper.command('amend', message='amend2')

    records = []

    def write(*args, **opts):
        records.append((args, opts))

    wrapper.repo.ui.write = write
    wrapper.command('hpd-unique-successor', rev=ctx.hex())
    out = records[0][0][0]

    succ_ctx = scmutil.revsingle(wrapper.repo, out)
    assert succ_ctx.description() == 'amend2'


def test_hpd_unique_successor_divergence(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    config = common_config()
    config.setdefault('experimental', {})['evolution.allowdivergence'] = 'yes'
    wrapper = LocalRepoWrapper.init(repo_path, config=config)
    ctx = wrapper.write_commit('foo', message="default0",
                               return_ctx=True)
    repo_path.join('foo').write('amend 1')
    wrapper.command('amend', message='amend1')

    # let's create the divergence
    wrapper.update(ctx.hex(), hidden=True)
    repo_path.join('foo').write('amend 2')
    wrapper.command('amend', message='amend2')

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('hpd-unique-successor', rev=ctx.hex())
    assert 'divergent' in exc_info.value.args[0]


def test_hpd_unique_successor_missing_rev(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    wrapper = LocalRepoWrapper.init(repo_path, config=common_config())

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('hpd-unique-successor')
    assert 'specify a revision' in exc_info.value.args[0]
