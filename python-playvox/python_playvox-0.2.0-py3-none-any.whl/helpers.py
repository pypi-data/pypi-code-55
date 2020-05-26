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
        :param include: use include='all' to include all coaching related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing coachings data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='coachings', params=kwargs)


class Learning(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        :param include: use include='all' to include all coaching related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing learning data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='learning-results', params=kwargs)


class Campaign(PlayvoxMixin):
    def get(self, campaign_id=None, **kwargs):
        '''
        :param include: use include='all' to include all coaching related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing campaign data
        :rtype: dict
        '''
        if not campaign_id:
            return self.client.make_request(endpoint='campaigns', params=kwargs)
        else:
            return self.client.make_request(endpoint='campaigns/{}'
                                            .format(campaign_id))

    def vars(self, campaign_id):
        '''
        :param campaign_id: campaign ID to pull vars data for
        :type campaign_id: string
        :return: Response containing vars data for the specified campaign.
        :rtype: dict
        '''
        return self.client.make_request(endpoint='campaigns/{}/actions'
                                        .format(campaign_id), params={'o': 'vars-by-type'})

    def users(self, campaign_id):
        '''
        :param campaign_id: campaign ID to pull users data for
        :type campaign_id: string
        :return: Response containing users data for the specified campaign.
        :rtype: dict
        '''
        return self.client.make_request(endpoint='campaigns/{}/actions'.format(campaign_id), params={
            'o': 'users'})

    def send_data(self, campaign_id, data):
        '''
        :param campaign_id: campaign ID to send campaign metric data to
        :param data: metric data to add to the campaign
        :type campaign_id: string
        :type data: dict or list[dict]
        :return: Returns true if the data was successfully added, otherwise an error is raised.
        :rtype: boolean
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
        :param include: use include='all' to include all calibration related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing calibration data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='calibrations', params=kwargs)


class Evaluation(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        :param include: use include='all' to include all evaluation related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing evaluations data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='evaluations', params=kwargs)


class Scorecard(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        :param include: use include='all' to include all scorecard related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing scorecards data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='scorecards', params=kwargs)


class Team(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        :param include: use include='all' to include all team related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing team data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='teams', params=kwargs)

    def new(self, name, description, team_leaders, users):
        '''
        :param name: name of the new team
        :param description: team description
        :team_leaders: a list of the user ids of team leaders
        :users: a list of the user ids of team members
        :type name: string
        :type description: string
        :type team_leaders: list
        :typer users: list
        :return: The team ID of the new team.
        :rtype: string
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
        :param name: the new name for the existing team
        :param description: the new description for the existing team
        :param team_leader_id: a list of user ids for team leaders to replace the current list
        :param users: a list of user ids for users to replace the current list of users
        :type name: string
        :type description: string
        :type team_leader_id: list
        :type users: list
        :return: Returns True if updated successfuly, otherwise an error will be raised.
        :rtype: boolean
        '''
        res = self.client.make_request(method='POST', endpoint='teams/{}'.format(
            team_id), data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def add_user(self, team_id, user_id):
        '''
        :param team_id: The id of the team that the user will be added to
        :param user_id: The id of the user that will be added to the team
        :type team_id: string
        :type user_id: string
        :return: Returns True if successful, otherwise an error will be raised.
        :rtype: boolean
        '''

        res = self.client.make_request(method='POST', endpoint='teams/{}'.format(
            team_id), data={"id": user_id})

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def remove_user(self, team_id, user_id):
        '''
        :param team_id: the id of the team the user will be removed from
        :param user_id: the id of the user to be removed from the team
        :type team_id: string
        :type user_id: string
        :return: Returns True if successful, otherwise an error will be raised.
        :rtype: boolean
        '''

        res = self.client.make_request(method='DELETE',
                                       endpoint='teams/{}/users/{}'.format(team_id, user_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, team_id):
        '''
        :param team_id: The id of the team to be deleted.
        :type team_id: string
        :return: Returns True if successful, otherwise an error will be raised.
        :rtype: boolean
        '''

        res = self.client.make_request(method='DELETE', endpoint='teams/{}'.format(
            team_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True


class User(PlayvoxMixin):
    def get(self, **kwargs):
        '''
        :param include: use include='all' to include all user related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing user data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='users', params=kwargs)

    def new(self, first_name, last_name, username, email, password, **kwargs):
        '''
        :param first_name: the new user's first name
        :param last_name: the new user's last name
        :param username: the username the user will login with
        :param email: the user's email address
        :param password: the new user's password, at least 10 characters including a number, uppercase letter, and lowercase letter
        :param integrations_{integration name}: the user's integration ID for the specified integration. Acceptable integration names include: five9, zendesk, desk, salesforce, livechat, ringcentral, intercom, freshdesk, talkdesk, zopim, kustomer, helpscout and helpshift.
        :type first_name: string
        :type last_name: string
        :type username: string
        :type email: string
        :type password: string
        :type integrations_{integration name}: string
        :return: Returns the id of the new user
        :rtype: string
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
        :param user_id: The id of the user to be updated
        :param name: the new first name for the specified user
        :param last_name: the new last name for the specified user
        :param integrations_{integration name}: the user's integration ID for the specified integrations. available integration names include: five9, zendesk, desk, salesforce, livechat, ringcentral, intercom, freshdesk, talkdesk, zopim, kustomer, helpscout, and helpshift.
        :type user_id: string
        :type name: string
        :type last_name: string
        :type integrations_{integration name}: string
        :return: Returns True if the user updated successfully, otherwise an error is raised.
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='users/{}'.format(user_id),
                                       method='POST', data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def deactivate(self, user_id, deactivation_type, reason):
        '''
        :param user_id: the id of the user to be deactivated
        :param deactivation_type: the type of deactivation
        :param deactivation_reason: the reason for deactivation
        :type user_id: string
        :type deactivation_type: string
        :type deactivation_reason: string
        :return: Returns True if the user is successfuly deactivated, otherwise an error is raised.
        :rtype: boolean
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
        :param user_id: the id of a previously deactivated user to be activated
        :type user_id: string
        :return: Returns True if the user is successfully activated. Otherwise an error will be raised.
        :rtype: boolean
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
        :param include: use include='all' to include all role related objects information
        :param page: page number for data pagination
        :param per_page: number of resources per page for data pagination (max: 100, default: 12)
        :param query: JSON specifying resource filters
        :param fields: comma separated list of fields to be returned from the resource
        :param sort: comma separated list of sort atributes. Use + as prefix for ascending and - as prefix for descending
        :type include: string
        :type page: int
        :type per_page: int
        :type query: string (json)
        :type fields: string
        :type sort: string:
        :return: Response containing role data
        :rtype: dict
        '''
        return self.client.make_request(endpoint='scorecards', params=kwargs)


class Integration(PlayvoxMixin):
    def get(self):
        '''
        :return: Returns all available integrations
        :rtype: dict
        '''

        return self.client.make_request(endpoint='integrations')

    def new(self, name, description, data_storage_minutes):
        '''
        :param name: name of the integration
        :param description: description for the integration
        :param data_storage_minutes: the time in minutes to retain data from the integration, Max: 129600 (90 days).
        :type name: string
        :type description: string
        :type data_storage_minutes: int
        :return: Returns the id of the newly created integration.
        :rtype: string
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
        :param integration_id: the id of the integration to be updated
        :param name: new name for the specified integration
        :param description: new description for the integration
        :param data_storage_minutes: the time in minutes to retain data from the integration. Max: 129600 (90 days).
        :type integration_id: string
        :type name: string
        :type description: string
        :type data_storage_minutes: int
        :return: returns True if successful, otherwise an error is raised.
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='integrations/{}'.format(
            integration_id), method='PUT', data=kwargs)

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, integration_id):
        '''
        :param integration_id: the ID of the integration to delete
        :type integration_id: string
        :return: returns True if the integration is deleted successfully, otherwise an error is raised.
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='integrations/{}'.format(
            integration_id), method='DELETE')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def add_metadata(self, integration_id, field_id, m_type, allowed, required,
                    available_in):
        '''
        :param integration_id: the id of the integration to which the metadata will be added
        :param field_id: name to identify the field, a minimum of 3 characters and a maximum of 30 characters, ony a-z and underscores are accepted.
        :param m_type: the type of the field. allowed values are string, integer, float, list, boolean, and datetime
        :param allowed: the allowed values that the field will accept
        :param required: specifies whether or not the field is required
        :param available_in: specify if the field can be filtered or available to show in all fields, accepted values include 'filters' and 'display'
        :type integration_id: string
        :type field_id: string
        :type m_type: string
        :type allowed: list
        :type required: boolean
        :type available_in: list
        :return: Returns the metadata_id if successful, otherwise an error is raised.
        :rtype: string
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
        :param integration_id: the id of the integration that the metadata field exists on
        :param metadata_id: the id of the metadata field that will be updated
        :param field_id: name to identify the field, a minimum of 3 characters and a maximum of 30 characters, ony a-z and underscores are accepted.
        :param m_type: the type of the field. allowed values are string, integer, float, list, boolean, and datetime
        :param allowed: the allowed values that the field will accept
        :param required: specifies whether or not the field is required
        :param available_in: specify if the field can be filtered or available to show in all fields, accepted values include 'filters' and 'display'
        :type integration_id: string
        :type metadata_id: string
        :type field_id: string
        :type m_type: string
        :type allowed: list
        :type required: boolean
        :type available_in: list
        :return: returns True if successful, otherwise an error is raised.
        :rtype: boolean
        '''
        res = self.client.make_request(endpoint='integrations/{}/metadata/{}'\
            .format(integration_id, metadata_id), data=kwargs, method='PUT')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete_metadata(self, integration_id, metadata_id):
        '''
        :param integration_id: the id of the integration that the metadata field exists on
        :param metadata_id: the id of the metadata field to be deleted
        :type integration_id: string
        :type metadata_id: string
        :return: returns True if successful, otherwise an error is raised
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='integrations/{}/metadata/{}'\
            .format(integration_id, metadata_id), method='DELETE')
        
        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    

