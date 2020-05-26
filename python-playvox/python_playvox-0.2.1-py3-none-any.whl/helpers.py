from python_playvox.errors import PlayvoxException
import json
import requests


class PlayvoxMixin:
    def __init__(self, client):
        self.client = client

    def _raise_generic_playvox_exception(self, res):
        raise PlayvoxException('The API call failed: \n {}'.format(
            json.dumps(res)))


class Client:
    def __init__(self, pv_subdomain, uid, key):
        self.auth = (uid, key)
        self.url = 'https://{}.playvox.com/api/v1/'.format(pv_subdomain)
        self.ui_api_url = 'https://{}.playvox.com/v1/'.format(pv_subdomain)
        self.pv_subdomain = pv_subdomain

    def make_request(self, method='GET', endpoint=None, data=None, params=None):
        if method == 'GET':
            return requests.get(self.url+endpoint, auth=self.auth, params=params).json()
        elif method == 'POST':
            return requests.post(self.url+endpoint, data=data, auth=self.auth, params=params).json()
        elif method == 'PUT':
            return requests.put(self.url+endpoint, data=data, auth=self.auth, params=params).json()
        elif method == 'DELETE':
            return requests.delete(self.url+endpoint, params=params).json()
        else:
            error_message = "{} is not a valid request method.".format(method)
            raise ValueError(error_message)

    def make_ui_api_request(self, method='GET', endpoint=None, data=None, params=None):
        if method == 'GET':
            return requests.get(self.ui_api_url+endpoint, auth=self.auth, data=None, params=params).json()
        elif method == 'POST':
            return requests.post(self.ui_api_url+endpoint, data=data, auth=self.auth, params=params).json()
        elif method == 'PUT':
            return requests.put(self.ui_api_url+endpoint, data=data, auth=self.auth, params=params).json()
        elif method == 'DELETE':
            return requests.delete(self.ui_api_url+endpoint, params=params).json()
        else:
            error_message = "{} is not a valid request method.".format(method)
            raise ValueError(error_message)


class Coaching(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parametrs:

        - include(string): use include='all' to include all coaching related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of coaching data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='coachings', params=kwargs)


class Learning(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all learning related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of learnings data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='learning-results', params=kwargs)


