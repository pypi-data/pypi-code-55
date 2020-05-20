#!/usr/bin/env python
# coding: utf-8

from trivoreid.models.misc import Meta
from trivoreid.models.email import EmailAddress
from trivoreid.exceptions import TrivoreIDSDKException

class User(object):
    '''
    The User class that represents a user object.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user fields
        Dictionary keys:
            'id' - user ID
            'username' - sign in name
            'userAccountType' - PERSON or LEGAL_ENTITY
            'nsCode' - namespace code
            'emails' - list of emails. Object of 'EmailAddresses' class
            'mobiles' - list of mobiles. Object of 'Mobiles' class
            'name' - user names. Object of 'Names' class
            'memberOf' - the list of group IDs (when creating new user or
                         modifying existing - can be group names)
            'addresses' - list of addresses. Object of 'Addresses' class

            'locale' - user's preferred locale
            'preferredLanguage' - user's preferred language
            'timeZone' - user's preferred timezone
            'mfaMethod' - multi-factor authentication method (TOTP, SMS or NONE)
            'nickName' - user's nickname or preferred name
            'locked' - user's locked status
            'minor' - is user a legal minor (client defined age). Can be used
                      as alternative to dateOfBirth.
            'websiteMain' - main website
            'websiteAux' - auxiliary website
            'domicileCode' -
            'strongIdentification' - information about last strong
                                     identification event
            'customerGroupInfo' - customer service entered data regarding
                                  customer's special statuses
            'dateOfBirth' - date of birth
            'meta' - meta data

            'gender' - Free-form field for gender
            'sex' - The juridical sex of the user. 'FEMALE', 'MALE', 'OTHER',
                    'UNDISCLOSED'.
            'nationality' - Represents the user's nationality in format
                            ISO 3166-1 Alpha-2, e.g. DE
            'salutation' - End-user’s salutation, e.g. "Mr."
            'title' - End-user’s title, e.g. "Dr."
            'birthFirstName' - First name someone has when they are born, or at
                               least from the time they are a child. This term
                               can be used by a person, who changes the first
                               name later in life for any reason.
            'birthMiddleName' - Middle name someone has when they are born, or
                                at least from the time they are a child. This
                                term can be used by a person, who changes the
                                middle name later in life for any reason.
            'birthLastName' - Last name someone has when he or she is born, or
                              at least from the time he or she is a child. This
                              term can be used by a person who changes the
                              family name later in life for any reason.
            'place_of_birth' - End-user’s place of birth.
        '''

        mobiles = []
        for m in data.pop('mobiles', []):
            mobiles.append(Mobile(m))

        addresses = []
        for a in data.pop('addresses', []):
            addresses.append(Address(a))

        emails = []
        for e in data.pop('emails', []):
            emails.append(EmailAddress(e))

        self.id = data.pop('id', None)
        self.username = data.pop('username', None)
        self.userAccountType = data.pop('userAccountType', None)
        self.nsCode = data.pop('nsCode', None)
        self.memberOf = data.pop('memberOf', [])
        self.name = Names(data.pop('name', {}))
        self.mobiles = mobiles
        self.emails = emails
        self.addresses = addresses
        self.consents = Consents(data.pop('consents', {}))
        self.password = None
        self.locale = data.pop('locale', None)
        self.preferredLanguage = data.pop('preferredLanguage', None)
        self.timeZone = data.pop('timeZone', None)
        self.mfaMethod = data.pop('mfaMethod', None)
        self.nickName = data.pop('nickName', None)
        self.locked = data.pop('locked', False)
        self.minor = data.pop('minor', False)
        self.websiteMain = data.pop('websiteMain', None)
        self.websiteAux = data.pop('websiteAux', None)
        self.domicileCode = data.pop('domicileCode', None)
        self.domicileClasses = data.pop('domicileClasses', [])
        self.dateOfBirth = data.pop('dateOfBirth', None)
        self.strongIdentification = StrongIdentification(
                                           data.pop('strongIdentification', {}))
        self.customerGroupInfo = CustomerGroupInfo(
                                           data.pop('customerGroupInfo', {}))
        self.meta = Meta(data.pop('meta', {}))
        self.gender = data.pop('gender', None)
        self.sex = data.pop('sex', None)
        self.nationality = data.pop('nationality', None)
        self.salutation = data.pop('salutation', None)
        self.title = data.pop('title', None)
        self.birthFirstName = data.pop('birthFirstName', None)
        self.birthMiddleName = data.pop('birthMiddleName', None)
        self.birthLastName = data.pop('birthLastName', None)
        self.placeOfBirth = PlaceOfBirth(data.pop('place_of_birth', {}))
        self.tags = data.pop('tags', [])

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''

        mobiles = []
        for m in self.mobiles:
            mobiles.append(m.serialize())

        addresses = []
        for a in self.addresses:
            addresses.append(a.serialize())

        emails = []
        for e in self.emails:
            emails.append(e.serialize())

        user_serializable = {
            'id': self.id,
            'username': self.username,
            'userAccountType': self.userAccountType,
            'nsCode': self.nsCode,
            'emails': emails,
            'mobiles': mobiles,
            'addresses': addresses,
            'name':  self.name.serialize(),
            'consents': self.consents.serialize(),
            'memberOf': self.memberOf,
            'locale': self.locale,
            'preferredLanguage': self.preferredLanguage,
            'timeZone': self.timeZone,
            'mfaMethod': self.mfaMethod,
            'nickName': self.nickName,
            'locked': self.locked,
            'minor': self.minor,
            'websiteMain': self.websiteMain,
            'websiteAux': self.websiteAux,
            'domicileCode': self.domicileCode,
            'domicileClasses': self.domicileClasses,
            'dateOfBirth': self.dateOfBirth,
            'customerGroupInfo': self.customerGroupInfo.serialize(),
            'strongIdentification': self.strongIdentification.serialize(),
            'meta': self.meta.serialize(),
            'gender': self.gender,
            'sex': self.sex,
            'nationality': self.nationality,
            'salutation': self.salutation,
            'title': self.title,
            'birthFirstName': self.birthFirstName,
            'birthMiddleName': self.birthMiddleName,
            'birthLastName': self.birthLastName,
            'place_of_birth': self.placeOfBirth.serialize(),
            'tags': self.tags
        }

        if self.password is not None:
            user_serializable['password'] = self.password

        return user_serializable

