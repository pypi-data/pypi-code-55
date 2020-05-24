# -*- coding: utf-8 -*-
"""Audit Logs class file."""

import argparse
import datetime
import json
import logging
import pytz
import re
import sys

from bits.google import Google


class AuditLogs(object):
    """Audit Logs class."""

    def __init__(self, auth, github, args):
        """Initialize a class instance."""
        self.auth = auth
        self.github = github

        self.flags = self.parse_args(args)
        self.filename = self.flags.filename

        self.org_members = {}
        self.org_teams = {}

        self.verbose = self.github.verbose

    def _convert_created_at(self, created_at):
        """Return the created_at timestamp as a datetime."""
        # convert created_at to a unit timestamp
        timestamp = int(str(created_at)[:-3])
        # get timestamp in eastern time
        tz = pytz.timezone('America/New_York')
        # convert from unix timestamp to a datetime
        return datetime.datetime.fromtimestamp(timestamp, tz=tz)

    def _get_org_members(self):
        """Return a dict of org members by login."""
        members = {}
        for m in self.github.get_org_members():
            login = m['login'].lower()
            members[login] = m
        return members

    def _get_org_teams(self):
        """Return a dict of org teams by slug."""
        teams = {}
        for t in self.github.get_org_teams():
            slug = t['slug'].lower()
            teams[slug] = t
        return teams

    def _get_location(self):
        """Return the type of file being imported."""
        # determine the type of file being passed
        filetype = None
        if re.match('gs://', self.filename):
            filetype = 'gcs'
        elif not re.search(':', self.filename):
            filetype = 'local'
        logging.info('Filename: {} [{}]'.format(self.filename, filetype))
        return filetype

    def _import_gcs_file(self):
        """Import audit logs from a gcs object."""
        g = Google()
        path = self.filename.replace('gs://', '')
        bucket = path.split('/')[0]
        filename = '/'.join(path.split('/')[1:])
        return g.storage().download_blob_as_string(bucket, filename)

    def _import_local_file(self):
        """Import audit logs from a local file."""
        # read file off disk
        try:
            f = open(self.filename, 'r')
        except FileNotFoundError as e:
            logging.error('Failed to open audit logs file: {}'.format(self.filename))
            sys.exit(e)

        return f.read()

    #
    # Parse arguments
    #
    def parse_args(self, args=None):
        """Parse arguments for the audit logs."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'filename',
            help="Relative path to Audit Log JSON file or GCS path."
        )
        parser.add_argument(
            '-n',
            '--noop',
            action="store_true",
            help="Don't make an changes.",
        )
        parser.add_argument(
            '--action',
            choices=['repo.remove_member', 'team.remove_member'],
            help="Filter by a specific action.",
            required=True,
        )
        parser.add_argument(
            '--min-datetime',
            help="Specify the minimum time to consider in the audit logs."
        )
        parser.add_argument(
            '--max-datetime',
            help="Specify the maximum time to consider in the audit logs."
        )
        parser.add_argument('--actor', help="Filter by a specific actor.")
        parser.add_argument('--org', help="Filter by a specific org.")
        parser.add_argument('--repo', help="Filter by a specific repo.")
        parser.add_argument('--team', help="Filter by a specificmteak.")
        parser.add_argument('--user', help="Filter by a specific user.")
        return parser.parse_args(args)

    #
    # Logs
    #
    def display_logs(self, logs=None):
        """Display the audit logs in a human-readable format."""
        if not logs:
            logs = self.import_logs()
        for log in logs:
            if 'data' in log and 'team' in log['data']:
                resource = log['data']['team'].lower()
            elif 'repo' in log:
                resource = log['repo'].lower()
            created_at = self._convert_created_at(log['created_at'])
            print('{} {} performed "{}" from {} on user "{}".'.format(
                created_at,
                log.get('actor'),
                log.get('action'),
                resource,
                log.get('user').lower(),
            ))

    def filter_logs(self, logs=None):
        """Filter logs to a specific set and return as iterator."""
        if not logs:
            logs = self.import_logs()
        for log in logs:
            # filter on action
            if self.flags.action and log.get('action') != self.flags.action:
                continue
            # filter on actor
            if self.flags.actor and log.get('actor') != self.flags.actor:
                continue
            # filter on org
            if self.flags.org and log.get('org') != self.flags.org:
                continue
            # filter on repo
            if self.flags.repo and log.get('repo') != self.flags.repo:
                continue
            # filter on user
            if self.flags.user and log.get('user') != self.flags.user:
                continue
            # filter on team
            if 'data' in log and 'team' in log['data']:
                if self.flags.team and log['data']['team'] != self.flags.team:
                    continue
            created_at = self._convert_created_at(log['created_at'])
            # filter on min datetime
            if self.flags.min_datetime and str(created_at) < self.flags.min_datetime:
                continue
            # filter on max datetime
            if self.flags.max_datetime and str(created_at) > self.flags.max_datetime:
                continue

            yield log

    def import_logs(self):
        """Import audit logs from a file."""
        # determine location of file
        location = self._get_location()

        # import file contents
        if location == 'gcs':
            filestring = self._import_gcs_file()
        elif location == 'local':
            filestring = self._import_local_file()
        else:
            logging.error('Unsupported file path: "{}"'.format(self.filename))
            sys.exit(1)

        # import json to a dictionary
        try:
            logs = sorted(json.loads(filestring), key=lambda x: x['created_at'])
        except json.decoder.JSONDecodeError as e:
            logging.error('Failed to import audit logs JSON.')
            sys.exit(e)

        return self.filter_logs(logs)

    def _get_repo_collaborators(self, repo):
        """Return a list of logins that are current repo collaborators."""
        try:
            collaborators = self.github.get_repo_collaborators(repo)
        except Exception as e:
            logging.error('Failed to get collaborators for repo: {}'.format(repo))
            print(e)
            return []
        logins = []
        for m in collaborators:
            logins.append(m['login'].lower())
        return logins

    def _restore_repo_collaborators(self, repo, actions):
        """Restore collaborators for a single repo."""
        collaborators = self._get_repo_collaborators(repo)
        print('\nRepo: {} [{}]'.format(repo, len(actions)))
        for login in sorted(actions):
            if login in collaborators:
                if self.verbose:
                    print('   o Already added {}'.format(login))
            elif login in self.org_members:
                print('   + Inviting {}...'.format(login))
                if not self.flags.noop:
                    self.github.add_repo_collaborator(repo, login)
            else:
                if self.verbose:
                    print('   o Skipping {} [not org member]'.format(login))

    def restore_repos_collaborators(self, logs):
        """Restore repo collaborators from audit logs."""
        self.org_members = self._get_org_members()
        repos = {}
        for row in logs:
            login = row['user'].lower()
            repo = row['repo'].replace('broadinstitute/', '').lower()
            if repo not in repos:
                repos[repo] = []
            if login not in repos[repo]:
                repos[repo].append(login)
        if repos:
            resource = 'repo'
            if len(repos) > 1:
                resource += 's'
            print('\nRestoring collaborators to {} {}...'.format(len(repos), resource))
            for repo in sorted(repos):
                self._restore_repo_collaborators(repo, repos[repo])

    def _get_team_members(self, team_id):
        """Return a list of logins that are current team members."""
        logins = []
        for m in self.github.get_team_members(team_id):
            logins.append(m['login'].lower())
        return logins

    def _restore_team_members(self, slug, actions):
        """Restore members for a single team."""
        team = slug.replace('broadinstitute/', '')
        if team not in self.org_teams:
            logging.error('Team not found in org: {}'.format(team))
            return []
        team_id = self.org_teams[team]['id']
        members = self._get_team_members(team_id)
        print('\nTeam: {} [{}]'.format(team, len(actions)))
        for login in sorted(actions):
            if login in members:
                if self.verbose:
                    print('   o Already added {}'.format(login))
            elif login in self.org_members:
                print('   + Inviting {}...'.format(login))
                self.github.invite_team_member(team_id, login)
            else:
                if self.verbose:
                    print('   o Skipping {} [not org member]'.format(login))

    def restore_teams_members(self, logs):
        """Restore team members from audit logs."""
        self.org_members = self._get_org_members()
        self.org_teams = self._get_org_teams()
        teams = {}
        for row in logs:
            login = row['user'].lower()
            if 'data' in row and 'team' in row['data']:
                team = row['data']['team'].lower()
            else:
                print(row)
                continue
            if team not in teams:
                teams[team] = []
            if login not in teams[team]:
                teams[team].append(login)
        if teams:
            resource = 'team'
            if len(teams) > 1:
                resource += 's'
            print('\nRestoring members to {} {}...'.format(len(teams), resource))
            for team in sorted(teams):
                self._restore_team_members(team, teams[team])

    #
    # Stats
    #
    def display_stats(self, stats):
        """Display stats about the logs."""
        start_date = stats['min_created_at']
        end_date = stats['max_created_at']

        print('Audit Logs Start Date: {}'.format(start_date))
        print('Audit Logs End Date: {}'.format(end_date))

        # actions
        actions = stats['actions']
        print('\nActions: [{}]'.format(len(actions)))
        print('{}{}'.format(
            '   * ',
            '\n   * '.join(sorted(actions)),
        ))

        # actors
        actors = stats['actors']
        print('\nActors: [{}]'.format(len(actors)))
        print('{}{}'.format(
            '   * ',
            '\n   * '.join(sorted(actors)),
        ))

        # repos
        repos = stats['repos']
        if repos:
            print('\nRepos: [{}]'.format(len(repos)))
        print('{}{}'.format(
            '   * ',
            '\n   * '.join(sorted(repos)),
        ))

        # teams
        teams = stats['teams']
        if teams:
            print('\nTeams: [{}]'.format(len(teams)))
        print('{}{}'.format(
            '   * ',
            '\n   * '.join(sorted(teams)),
        ))

        # users
        users = stats['users']
        print('\nUsers: [{}]'.format(len(users)))
        print('{}{}'.format(
            '   * ',
            '\n   * '.join(sorted(users)),
        ))

    def get_stats(self, logs):
        """Return status about the logs."""
        actors = []
        actions = []
        repos = []
        teams = []
        users = []
        max_created_at = ''
        min_created_at = ''

        for row in logs:
            # get action
            action = row.get('action', '')
            if action not in actions:
                actions.append(action)

            # get actor
            actor = row.get('actor', '')
            if actor not in actors:
                actors.append(actor)

            # get created_at
            created_at = self._convert_created_at(row['created_at'])
            if not max_created_at or created_at > max_created_at:
                max_created_at = created_at
            if not min_created_at or created_at < min_created_at:
                min_created_at = created_at

            # get repo
            if 'repo' in row:
                repo = row['repo'].lower()
                if repo not in repos:
                    repos.append(repo)

            # get team
            if 'data' in row:
                data = row['data']
                if 'team' in data:
                    team = data['team'].lower()
                    if team not in teams:
                        teams.append(team)

            # get user
            user = row.get('user', '').lower()
            if user not in users:
                users.append(user)

        stats = {
            'actions': actions,
            'actors': actors,
            'repos': repos,
            'teams': teams,
            'users': users,
            'max_created_at': max_created_at,
            'min_created_at': min_created_at,
        }
        return stats