class Campaign(PlayvoxMixin):
    def get(self, campaign_id=None, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all campaign related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of campaign data that match the specified parameters*
        '''
        if not campaign_id:
            return self.client.make_request(endpoint='campaigns', params=kwargs)
        else:
            return self.client.make_request(endpoint='campaigns/{}'
                                            .format(campaign_id))

    def vars(self, campaign_id):
        '''
        Parameters:

        - campaign_id(string) *required*: campaign ID to pull vars data for

        *Returns a dict containing vars data for the specified campaign*
        '''
        return self.client.make_request(endpoint='campaigns/{}/actions'
                                        .format(campaign_id), params={'o': 'vars-by-type'})

    def users(self, campaign_id):
        '''
        Parameters:

        - campaign_id(string) *required*: campaign ID to pull users data for

        *Returns a dict containing users data for the specified campaign*
        '''
        return self.client.make_request(endpoint='campaigns/{}/actions'.format(campaign_id), params={
            'o': 'users'})

    def send_data(self, campaign_id, data):
        '''
        Parameters:

        - campaign_id(string) *required*: id of campaign to send campaign metric data to
        - data(dict or list[dict]) *required*: metric data to add to the campaign

        *Returns True if the data was successfully added, otherwise an error is raised*
        '''
        res = self.client.make_request(method='POST',
                                       endpoint='campaigns/{}/metrics'.format(campaign_id), data=data)
        if res['result']['total_errors'] > 0:
            msg = 'The following errors have occured\n' + '\n'.join(
                res['result']['errors']
            )
            raise PlayvoxException(msg)
        else:
            return True


class Calibration(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all calibration related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of calibration data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='calibrations', params=kwargs)


class Evaluation(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all evaluation related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of evaluation data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='evaluations', params=kwargs)


class Scorecard(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all scorecard related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of scorecard data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='scorecards', params=kwargs)


class Team(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all team related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of team data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='teams', params=kwargs)

    def new(self, name, description, team_leaders, users):
        '''
        Parameters:

        - name(string) *required*: name of the new team
        - description(string): description of the new team
        - team_leaders(list) *required*: a list of the user ids of team leaders
        - users(list): a list of the user ids of team members

        *Returns the id of the newly created team*
        '''
        payload = {
            'name': name,
            'description': description,
            'team_leader_id': team_leaders,
            'users': users
        }
        res = self.client.make_request(
            method='POST', endpoint='teams', data=payload)
        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['result']['_id']

    def update(self, team_id, **kwargs):
        '''
        Parameters:

        - team_id(string) *required*: the id of the team to be updated
        - name(string): the new name of the team
        - description(string): the new description for the team
        - team_leader_id(list): a list of user ids for team leaders to replace the current list
        - users(list): a list of user ids for users to replace the current list

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(method='POST', endpoint='teams/{}'.format(
            team_id), data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def add_user(self, team_id, user_id):
        '''
        Parameters:

        - team_id(string) *required*: the id of the team the user will be added to
        - user_id(string) *required*: the id of the user that will be added to the team

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(method='POST', endpoint='teams/{}'.format(
            team_id), data={"id": user_id})

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def remove_user(self, team_id, user_id):
        '''
        Parameters:

        - team_id(string) *required*: the id of the team that the user will be removed from
        - user_id(string) *required*: the id of the user that will be removed from the team

        *Returns True if successful, otherwise an error will be raised*
        '''

        res = self.client.make_request(method='DELETE',
                                       endpoint='teams/{}/users/{}'.format(team_id, user_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, team_id):
        '''
        Parameters:

        - team_id(string) *required*: the id of the team that will be deleted

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(method='DELETE', endpoint='teams/{}'.format(
            team_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True


class User(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all user related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict containing user data for the specified parameters*
        '''
        return self.client.make_request(endpoint='users', params=kwargs)

    def new(self, first_name, last_name, username, email, password, **kwargs):
        '''
        Parameters:

        - first_name(string) *required*: the new user's first name
        - last_name(string) *required*: the new user's last name
        - username(string) *required*: the username that the new user will login with
        - email(string) *required*: the new user's email address
        - password(string) *required*: the new user's password
        - at least 10 characters
        - 1 numer required
        - 1 uppercase letter required
        - 1 lowercase letter required
        - integrations_{integration_name}(string): the user's integration ID for the specified integration, acceptable integration names include:
        - five9
        - zendesk
        - salesforce
        - livechat
        - ringcentral
        - intercom
        - freshdesk
        - talkdesk
        - sopim
        - kustomer
        - helpscout
        - helpshift

        *Returns the id of the new user*
        '''
        payload = {
            'name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password,
        }

        for k, v in kwargs:
            payload[k] = v

        res = self.client.make_request(
            endpoint='users', method='POST', data=payload)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['result']['_id']

    def update(self, user_id, **kwargs):
        '''
        Parameters:

        - user_id(string) *required*: the id of the user to be updated
        - name(string): the new first name for the specified user
        - last_name(string): the new last name for the specified user
        - integrations_{integration_name}(string): the user's integration ID for the specified integration, acceptable integration names include:
        - five9
        - zendesk
        - salesforce
        - livechat
        - ringcentral
        - intercom
        - freshdesk
        - talkdesk
        - sopim
        - kustomer
        - helpscout
        - helpshift

        *Returns True if the user was updated successfully, otherwise an error will be raised*
        '''

        res = self.client.make_request(endpoint='users/{}'.format(user_id),
                                       method='POST', data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def deactivate(self, user_id, deactivation_type, reason):
        '''
        Parameters:

        - user_id(string) *required*: the id of the user to be deactivated
        - deactivation_type(string) *required*: the type of deactivation
        - reason(string) *required*: the reason the user is being deactivated

        *Returns True if successful, otherwise an error will be raised*
        '''
        payload = {
            "status": "inactive",
            "deactivation_type": deactivation_type,
            "deactivation_reason": reason
        }

        res = self.client.make_request(endpoint='users/{}'.format(user_id),
                                       method='POST', data=payload)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def activate(self, user_id):
        '''
        Parameters:

        - user_id(string) *required*: the id of a previously deactivated user to be activated

        *Returns True if succesful, otherwise an error will be raised*
        '''
        payload = {
            "status": "active",
            "deactivation_type": "",
            "deactivation_reason": ""
        }

        res = self.client.make_request(endpoint='users/{}'.format(user_id),
                                       method='POST', data=payload)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True


class Role(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        Parameters:

        - include(string): use include='all' to include all role related objects information
        - page(int): page number for data pagination
        - per_page(int): number of resources per page for data pagination
        - query(string): JSON specifying resource filters
        - fields(string): comma separated list of fields to be returned from the resource
        - sort(string): comma separated list of sort attributes. Use + as prefix for ascending and - as prefix for descending

        *Returns a dict of role data that match the specified parameters*
        '''
        return self.client.make_request(endpoint='roles', params=kwargs)


class Integration(PlayvoxMixin):
    def get(self):
        '''
        *Returns all available integrations*
        '''
        return self.client.make_request(endpoint='integrations')

    def new(self, name, description, data_storage_minutes):
        '''
        Parameters:

        - name(string) *required*: name for the new integration
        - description(string) *required*: description for the new integration
        - data_storage_minutes(int) *required*: the time in minutes to retain data from the integration
          - Max: 129600(90 days)

        *Returns the id of the newly created integration*
        '''
        payload = {
            'name': name,
            'description': description,
            'settings': {
                'data_storage_minutes': data_storage_minutes
            }
        }

        res = self.client.make_request(endpoint='integrations', method='POST',
                                       data=payload)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['_id']

    def update(self, integration_id, **kwargs):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration to be updated
        - name(string): a new name for the integration
        - description(string): a new description for the integration
        - data_storage_minutes(int): the time in minutes to retain data from the integration
          - Max: 129600(90 days)

        *Returns True if the specified integration is updated successfully, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}'.format(
            integration_id), method='PUT', data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, integration_id):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration to be deleted

        *Returns True if the specified integration is deleted successfully, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}'.format(
            integration_id), method='DELETE')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def add_metadata(self, integration_id, field_id, m_type, allowed, required,
                    available_in):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration that the metadata field will be added to
        - field_id(string) *required*: name to identify the metadata field
            - Minimum 3 characters
            - Maximum 30 characters
            - Accepts only a-z and underscores
        - m_type(string) *required*: the type of the field, allowed values:
            - string
            - integer
            - float
            - list
            - boolean
            - datetime
        - allowed(list) *required*: the allowed values that the filed will accept
        - required(boolean) *required*: specifies whether or not the field is required
        - available_in(list[string]): specifies if the field can be filtered or shown in related data, accepts:
            - 'filters'
            - 'display'

        *Returns the id of the new metadata field if successful, otherwise an error will be raised*
        '''
        payload={
            'integration_id': integration_id,
            'field_id': field_id,
            'type': m_type,
            'allowed': allowed,
            'required': required,
            'available_in': available_in
        }

        res = self.client.make_request(endpoint='integrations/{}/metadata'.format(
            integration_id), method='POST', data=payload)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        for md in res['metadata']:
            if md['field_id'] == field_id:
                return md['_id']


    def update_metadata(self, integration_id, metadata_id, **kwargs):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration that the target metadata field exists on
        - metadata_id(string) *required*: the id of the metadata field that will be updated
        - field_id(string): name to identify the metadata field
            - Minimum 3 characters
            - Maximum 30 characters
            - Accepts only a-z and underscores
        - m_type(string): the type of the field, allowed values:
            - string
            - integer
            - float
            - list
            - boolean
            - datetime
        - allowed(list): the allowed values that the filed will accept
        - required(boolean): specifies whether or not the field is required
        - available_in(list[string]): specifies if the field can be filtered or shown in related data, accepts:
            - 'filters'
            - 'display'

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}/metadata/{}'\
            .format(integration_id, metadata_id), data=kwargs, method='PUT')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete_metadata(self, integration_id, metadata_id):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration that the target metadata field exists on
        - metadata_id(string) *required*: the id of the metadata field to be deleted

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}/metadata/{}'\
            .format(integration_id, metadata_id), method='DELETE')
        
        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    

class Interaction(PlayvoxMixin):
    def get(self, integration_id):
        '''
        Parameters:

        - integration_id(string) *required* The id of the integration to get integrations for.

        *Returns all interactions for the specified integration*
        '''
        return self.client.make_request(endpoint='integrations/{}/interactions'\
            .format(integration_id))

    def add(self, integration_id, interaction_id, assignee_id, 
                        custom_metadata):
        '''
        Parameters:

        - integration_id(string) *required*: The id of the integration the interaction will be added to.
        - interaction_id(string): The id of your external system
            - Max length: 68 characters
        - assignee_id(string): The id of the user on the external system (should match email or username in playvox)
        - custom_metadata(dict) *required*: The payload of all the metadata fields defined on the integration

        *Returns the id of the new interaction*
        '''
        custom_metadata['interaction_id'] = interaction_id
        custom_metadata['assignee_id'] = assignee_id

        res = self.client.make_request(endpoint='integrations/{}/interactions'\
            .format(integration_id), data=custom_metadata, method='POST')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['_id']

    def update(self, integration_id, interaction_id, data):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration the target interaction exists on
        - interaction_id(string) *required*: the id of the interaction to be updated
        - data(dict) *required*: The payload of the metadata fields to be updated

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}/interactions/{}'\
            .format(integration_id, interaction_id), data=data, method='PUT')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, integration_id, interaction_id):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration the target interaction exists on
        - interaction_id(string) *required*: the id of the interaction to be deleted

        *Returns True if successful, otherwise an error will be raised*
        '''
        res = self.client.make_request(endpoint='integrations/{}/interactions/{}'\
            .format(integration_id, interaction_id, method='DELETE'))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def get_comments(self, interaction_id):
        '''
        Parameters:

        - interaction_id(string) *required*: the id of the interaction to get comments for

        *Returns all comments associated with the interaction*
        '''
        return self.client.make_request(endpoint='interactions/{}/comments'\
            .format(interaction_id))

    def add_comment(self, interaction_id, body, comment_type, author_id,
                    comment_dt=None):
        '''
        Parameters:

        - interaction_id(string) *required*: the id of the interaction the comment will be added to
        - body(string) *required*: the body of the comment
        - comment_type(string) *required*: the type of comment, accepts:
            - 'customer_comment'
            - 'agent_comment'
            - 'internal_note'
        - author_id(string) *required*: the username or email of the author on playvox
        - comment_dt(datetime): the time that the comment was added to the interaction, defaults to current time if not specified

        *Returns the id of the newly created comment*
        '''
        data = {
            'body': body,
            'type': comment_type,
            'author_id': author_id
        }
        if comment_dt:
            data['added_at'] = comment_dt.strftime('%Y-%m-%dT%H:%M:%S%Z')
        
        res = self.client.make_request(endpoint='interactions/{}/comments'\
            .format(interaction_id), data=data, method='POST')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['result']['_id']

    def update_comment(self, interaction_id, comment_id, body, comment_dt=None):
        '''
        Parameters:

        - interaction_id(string) *required*: the id of the interaction that the comment is associated with
        - comment_id(string) *required*: the id of the comment to be updated
        - body(string) *required*: the new body of the comment
        - comment_dt(datetime): the time that the comment was updated, defaults to current time if not specified

        *Returns True if the comment is updated successfully, otherwise an error will be raised*
        '''
        data = {
            'body': body,
        }

        if comment_dt:
            data['added_at'] = comment_dt.strftime('%Y-%m-%dT%H:%M:%S%Z')

        res = self.client.make_request(endpoint='interactions/{}/comments/{}'\
            .format(interaction_id, comment_id), data=data, method='PUT')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete_comment(self, interaction_id, comment_id):
        '''
        Parameters:

        - interaction_id(string) *required*: the id of the interaction that the target comment is associated with
        - comment_id(string) *required*: the id of the comment to be deleted

        *Returns True if the comment is deleted successfully, otherwise an error will be raised*
        '''

        res = self.client.make_request(endpoint='interactions/{}/comments/{}'\
            .format(interaction_id, comment_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def bulk_add(self, integration_id, interactions):
        '''
        Parameters:

        - integration_id(string) *required*: the id of the integration that the interactions will be added to
        - interactions(dict) *required*: the interactions to be added to the integration, for more information see the [Playvox API Documentation](https://developers.playvox.com/restapis/#/reference/0/bulk-interactions/create)

        *Returns the job id of the bulk job*
        '''

        res = self.client.make_request(endpoint='integrations/{}/bulk/interactions'\
            .format(integration_id), data=interactions, method='POST')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['result']['_id']

    def bulk_status(self, job_id):
        '''
        Parameters:

        - job_id(string) *required*: the id of the bulk job to check the status of

        *Returns status information on the specified bulk job*
        '''
        return self.client.make_request(endpoint='jobs/{}'.format(job_id))