class Names(object):
    '''
    The object containing user's given, middle and family names.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): name fields
        Dictionary keys:
            'givenName' - user's given name
            'middleName' - user's middle name
            'familyName' - user's family name
        '''
        self.givenName = data.pop('givenName', None)
        self.middleName = data.pop('middleName', None)
        self.familyName = data.pop('familyName', None)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'givenName'  : self.givenName,
            'middleName' : self.middleName,
            'familyName' : self.familyName,
        }

class Mobile(object):
    '''
    The object containing the mobile data.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict, str) : mobile fields, or single mobile number.
        Dictionary keys:
            'number' (str) - mobile number
            'verified' (bool) - verification status
        '''
        if type(data) is dict:
            self.name = data.pop('name', None)
            self.number = data.pop('number', None)
            self.verified = data.pop('verified', False)
            self.tags = data.pop('tags', [])
        elif type(data) is str:
            self.number = data
            self.name = None
            self.verified = None
            self.tags = None
        else:
            raise TrivoreIDSDKException('Wrong type of the mobile!')

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'name'      : self.name,
            'number'    : self.number,
            'verified'  : self.verified,
            'tags'      : self.tags
        }

class Address(object):
    '''
    The object containing the user address.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): address fields
        Dictionary keys:
            'addressName'
            'name'
            'country'
            'locality'
            'postalCode'
            'region'
            'streetAddress'
            'type' PERMANENT or TEMPORARY
            'organisation'
            'verified'
            'source'
            'language' ISO 639 2-letter language code.
        '''
        self.addressName = data.pop('addressName', None)
        self.name = data.pop('name', None)
        self.country = data.pop('country', None)
        self.locality = data.pop('locality', None)
        self.region = data.pop('region', None)
        self.postalCode = data.pop('postalCode', None)
        self.streetAddress = data.pop('streetAddress', None)
        self.type = data.pop('type', None)
        self.organisation = data.pop('organisation', None)
        self.verified = data.pop('verified', None)
        self.source = data.pop('source', None)
        self.language = data.pop('language', None)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'addressName': self.addressName,
            'name': self.name,
            'country': self.country,
            'locality': self.locality,
            'postalCode': self.postalCode,
            'region': self.region,
            'streetAddress': self.streetAddress,
            'type': self.type,
            'organisation': self.organisation,
            'verified': self.verified,
            'source': self.source,
            'language': self.language
        }

