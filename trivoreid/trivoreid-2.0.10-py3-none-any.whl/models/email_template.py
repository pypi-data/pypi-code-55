#!/usr/bin/env python
# coding: utf-8

class EmailTemplate(object):
    '''
    Wrapper for a single email template.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): email template fields
        Dictionary keys:
            'id' entity ID
            'name' name of email template
            'description' description of email template purpose
            'templateEngine' template engine used to process templates
            'defaultLocale' default locale, used to pick translation if one
                            cannot be picked otherwise
            'defaultTimeZone' default timezone, used if preferred timezone
                              not specified
            'subjectTemplate' template for message's subject field
            'htmlTemplate' template for message's HTML content
            'textTemplate' template for message's plain text content
            'localeProperties' locale specific properties. Those for default
                               locale and those for preferred locale will be
                               used when processing message.
            'namespaceIds' IDs of namespaces where admins and clients can see
                           and use this template
        '''
        self.id = data.pop('id', None)
        self.name = data.pop('name', None)
        self.description = data.pop('description', None)
        self.templateEngine = data.pop('templateEngine', None)
        self.defaultLocale = data.pop('defaultLocale', None)
        self.defaultTimeZone = data.pop('defaultTimeZone', None)
        self.subjectTemplate = data.pop('subjectTemplate', None)
        self.htmlTemplate = data.pop('htmlTemplate', None)
        self.textTemplate = data.pop('textTemplate', None)
        self.localeProperties = data.pop('localeProperties', {})
        self.namespaceIds = data.pop('namespaceIds', [])

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'id'                : self.id,
            'name'              : self.name,
            'description'       : self.description,
            'templateEngine'    : self.templateEngine,
            'defaultLocale'     : self.defaultLocale,
            'defaultTimeZone'   : self.defaultTimeZone,
            'subjectTemplate'   : self.subjectTemplate,
            'htmlTemplate'      : self.htmlTemplate,
            'textTemplate'      : self.textTemplate,
            'localeProperties'  : self.localeProperties,
            'namespaceIds'      : self.namespaceIds
        }

class SendMessageOptions(object):
    '''
    Wrapper for sending message options with email templates.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): email template fields
        Dictionary keys:
            'recipients' message recipients. List of RecipientDetails objects
            'preferredLocale' preferred locale if not specified for recipient
            'preferredTimezone' preferred timezone if not specified
                                for recipient
            'properties' extra properties for template. Recipient properties are
                         added to these. Don't use period characters in keys.
        '''

        self.recipients = []
        for r in data.pop('recipients', []):
            self.recipients.append(RecipientDetails(r))

        self.preferredLocale = data.pop('preferredLocale', None)
        self.preferredTimezone = data.pop('preferredTimezone', None)
        self.properties = data.pop('properties', {})

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        recipients = []
        for r in self.recipients:
            recipients.append(r.serialize())

        return {
            'recipients'        : recipients,
            'preferredLocale'   : self.preferredLocale,
            'preferredTimezone' : self.preferredTimezone,
            'properties'        : self.properties
        }

class RecipientDetails(object):
    '''
    Wrapper for a single recipient details.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): email template fields
        Dictionary keys:
            'emailAddress' email address that is added to 'To' field. If not
                           specified, user's primary email address is used.
            'userId' recipient user ID. User information can be used
                     in template.
            'preferredLocale' preferred locale, used for translation and
                              formatting. If not specified, User's locale
                              preference is used.
            'preferredTimezone' preferred timezone, used for time and date
                                operations. If not specified, User's timezone
                                preference is used.
            'properties' properties for template. These are added on top of base
                         properties. Don't use period characters in keys.
        '''
        self.emailAddress = data.pop('emailAddress', None)
        self.userId = data.pop('userId', None)
        self.preferredLocale = data.pop('preferredLocale', None)
        self.preferredTimezone = data.pop('preferredTimezone', None)
        self.properties = data.pop('properties', {})

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'emailAddress'      : self.emailAddress,
            'userId'            : self.userId,
            'preferredLocale'   : self.preferredLocale,
            'preferredTimezone' : self.preferredTimezone,
            'properties'        : self.properties
        }
