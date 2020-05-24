# -*- coding: utf-8 -*-
"""Update Class file."""

import datetime
import dateutil.parser
import logging
import pytz
import sys

from bits.github import GitHub
from requests import HTTPError


class Update(object):
    """Update class."""

    def __init__(self, auth=None, github=None):
        """Initialize a class instance."""
        self.auth = auth
        self.github = github

        self.verbose = False
        if self.auth:
            self.verbose = self.auth.verbose

        # data
        self.github_ids = {}
        self.github_users = {}
        self.google_ids = {}
        self.people = {}
        self.role_accounts = {}
        self.users = {}

    def _get_firestore_github_users(self):
        """Return a dict of cached GitHub users from Firestore."""
        github_users = {}
        firestore = self.github.firestore(app_project='broad-github-app')
        for doc in firestore.app.collection('github_users').stream():
            github_id = doc.id
            github_users[github_id] = doc.to_dict()
        return github_users

    def _get_github_role_accounts(self):
        """Return a dict of github role accounts by github ID."""
        role_accounts = {}
        for m in self.github.get_team_members(self.github.role_team):
            github_id = str(m['id'])
            role_accounts[github_id] = m
        return role_accounts

    def _get_github_team_invitations(self, team_id):
        """Return a dict fo github team invitations by login."""
        invitations = {}
        for i in self.github.get_team_invitations(team_id):
            login = i['login'].lower()
            invitations[login] = i
        return invitations

    def _get_github_team_members(self, team_id):
        """Return a dict of github team members by github ID."""
        members = {}
        for m in self.github.get_team_members(team_id):
            github_id = str(m['id'])
            members[github_id] = m
        return members

    def _get_google_group_members(self, email):
        """Return a list of members from a google group."""
        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.directory().get_derived_members(email)

    def _get_invitations(self):
        """Return a dict of invitations by GitHub ID."""
        invitations = {}
        for i in self.github.get_org_invitations():
            login = i['login'].lower()
            invitations[login] = i
        return invitations

    def _get_members(self):
        """Return a dict of members by GitHub ID."""
        members = {}
        for m in self.github.get_org_members():
            gid = u'{}'.format(m['id'])
            members[gid] = m
        return members

    def _get_new_logins(self, new):
        """Return a list of logins in the new users data."""
        logins = []
        for gid in new:
            n = new[gid]
            login = n['login'].lower()
            logins.append(login)
        return logins

    def _get_people(self):
        """Return a dict of people."""
        firestore = self.github.firestore()
        self.people = firestore.get_people_dict(key='google_id')
        return self.people

    def _get_team_members_to_add(self, current, new, invitations):
        """Return a list of members to add to a team."""
        add = {}
        for github_id in new:
            n = new[github_id]
            login = n['login'].lower()
            if github_id not in current and login not in invitations:
                add[github_id] = new[github_id]
        return add

    def _get_team_members_to_remove(self, current, new, invitations):
        """Return a list of members to remove from a team."""
        remove = {}
        for github_id in current:
            c = current[github_id]
            login = c['login'].lower()
            if github_id not in new and login not in invitations and github_id not in self.role_accounts:
                remove[github_id] = current[github_id]
        return remove

    def _get_users(self):
        """Return a dict of users."""
        firestore = self.github.firestore(app_project='broad-github-app')
        # get users by github_id and google_id
        self.github_ids = {}
        self.google_ids = {}
        self.users = {}
        for t in firestore.get_tokens():
            email = t['google_email']
            t['github_id'] = str(t['github_id'])
            t['google_id'] = str(t['google_id'])
            github_id = t['github_id']
            google_id = t['google_id']

            # fix login
            t['login'] = t['github_login'].lower()
            del t['github_login']

            self.github_ids[github_id] = t
            self.google_ids[google_id] = t
            self.users[email] = t

            # import json
            # print(json.dumps(t, indent=2, sort_keys=True, default=str))

        # datastore = self.github.datastore()
        # self.users = datastore.get_users_dict()
        # # get users by github_id and google_id
        # self.github_ids = {}
        # self.google_ids = {}
        # for email in self.users:
        #     e = self.users[email]
        #     github_id = e['github_id']
        #     google_id = e['google_id']
        #     self.github_ids[github_id] = e
        #     self.google_ids[google_id] = e

        return self.users

    def _get_users_to_invite(self, current, new, invitations):
        """Return a list of logins to invite to the organization."""
        invite = []
        for gid in new:
            n = new[gid]
            login = n['login']
            if gid not in current:
                # make sure user doens't already have an invitation
                if login not in invitations:
                    invite.append(login)
        return invite

    def _get_users_to_remove(self, current, new):
        """Return a list of users to remove from the organization."""
        remove = []
        for gid in current:
            if gid not in new:
                login = current[gid]['login']
                remove.append(login)
        return remove

    def _get_users_to_uninvite(self, invitations, logins):
        """Return a list of users to uninvite from the organization."""
        uninvite = []
        for login in invitations:
            if login.lower() not in logins:
                uninvite.append(login)
        return uninvite

    def _prepare_members(self):
        """Prepare a list of org members for GitHub."""
        # get users that have linked their github account
        if not self.users:
            self.users = self._get_users()
        print('Found {} Tokens in GitHub App.'.format(len(self.users)))

        # get people
        if not self.people:
            self.people = self._get_people()
        print('Found {} People in BITSdb.'.format(len(self.people)))

        # get role_accounts
        if not self.role_accounts:
            role_accounts = self._get_github_role_accounts()
        print('Found {} GitHub Role Accounts.'.format(len(role_accounts)))

        members = {}

        # add github users who have linked their account and have a valid token
        for email in self.users:
            user = self.users[email]
            github_id = str(user['github_id'])
            google_id = user['google_id']
            if google_id not in self.people:
                # print('ERROR: Person not found: {}'.format(email))
                continue
            elif self.people[google_id]['terminated']:
                # print('WARNING: Person is terminated: {}'.format(email))
                continue
            members[github_id] = user

        # add in role accounts
        for github_id in role_accounts:
            user = role_accounts[github_id]
            members[github_id] = user

        return members

    def _prepare_team_members(self, group_members):
        """Covert Google Group Members to GitHub ID/logins."""
        team_members = {}
        for m in group_members:
            google_id = m['id']

            # check if google id has linked their account
            if google_id not in self.google_ids:
                # print('Google User not found: {} [{}]'.format(m['email'], google_id))
                continue

            # check if google id is in people
            if google_id not in self.people:
                print('Person not found: {} [{}]'.format(m['email'], google_id))
                continue

            # check if google id is terminated
            else:
                if self.people[google_id]['terminated']:
                    continue

            user = self.google_ids[google_id]
            github_id = user['github_id']
            team_members[github_id] = user

        return team_members

    #
    # Update Org Members
    #
    def update_members(self):
        """Update members in GitHub."""
        current = self._get_members()
        print('Found {} current GitHub Members.'.format(len(current)))

        new = self._prepare_members()
        print('Found {} suitable GitHub Members.'.format(len(new)))

        invitations = self._get_invitations()
        print('Found {} open GitHub Invitations.'.format(len(invitations)))

        # get users to invite and remove from the org
        invite = self._get_users_to_invite(current, new, invitations)
        remove = self._get_users_to_remove(current, new)

        # check to make sure we do not remove too many members
        current_count = len(current) + len(invitations)
        new_count = len(new)

        # check for more than 50 members being removed
        if (current_count - new_count) > 50 or len(remove) > 50:
            logging.error('More than 50 members to remove! Exiting.')
            sys.exit(1)

        # check for invitations to cancel
        logins = self._get_new_logins(new)
        uninvite = self._get_users_to_uninvite(invitations, logins)

        if invite:
            print('\nMembers to invite: {}'.format(len(invite)))
            for login in sorted(invite):
                print('   + {}'.format(login))
                try:
                    self.github.invite_org_member(login)
                except Exception as e:
                    print('ERROR: Failed to invite org member: {}'.format(login))
                    print(e)

        if remove:
            print('\nMembers to remove: {}'.format(len(remove)))
            for login in sorted(remove):
                print('   - {}'.format(login))
                self.github.remove_org_member(login)

        if uninvite:
            print('\nInvitations to cancel: {}'.format(len(uninvite)))
            for login in sorted(uninvite):
                print('   - {}'.format(login))
                self.github.remove_org_member(login)

        if self.verbose:
            print('Done updating GitHub members.')

    #
    # Update Org Teams
    #
    def update_team(self, slug, team_id, email):
        """Update a single team."""
        # get current team members
        current = self._get_github_team_members(team_id)

        # get open team invitations
        invitations = self._get_github_team_invitations(team_id)

        # get google group members
        group_members = self._get_google_group_members(email)

        # prepare google group members into github team members
        new = self._prepare_team_members(group_members)

        # get team members to add
        add = self._get_team_members_to_add(current, new, invitations)

        # get team members to remove
        remove = self._get_team_members_to_remove(current, new, invitations)

        if self.verbose or add or remove:
            print('\n{} [{}] <-- {}:'.format(
                slug,
                team_id,
                email,
            ))

        # display stats
        if self.verbose:
            print('   current: {}, group: {}, new: {}, invitations: {}'.format(
                len(current),
                len(group_members),
                len(new),
                len(invitations),
            ))

        # display any users to add
        if add:
            print('   members to add: {}'.format(len(add)))
            for github_id in sorted(add, key=lambda x: add[x]['login'].lower()):
                user = add[github_id]
                login = user['login'].lower()
                print('     + {} [{}]'.format(login, github_id))
                # add the github user to the team
                self.github.invite_team_member(team_id, login)

        # display any users to remove
        if remove:
            print('   members to remove: {}'.format(len(remove)))
            for github_id in sorted(remove, key=lambda x: remove[x]['login'].lower()):
                user = remove[github_id]
                login = user['login'].lower()
                print('     - {} [{}]'.format(login, github_id))
                # remove the github user from the team
                self.github.remove_team_member(team_id, login)

    def update_teams(self):
        """Update team membership in GitHub from Google Groups."""
        # get Broadies that have linked their GitHub accounts.
        if not self.users:
            self.users = self._get_users()
        print('Found {} Tokens in GitHub App.'.format(len(self.users)))

        # get role accounts
        if not self.role_accounts:
            self.role_accounts = self._get_github_role_accounts()
        print('Found {} Role Accounts in GitHub.'.format(len(self.role_accounts)))

        # firestore - get people
        if not self.people:
            self.people = self._get_people()
        print('Found {} People in BITSdb.'.format(len(self.people)))

        # firestore - get team syncs
        firestore = self.github.firestore(app_project='broad-github-app')
        team_syncs = firestore.get_team_syncs_dict()
        print('Found {} GitHub Team Syncs in BITSdb.'.format(len(team_syncs)))

        for slug in sorted(team_syncs):
            s = team_syncs[slug]
            team_id = s['team_id']
            email = s['group_email']
            self.update_team(slug, team_id, email)

        if self.verbose:
            print('Done updating GitHub teams.')

    #
    # Update Team Syncs
    #
    def update_team_syncs(self):
        """Update Team Syncs from On-Prem Mongo to Cloud Firestore."""
        b = self.auth.bitsdbapi()

        firestore_project = self.auth.settings.get('githubapp', {}).get('project')
        if not firestore_project:
            logging.error('Firestore Project required: settings["githubapp"]["project]')
            sys.exit()

        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)

        # get team syncs from source of truth - bitsdb mongo
        m = self.auth.mongo()

        tz = pytz.timezone('UTC')
        mongo_team_syncs = []
        syncs_dict = {}
        for sync in m.get_collection('github_team_sync'):
            created = sync['created']
            modified = sync['modified']
            if isinstance(created, str):
                sync['created'] = datetime.datetime.strptime(created, '%Y-%b-%d %H:%M:%S').astimezone(tz)
            if isinstance(modified, str):
                sync['modified'] = datetime.datetime.strptime(modified, '%Y-%b-%d %H:%M:%S').astimezone(tz)
            mongo_team_syncs.append(sync)
            syncs_dict[sync['_id']] = sync
        m.update_collection('github_team_sync', syncs_dict)
        print('Found {} GitHub Team Syncs in BITSdb Mongo.'.format(len(mongo_team_syncs)))

        # create new dict of team syncs ready for datastore and firestore
        datastore_syncs = {}
        firestore_syncs = {}
        for sync in sorted(mongo_team_syncs, key=lambda x: x['google_group']):
            del sync['_id']
            email = sync['google_group']

            print('Getting group and members: {}'.format(email))
            # get group
            group = g.directory().get_group(email)
            # get members
            members = []
            for m in g.directory().get_members_recursively(email):
                members.append(m['id'])

            # prepare sync for datastore (bitsdb api)
            datastore_sync = {
                'kind': 'github#teamsync',
                'id': str(sync['github_team']),
                'google_group_id': group['id'],
                'google_group_email': group['email'],
                'google_group_name': group['name'],
                'github_team_id': str(sync['github_team']),
                'github_team_name': sync['github_team_name'],
                'github_team_slug': sync['github_team_slug'],
            }

            # prepare sync for firestore (github app)
            firestore_sync = {
                # sync info
                'created': sync['created'],
                'modified': sync['modified'],
                # group info
                'group_email': group['email'],
                'group_id': group['id'],
                'group_members': members,
                'group_name': group['name'],
                # team info
                'team_id': sync['github_team'],
                'team_name': sync['github_team_name'],
                'team_slug': sync['github_team_slug'],
            }
            team_id = str(sync['github_team'])

            # add to datastore syncs
            if team_id in datastore_syncs:
                print('Duplicate Datastore Sync: {} -> {}'.format(email, team_id))
            datastore_syncs[team_id] = datastore_sync

            # add to firestore syncs
            if team_id in firestore_syncs:
                print('Duplicate Firestore Sync: {} -> {}'.format(email, team_id))
            firestore_syncs[team_id] = firestore_sync

        # update the data in the bitsdb api
        b.update(
            cls=g,
            collection='github/teams/syncs',
            data=datastore_syncs,
            delete_function='delete_github_team_sync',
            insert_function='add_github_team_sync',
            list_function='get_github_team_syncs',
            key='github_team_id',
            kinds='teams_syncs',
            prep=False,
        )

        # update firestore in the github app projects
        print(g.firestore(firestore_project).update_collection_batch(
            'team_syncs',
            firestore_syncs,
            delete_docs=True,
        ))

    #
    # Update Tokens
    #
    def update_tokens(self):
        """Check stored GitHub Tokens and update as necessary."""
        firestore_project = self.auth.settings.get('githubapp', {}).get('project')
        firestore = self.github.firestore(app_project=firestore_project)

        # get people from firestore
        people = firestore.get_people_dict(key='google_id')

        # get users from firestore
        users = {}
        for u in firestore.get_github_users():
            uid = u['id']
            users[uid] = u

        remove_tokens = []
        update_tokens = []

        # get tokens from
        for t in firestore.get_tokens():
            github_id = int(t['github_id'])
            github_login = t['github_login']

            google_id = t['google_id']
            google_email = t['google_email']

            remove = False
            update = False

            # check google_id
            if google_id not in people:
                print('Google User not found: {} [{}]'.format(google_id, google_email))
                remove = True

            # check github_id
            elif github_id not in users:
                print('GitHub User not found: {} [{}]'.format(github_id, github_login))
                remove = True

            # check google email
            elif google_email != people[google_id]['email_username']:
                print('Google Email needs update: {}: {} -> {}'.format(
                    google_id,
                    google_email,
                    people[google_id]['email_username'],
                ))
                t['google_email'] = people[google_id]['email_username']
                update = True

            # check github login
            elif github_login != users[github_id]['login'].lower():
                print('GitHub Login needs update: {}: {} -> {}'.format(
                    github_id,
                    github_login,
                    users[github_id]['login'].lower(),
                ))
                t['github_login'] = users[github_id]['login'].lower()
                update = True

            if remove:
                remove_tokens.append(t)
            elif update:
                update_tokens.append(t)

        # update tokens that need updating
        if update_tokens:
            print('\nUpdating tokens for {} users...'.format(len(update_tokens)))
            for t in sorted(update_tokens, key=lambda x: x['github_login']):
                current = firestore.get_stored_token(t['google_id'])
                print('   * {} [{}]'.format(
                    current['github_login'],
                    current['github_id'],
                ))
                current = firestore.get_stored_token(t['google_id'])
                current['github_login'] = t['github_login']
                current['google_email'] = t['google_email']
                firestore.store_token(current)

        # remove tokens that need updating
        if remove_tokens:
            print('\nRemoving tokens for {} users...'.format(len(remove_tokens)))
            for t in sorted(remove_tokens, key=lambda x: x['github_login']):
                print('   - {} [{}]'.format(
                    t['github_login'],
                    t['github_id'],
                ))
                firestore.delete_stored_token(t['google_id'])

    #
    # Update Users
    #
    def update_user(self, github_id, login, token, user):
        """Update a single user."""
        # get last modified date from current record
        last_modified = None
        if user:
            updated_at = dateutil.parser.parse(user['updated_at'])
            last_modified = updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')

        # authenticate with user's token
        github = GitHub(token)

        # get user from github api
        try:
            new = github.get_self(last_modified=last_modified)
        except HTTPError as e:
            if e.response.status_code == 401:
                logging.warning('Invalid token for user: {} [{}]'.format(login, github_id))
                print('Deleting user with invalid token: {} [{}]'.format(login, github_id))
                # delete user with invalid token from user token store
                self.github.firestore().delete_stored_github_user(github_id)
            else:
                logging.error('Failed to get user: {} [{}]'.format(login, github_id))
                logging.error(e)
            return user

        # don't update users that haven't changed
        if new is False:
            # User record has not been updated since the last time we checked.
            if self.verbose:
                print('Skipping {} [{}]'.format(login, github_id))
            return user

        # print(json.dumps(user, indent=2, sort_keys=True))
        if user:
            print('Updated user: {}'.format(new['login'].lower()))
        else:
            print('Added user: {}'.format(new['login'].lower()))

        # check user_id
        user_id = str(new['id'])
        if github_id != user_id:
            logging.error('User ID Mismatch: {} != {}'.format(github_id, user_id))

        return new

    def update_users(self):
        """Update cached data about linked users in Firestore."""
        # get Broadies that have linked their GitHub accounts.
        if not self.users:
            self.users = self._get_users()
        if self.verbose:
            print('Found {} Tokens in GitHub App.'.format(len(self.users)))

        if not self.github_users:
            self.github_users = self._get_firestore_github_users()
        if self.verbose:
            print('Found {} GitHub Users in Firestore.'.format(len(self.github_users)))

        # update users
        github_users = []
        updates = []
        for email in sorted(self.users, key=lambda x: self.users[x]['login'].lower()):
            # get user from github app with stored token
            linked_user = self.users[email]
            github_id = linked_user['github_id']
            login = linked_user['login']
            token = linked_user['token']

            # get cached user from firestore
            user = self.github_users.get(github_id, {})
            new = self.update_user(github_id, login, token, user)

            # add updated user to list
            github_users.append(new)

            # if updated, add to updates
            if new != user:
                updates.append(new)

        if self.verbose:
            print('Updated {} GitHub Users.'.format(len(updates)))

        return github_users