class Consents(object):
    '''
    Wrapper for the user's marketing consents.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user's consents
        Dictionary keys:
            'marketingPost' (bool)
            'marketingEmail' (bool)
            'marketingPhone' (bool)
            'marketingMobileMessage' (bool)
            'marketingPushNotification' (bool)
            'marketingOther' (bool)
            'locationing' (bool)
            'profiling' (bool)
        '''
        self.marketingPost = data.pop('marketingPost', False)
        self.marketingEmail = data.pop('marketingEmail', False)
        self.marketingPhone = data.pop('marketingPhone', False)
        self.marketingMobileMessage = data.pop('marketingMobileMessage', False)
        self.marketingPushNotification = data.pop('marketingPushNotification', False)
        self.marketingOther = data.pop('marketingOther', False)
        self.locationing = data.pop('locationing', False)
        self.profiling = data.pop('profiling', False)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'marketingPost': self.marketingPost,
            'marketingEmail': self.marketingEmail,
            'marketingPhone': self.marketingPhone,
            'marketingMobileMessage': self.marketingMobileMessage,
            'marketingPushNotification': self.marketingPushNotification,
            'marketingOther': self.marketingOther,
            'locationing': self.locationing,
            'profiling': self.profiling,
        }

class CustomerGroupInfo(object):
    '''
    Wrapper for the user's customer group info.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user's consents
        Dictionary keys:
            'student' (bool)
            'studentIdentifier' (str)
            'studentValidFrom' (str)
            'studentValidTo' (str)
            'studentUpdated' (str)
            'senior' (bool)
            'seniorIdentifier' (str)
            'seniorUpdated' (str)
            'disabilities' (bool)
            'disabilitiesIdentifier' (str)
            'disabilitiesUpdated' (str)
            'studentValidNow' (bool)
        '''

        self.student = data.pop('student', None)
        self.studentIdentifier = data.pop('studentIdentifier', None)
        self.studentValidFrom = data.pop('studentValidFrom', None)
        self.studentValidTo = data.pop('studentValidTo', None)
        self.studentUpdated = data.pop('studentUpdated', None)
        self.senior = data.pop('senior', None)
        self.seniorIdentifier = data.pop('seniorIdentifier', None)
        self.seniorUpdated = data.pop('seniorUpdated', None)
        self.disabilities = data.pop('disabilities', None)
        self.disabilitiesIdentifier = data.pop('disabilitiesIdentifier', None)
        self.disabilitiesUpdated = data.pop('disabilitiesUpdated', None)
        self.studentValidNow = data.pop('studentValidNow', None)

    def serialize(self):
        return {
            'student': self.student,
            'studentIdentifier': self.studentIdentifier,
            'studentValidFrom': self.studentValidFrom,
            'studentValidTo': self.studentValidTo,
            'studentUpdated': self.studentUpdated,
            'senior' : self.senior,
            'seniorUpdated': self.seniorUpdated,
            'seniorIdentifier': self.seniorIdentifier,
            'disabilities': self.disabilities,
            'disabilitiesIdentifier': self.disabilitiesIdentifier,
            'disabilitiesUpdated': self.disabilitiesUpdated,
            'studentValidNow': self.studentValidNow
        }

class StrongIdentification(object):
    '''
    Wrapper for the user's strong identification info.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user's strong identification fields
        Dictionary keys:
            'method' (str) method used to strongly identify user. One of:
                           IN_PERSON, SUOMI_FI, SUOMI_FI_VALTUUDET, USER_API
            'identificationDocuments' (list) documents used during
                                             identification.
            'otherExplanation' (str) other explanation related to identification.
            'personalId' (str) user's personal ID. May be censored if viewer
                               doesn't have permission ACCOUNT_VIEW_PERSONAL_ID.
            'remarks' (str) remarks related to last strong identification event.
            'identifier' (str) user name, client ID, or other who performed last
                               identification.
            'time' (str) timestamp when user was strongly identified.
            'firstTime' (str) first time when user was strongly identified.
            'count' (int) number of times user has been strongly identified.
            'identified' (bool) has user been strongly identified.
        '''

        self.method = data.pop('method', None)
        self.identificationDocuments = data.pop('identificationDocuments', None)
        self.otherExplanation = data.pop('otherExplanation', None)
        self.personalId = data.pop('personalId', None)
        self.remarks = data.pop('remarks', None)
        self.identifier = data.pop('identifier', None)
        self.time = data.pop('time', None)
        self.firstTime = data.pop('firstTime', None)
        self.count = data.pop('count', None)
        self.identified = data.pop('identified', None)

    def serialize(self):
        return {
            'method': self.method,
            'identificationDocuments': self.identificationDocuments,
            'otherExplanation': self.otherExplanation,
            'personalId': self.personalId,
            'remarks': self.remarks,
            'identifier': self.identifier,
            'time': self.time,
            'firstTime': self.firstTime,
            'count': self.count,
            'identified': self.identified
        }