class Interaction(PlayvoxMixin):
    def get(self, integration_id):
        '''
        :param integration_id: The id of the integration to get interagions for.
        :type integration_id: string
        :return: returns all interactions for the specified integration
        :rtype: dict
        '''

        return self.client.make_request(endpoint='integrations/{}/interactions'\
            .format(integration_id))

    def add(self, integration_id, interaction_id, assignee_id, 
                        custom_metadata):
        '''
        :param integration_id: The id of the integration the interaction will be added to.
        :param interaction_id: the id of your external system, max length 68 characters.
        :param assignee_id: the id of the user on the external system (should match email or username in playvox)
        :param custom_metadata: The payload of all the metadata defined on the integration.
        :type integration_id: string
        :type interaction_id: string
        :type assignee_id: string
        :type custom_metadata: dict
        :return: Returns the id of the new interaction
        :rtype: string
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
        :param integration_id: the id of the integration the interaction exists on
        :param interaction_id: the id of the interaction to update
        :param data: the data to be updated on the interaction
        :type integration_id: string
        :type interaction_id: string
        :type data: dict
        :return: returns True if the interaction is update successfully, otherwise an error will be raised
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='integrations/{}/interactions/{}'\
            .format(integration_id, interaction_id), data=data, method='PUT')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def delete(self, integration_id, interaction_id):
        '''
        :param integration_id: the id of the integration the interaction exists on
        :param interaction_id: the id of the interaction to delete
        :type integration_id: string
        :type interaction_id: string
        :return: returns True if the interaction is deleted successfully, otherwise an error is raised
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='integrations/{}/interactions/{}'\
            .format(integration_id, interaction_id, method='DELETE'))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def get_comments(self, interaction_id):
        '''
        :param interaction_id: the id of the interaction to get comments for
        :type interaction_id: string
        :return: returns all comments associated with the interaction
        :rtype: dict
        '''

        return self.client.make_request(endpoint='interactions/{}/comments'\
            .format(interaction_id))

    def add_comment(self, interaction_id, body, comment_type, author_id,
                    comment_dt=None):
        '''
        :param interaction_id: the id of the interaction to add the comment to
        :param body: the body of the comment
        :param comment_type: the type of the comment, accepted values are customer_comment, agent_comment, and internal_note
        :param author_id: the username or email of the author on playvox
        :param comment_dt: the time that the comment was added to the interaction, defaults to current time if not specified
        :type interaction_id: string
        :type body: string
        :type comment_type: string
        :type author_id" string
        :type comment_dt: datetime
        :return: returns the id of the newly created comment
        :rtype: string
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
        :param interaction_id: the interaction that the comment is associated with
        :param comment_id: the id of the comment to be updated
        :param body: the new body of the comment
        :param comment_dt: the time that the comment was updated, defaults to current time if not specified
        :type interaction_id: string
        :type comment_id: string
        :type body: string
        :type comment_dt: datetime
        :return: returns True if the comment is updated successfully, otherwise an error is raised
        :rtype: boolean
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
        :param interaction_id: the interaction that the comment is associated with
        :param comment_id: the id of the comment to be deleted
        :type interaction_id: string
        :type comment_id: string
        :return: returns True if successful, otherwise an error is raised
        :rtype: boolean
        '''

        res = self.client.make_request(endpoint='interactions/{}/comments/{}'\
            .format(interaction_id, comment_id))

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return True

    def bulk_add(self, integration_id, interactions):
        '''
        :param integration_id: the id of the integration that the interactions will be added to
        :param interactions: the interactions to be added to the integration, for more information see https://developers.playvox.com/restapis/#/reference/0/bulk-interactions/create
        :type integration_id: string
        :type interactions: list[dict]
        :return: returns the job id of the bulk job
        :rtype: string
        '''

        res = self.client.make_request(endpoint='integrations/{}/bulk/interactions'\
            .format(integration_id), data=interactions, method='POST')

        if not res['success']:
            self._raise_generic_playvox_exception(res)

        return res['result']['_id']

    def bulk_status(self, job_id):
        '''
        :param job_id: the id of the bulk job to check the status of
        :type job_id: string
        :return: returns information on the specified bulk job
        :rtype: dict
        '''
        return self.client.make_request(endpoint='jobs/{}'.format(job_id))