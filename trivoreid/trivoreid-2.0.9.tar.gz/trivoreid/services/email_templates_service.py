#!/usr/bin/env python
# coding: utf-8

import requests
import string
import random
import logging

import trivoreid.utils.service_utils as su
from trivoreid.utils.criteria import Filter
from trivoreid.models.page import Page
from trivoreid.models.email_template import EmailTemplate, SendMessageOptions
from trivoreid.exceptions import TrivoreIDSDKException, TrivoreIDException


class EmailTemplatesService(object):
    '''
    Class to wrap Trivore ID /emailtemplate APIs
    '''

    _EMAIL_TEMPLATES = 'api/rest/v1/emailtemplate'
    _EMAIL_TEMPLATE = 'api/rest/v1/emailtemplate/{}'
    _EMAIL_TEMPLATE_SEND = 'api/rest/v1/emailtemplate/{}/send'

    def __init__(self, credentials):
        self._server = credentials.server

        if credentials.oidc_client is None:
            self._session = requests
            self._auth = credentials.auth
        else:
            self._session = credentials.oidc_client
            self._auth = None

        self._header = credentials.access_token

    def get_all(self,
                filter_fields=None,
                start_index=0,
                count=100,
                sortBy=None,
                ascending=None):
        '''Get the list of the email templates.
        Args:
            filter_fields (Filter) : filter out the result.
            start_index (int)      : 0-based pagination start index
            count (int)            : pagination page size, max 500,
                                     100 by default
            sortBy (str)           : Sort by attribute name
            ascending (bool)       : Sort direction (ascending or descending)
        Returns:
            Page with the pagination data and the list of email templates.
        Raises:
            TrivoreIDException if the status code is not 200.
        '''
        params = su.generate_parameters(filter_fields, start_index, count)

        if sortBy != None:
            params['sortBy'] = sortBy

        if ascending != None:
            if ascending:
                params['ascending'] = 'ascending'
            else:
                params['ascending'] = 'descending'

        uri = su.uri(self._server, self._EMAIL_TEMPLATES)
        response = self._session.get(uri, params=params,
                                          headers=self._header,
                                          auth=self._auth)

        if response.status_code is 200:
            logging.debug('Found {} email templates'.format(
                                            len(response.json()['resources'])))
            templates = []
            for template in response.json()['resources']:
                templates.append(EmailTemplate(template))
            page = Page(response.json(), templates)
            return page
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def send(self, emailTemplateId, messageOptions):
        '''Get a single email template by id.
        Args:
            emailTemplateId (str) : unique identifier of the email template that
                                    will be used
            messageOptions (SendMessageOptions) : email template message options
        Raises:
            TrivoreIDException if the status code is not 200.
            TrivoreIDSDKException if the type of the SendMessageOptions is wrong
        '''
        if 'SendMessageOptions' not in str(type(messageOptions)):
            raise TrivoreIDSDKException('SendMessageOptions type is wrong!')

        uri = su.uri(self._server, self._EMAIL_TEMPLATE_SEND
                                            .format(emailTemplateId))
        response = self._session.post(uri,
                                      json=messageOptions.serialize(),
                                      headers=self._header,
                                      auth=self._auth)

        if response.status_code is 204:
            logging.debug('Succesfully sended email with the template with id {}'
                                        .format(emailTemplateId))
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def get(self, emailTemplateId):
        '''Get a single email template details by id.
        Args:
            emailTemplateId (str) : email template's unique identifier
        Returns:
            An email template.
        Raises:
            TrivoreIDException if the status code is not 200.
        '''
        uri = su.uri(self._server, self._EMAIL_TEMPLATE
                                        .format(emailTemplateId))
        response = self._session.get(uri, headers=self._header,
                                          auth=self._auth)

        if response.status_code is 200:
            logging.debug('Found email template with id {}'
                                        .format(emailTemplateId))
            return EmailTemplate(response.json())
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)