class PasswordUpdateResult(object):
    '''
    Wrapper for the user's password update result.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user's password update result fields
        Dictionary keys:
            'success' (bool)
            'validationErrors' (list) list of ValidationError objects
        '''

        self.validationErrors = []
        for v in data.pop('validationErrors', []):
            self.validationErrors.append(ValidationError(v))

        self.success = data.pop('success', None)

    def serialize(self):

        validationErrors = []
        for v in self.validationErrors:
            validationErrors.append(v.serialize())

        return {
            'success': self.success,
            'validationErrors' : validationErrors
        }

class PlaceOfBirth(object):
    '''
    Wrapper for the user’s place of birth.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user’s place of birth fields
        Dictionary keys:
            'country'
            'locality'
            'region'
        '''
        self.country = data.pop('country', None)
        self.locality = data.pop('locality', None)
        self.region = data.pop('region', None)

    def serialize(self):
        return {
            'country': self.country,
            'locality': self.locality,
            'region': self.region
        }

class ValidationError(object):
    '''
    Wrapper for the validation error.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): validation error
        Dictionary keys:
            'message' (str)
            'code' (str) validation error code
        '''
        self.message = data.pop('message', None)
        self.code = data.pop('code', None)

    def serialize(self):
        return {
            'message': self.message,
            'code' : self.code
        }

class NamespaceMigrationOptions(object):
    '''
    Wrapper for user namespase migrate options.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): namespace migrate options
        Dictionary keys:
            'targetNsCode' (str) Target namespace's code.
            'keepUserId' (bool) default: True. If true, same user ID will be
                                kept. If false, a new user ID is given. Some
                                internal references to original ID may be
                                deleted during migration even if the same ID
                                is kept.
            'keepProfile' (bool) default: True. If true: names, street
                                 addresses, legalinfo, customergroupinfo, DoB,
                                 and other profile data will be migrated.
            'keepEmails' (bool) default: True. If true, email addresses and
                                verification status will be migrated.
            'keepMobiles' (bool) default: True. If true, mobile numbers and
                                 verification status will be migrated.
            'keepConsents' (bool) default: True. If true, user consents will
                                  be migrated.
            'keepCustomFields' (bool) default: True. If true, custom fields
                                      will be migrated.
            'keepPassword' (bool) default: True. If true: password will be
                                  migrated unless new password is specified.
            'keepGroups' (bool) default: False. If true: user groups will be
                                migrated based on group names.
            'username' (str) Username after migration. If null, username is
                             autogenerated. Value must be unique in new
                             namespace.
            'userPassword' (str) Password for new migrated user.
        '''
        self.targetNsCode = data.pop('targetNsCode', None)
        self.keepUserId = data.pop('keepUserId', True)
        self.keepProfile = data.pop('keepProfile', True)
        self.keepEmails = data.pop('keepEmails', True)
        self.keepMobiles = data.pop('keepMobiles', True)
        self.keepConsents = data.pop('keepConsents', True)
        self.keepCustomFields = data.pop('keepCustomFields', True)
        self.keepPassword = data.pop('keepPassword', True)
        self.keepGroups = data.pop('keepGroups', False)
        self.username = data.pop('username', None)
        self.userPassword = data.pop('userPassword', None)

    def serialize(self):
        return {
            'targetNsCode': self.targetNsCode,
            'keepUserId' : self.keepUserId,
            'keepProfile' : self.keepProfile,
            'keepEmails' : self.keepEmails,
            'keepMobiles' : self.keepMobiles,
            'keepConsents' : self.keepConsents,
            'keepCustomFields' : self.keepCustomFields,
            'keepPassword' : self.keepPassword,
            'keepGroups' : self.keepGroups,
            'username' : self.username,
            'userPassword' : self.userPassword
        }

class LegalInfo(object):
    '''
    The LetalInfo class that represents user's legal information.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict): user legal info fields
        Dictionary keys:
            'firstNames' (str)
            'lastName' (str)
            'callingName' (str)
            'email' (str)
            'phone' (str)
            'domicile' (LegalDomicile)
            'personalIdentityCode' (str)
            'protectionOrder' (boolean)
            'dateOfBirth' (str)
            'dateOfDeath' (str)
            'addresses' (list of trivoreid.models.user.Address)
            'lastUpdatedAt' (str)
            'studentInfo' (StudentInfo)
        '''

        addresses = []
        for a in data.pop('addresses', []):
            addresses.append(Address(a))

        self.firstNames = data.pop('firstNames', None)
        self.lastName = data.pop('lastName', None)
        self.callingName = data.pop('callingName', None)
        self.email = data.pop('email', None)
        self.phone = data.pop('phone', None)
        self.domicile = LegalDomicile(data.pop('domicile', {}))
        self.personalIdentityCode = data.pop('personalIdentityCode', None)
        self.protectionOrder = data.pop('protectionOrder', None)
        self.dateOfBirth = data.pop('dateOfBirth', None)
        self.dateOfDeath = data.pop('dateOfDeath', None)
        self.addresses = addresses
        self.lastUpdatedAt = data.pop('lastUpdatedAt', None)
        self.studentInfo = 	StudentInfo(data.pop('studentInfo', {}))

    def serialize(self):
        addresses = []
        for a in self.addresses:
            addresses.append(a.serialize())

        return {
            'firstNames': self.firstNames,
            'lastName': self.lastName,
            'callingName': self.callingName,
            'email': self.email,
            'phone': self.phone,
            'domicile': self.domicile.serialize(),
            'addresses': addresses,
            'studentInfo': self.studentInfo.serialize(),
            'personalIdentityCode': self.personalIdentityCode,
            'protectionOrder': self.protectionOrder,
            'dateOfBirth': self.dateOfBirth,
            'dateOfDeath': self.dateOfDeath,
            'lastUpdatedAt': self.lastUpdatedAt
        }

class LegalDomicile(object):
    '''
    LegalDomicile class that represents user's legal domicile object.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): user legal domicile fields
        Dictionary keys:
            'names' (dict)
            'code' (str)
        '''

        self.names = data.pop('names', {})
        self.code = data.pop('code', None)

    def serialize(self):
        return {
            'names': self.names,
            'code': self.code
        }

class StudentInfo(object):
    '''
    StudentInfo class that represents user's student info.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): user student state fields
        Dictionary keys:
            'state' (StudentStatus)
            'studentValidFrom' (str)
            'studentValidTo' (str)
            'informationUpdated' (str)
            'remoteState' (str)
            'notStudentReason' (str)
            'queryConsentEnds' (str)
        '''

        self.state = data.pop('state', None)
        self.studentValidFrom = data.pop('studentValidFrom', None)
        self.studentValidTo = data.pop('studentValidTo', None)
        self.informationUpdated = data.pop('informationUpdated', None)
        self.remoteState = data.pop('remoteState', None)
        self.notStudentReason = data.pop('notStudentReason', None)
        self.queryConsentEnds = data.pop('queryConsentEnds', None)

    def serialize(self):
        return {
            'state': self.state,
            'studentValidFrom': self.studentValidFrom,
            'studentValidTo': self.studentValidTo,
            'informationUpdated': self.informationUpdated,
            'remoteState': self.remoteState,
            'notStudentReason': self.notStudentReason,
            'queryConsentEnds': self.queryConsentEnds
        }

class StudentState(object):
    '''
    StudentState class that represents user's student info.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict): user student state fields
        Dictionary keys:
            'state' (StudentStatus)
            'studentFrom' (str) Date when user becomes student
            'studentTo' (str) Date when user stops being a student.
            'updated' (str) Timestamp when student status was last updated.
            'lastQuerySuccess' (bool) True if last query from original source
                                      was successful. If false, the student
                                      information was not updated and may be
                                      stale. Client may use the previously known
                                      user information if it is not too old, or
                                      show an error message to the user if
                                      necessary, and try again later.
            'lastQueryError' (str) If lastQuerySuccess was false, this string
                                   contains the known error message. It may be
                                   useful for debugging.
            'source' (str) Database location where state was read from.
        '''

        self.state = data.pop('state', None)
        self.studentFrom = data.pop('studentFrom', None)
        self.studentTo = data.pop('studentTo', None)
        self.updated = data.pop('updated', None)
        self.lastQuerySuccess = data.pop('lastQuerySuccess', None)
        self.lastQueryError = data.pop('lastQueryError', None)
        self.source = data.pop('source', None)

    def serialize(self):
        return {
            'state': self.state,
            'studentFrom': self.studentFrom,
            'studentTo': self.studentTo,
            'updated': self.updated,
            'lastQuerySuccess': self.lastQuerySuccess,
            'lastQueryError': self.lastQueryError,
            'source': self.source
        }

class StudentStatus(object):
    '''
    Student statuses.
    '''
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    NOT_STUDENT = 'NOT_STUDENT'
    FORBIDDEN = 'FORBIDDEN'
    UNKNOWN = 'UNKNOWN'
