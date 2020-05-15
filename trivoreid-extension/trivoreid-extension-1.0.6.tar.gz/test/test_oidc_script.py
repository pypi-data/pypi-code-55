#!/usr/bin/env python
# coding: utf-8

import os
import json
import sys
import getopt
import logging
import time
import math

from importlib import reload
from requests_oauthlib import OAuth2Session

from trivoreid.client import TrivoreID
from trivoreid.exceptions import *

from trivoreid.models.authorisation import *
from trivoreid.models.groups import *
from trivoreid.models.datastorage import *
from trivoreid.models.user import *
from trivoreid.models.namespace import *
from trivoreid.models.email import *
from trivoreid.models.enterprise import *
from trivoreid.models.invite import *
from trivoreid.models.mydata import *
from trivoreid.models.pass_requirements import *
from trivoreid.models.paycard import *
from trivoreid.models.profile import *
from trivoreid.models.sms import *
from trivoreid.models.contract import *
from trivoreid.models.page import *
from trivoreid.models.subscription import *
from trivoreid.models.locationsite import *
from trivoreid.models.target import *
from trivoreid.models.accesscontrol import *
from trivoreid.models.contact import *
from trivoreid.models.access_right import *
from trivoreid.models.products import *
from trivoreid.models.wallet import *

from trivoreid.oidc.oidc_user import *
from trivoreid.oidc.oidc_client import *

from trivoreid.services.access_control_service import *
from trivoreid.services.access_right_service import *
from trivoreid.services.authorisation_service import *
from trivoreid.services.contact_service import *
from trivoreid.services.contract_service import *
from trivoreid.services.datastorage_service import *
from trivoreid.services.email_service import *
from trivoreid.services.group_service import *
from trivoreid.services.locationsites_service import *
from trivoreid.services.mydata_service import *
from trivoreid.services.namespace_service import *
from trivoreid.services.paycard_service import *
from trivoreid.services.product_service import *
from trivoreid.services.profile_service import *
from trivoreid.services.sms_service import *
from trivoreid.services.subscription_service import *
from trivoreid.services.target_service import *
from trivoreid.services.user_service import *
from trivoreid.services.wallet_service import *

from trivoreid.utils.criteria import *

SCOPE = [
    'address',
    'phone',
    'profile',
    'email',
    'https://oneportal.trivore.com/scope/address.update',
    'https://oneportal.trivore.com/scope/consent',
    'https://oneportal.trivore.com/scope/mydata.request',
    'https://oneportal.trivore.com/scope/paycards',
    'https://oneportal.trivore.com/scope/namespace',
    'https://oneportal.trivore.com/scope/contract.write',
    'https://oneportal.trivore.com/scope/authorisations.readonly',
    'https://oneportal.trivore.com/scope/user.custom.fields.readonly',
    'https://oneportal.trivore.com/scope/users.readonly',
    'https://oneportal.trivore.com/scope/profile.update',
    'https://oneportal.trivore.com/scope/groups.readonly',
    'https://oneportal.trivore.com/scope/datastorage.admin',
    'https://oneportal.trivore.com/scope/authorisations.sources.readonly',
    'https://oneportal.trivore.com/scope/datastorage',
    'https://oneportal.trivore.com/scope/paycards.number.readonly',
    'https://oneportal.trivore.com/scope/phone.update',
    'https://oneportal.trivore.com/scope/paycards.number',
    'https://oneportal.trivore.com/scope/accessrights',
    'https://oneportal.trivore.com/scope/password',
    'https://oneportal.trivore.com/scope/authorisations',
    'https://oneportal.trivore.com/scope/email.verify',
    'https://oneportal.trivore.com/scope/authorisations.sources',
    'https://oneportal.trivore.com/scope/groups',
    'https://oneportal.trivore.com/scope/authorisations.types.readonly',
    'https://oneportal.trivore.com/scope/consent.readonly',
    'https://oneportal.trivore.com/scope/user.invite',
    'https://oneportal.trivore.com/scope/contract.sign',
    'https://oneportal.trivore.com/scope/accessrights.readonly',
    'https://oneportal.trivore.com/scope/authorisation.grant.rights',
    'https://oneportal.trivore.com/scope/authorisations.types',
    'https://oneportal.trivore.com/scope/authorisation.grant.rights.readonly',
    'https://oneportal.trivore.com/scope/sms.verify',
    'https://oneportal.trivore.com/scope/mydata.download',
    'https://oneportal.trivore.com/scope/user.custom.fields',
    'https://oneportal.trivore.com/scope/contract.terminate',
    'https://oneportal.trivore.com/scope/namespace.readonly',
    'https://oneportal.trivore.com/scope/contract.read',
    'https://oneportal.trivore.com/scope/users',
    'https://oneportal.trivore.com/scope/accesscontrol',
    'https://oneportal.trivore.com/scope/user.tokens',
    'https://oneportal.trivore.com/scope/paycards.readonly',
    'https://oneportal.trivore.com/scope/user.tokens.readonly',
    'https://oneportal.trivore.com/scope/accesscontrol.readonly',
    'https://oneportal.trivore.com/scope/email.update',
    'https://oneportal.trivore.com/scope/datastorage.readonly',
    'https://oneportal.trivore.com/scope/products.catalog.read',
    'https://oneportal.trivore.com/scope/products.product.read',
    'https://oneportal.trivore.com/scope/products.pricingplan.read',
    'https://oneportal.trivore.com/scope/commerce.sales.products.query',
    'https://oneportal.trivore.com/scope/products.pricingplan.write',
    'https://oneportal.trivore.com/scope/products.product.write',
    'https://oneportal.trivore.com/scope/products.catalog.write',
    'https://oneportal.trivore.com/scope/commerce.wallet.read',
    'https://oneportal.trivore.com/scope/commerce.wallet.transfer',
    'https://oneportal.trivore.com/scope/commerce.wallet.write'
]

def main():
    '''
    Example of a command:
    python /path/to/test_oidc_script.py -p <path>

    path - optional parameter. If not defined, then the default
           /etc/trivoreid/client_sdk.properties will be used

    In the properties file there should be defined management API credentials.

    Example of the properties file:

        service.address=<placeholder>
        oidc.client.id=<placeholder>
        oidc.client.secret=<placeholder>
        oidc.client.redirect.uri=<placeholder>

    '''

    reload(logging)
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',level=logging.DEBUG, datefmt='%I:%M:%S')

    opts, args = getopt.getopt(sys.argv[1:], 'p:')

    path = '/etc/trivoreid/client_sdk.properties'

    for key, value in opts:
        if key == '-p':
            path = value

    nsCode = 'testsdk004'

    initialTime = 0

    oidc = OidcClient()

    properties = su.get_properties(path)
    client_id = properties.pop('oidc.client.id', None)
    client_secret = properties.pop('oidc.client.secret', None)
    redirect_uri = properties.pop('oidc.client.redirect.uri', None)
    server = properties.pop('service.address', None)

    oauth = OAuth2Session(client_id=client_id,
                          redirect_uri=redirect_uri,
                          scope=SCOPE)

    authorization_url, state = oauth.authorization_url(server + '/openid/auth')

    print('Please, go to this URI and authenticate:')
    print(authorization_url)
    print('\n')

    link = input('Then copy paste the redirected URI:')

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    token = oauth.fetch_token(oidc.token_endpoint,
                              authorization_response=link,
                              client_secret=client_secret)

    api = TrivoreID(oauth=oauth)

    try:
        initialTime = time.time()

        print('\n=====================')
        print('| Namespace Service |')
        print('=====================\n')

        ns = api.namespace_service.create(Namespace({
                    'code'           : nsCode,
                    'name'           : 'TestSDK004',
                    'shortName'      : 'TestSDK004',
                    'usernamePolicy' : UsernamePolicy.EMAIL
                }))

        filt = Filter(Filter.EQUAL, 'code', nsCode)
        ns = api.namespace_service.get_all(filt).resources[0]
        ns2 = api.namespace_service.get(nsCode)

        assert ns.usernamePolicy == UsernamePolicy.EMAIL

        ns.meta = Meta()
        ns2.meta = Meta()

        assert ns.serialize() == ns2.serialize()

        ns.usernamePolicy = UsernamePolicy.EIGHT_NUMBERS
        ns.commMethodMaxQty = 3
        ns.duplicateNicknamesAllowed = True
        ns.validTo = '2022-10-26T09:39:42.195Z'
        api.namespace_service.update(ns)
        ns = api.namespace_service.get(nsCode)

        assert ns.code == nsCode
        assert ns.name == 'TestSDK004'
        assert ns.shortName == 'TestSDK004'
        assert ns.commMethodMaxQty == 3
        assert ns.duplicateNicknamesAllowed
        assert ns.validTo == '2022-10-26T09:39:42.195Z'
        assert bool(ns.validFrom) # should not be empty
        assert ns.usernamePolicy == UsernamePolicy.EIGHT_NUMBERS

        print('\n================')
        print('| User Service |')
        print('================\n')

        user = api.user_service.create(User({'nsCode' : nsCode}))
        userId = user.id

        r = api.user_service.change_password(userId, 'a')
        assert not r.success

        user_groups = ['gr001', 'gr002']
        user_names = Names({
                'givenName' : 'First Name',
                'middleName' : 'Middle Name',
                'familyName' : 'Last Name'})

        user_addresses = [Address({
                'addressName' : 'address',
                'name' : 'home',
                'country' : 'FI',
                'locality' : 'fi',
                'postalCode' : '20750',
                'region' : 'Region',
                'streetAddress' : 'Street Address 5C'})]

        user_emails = [EmailAddress({'address' : 'example1@trivore.com'}),
                       EmailAddress({'address' : 'example2@trivore.com',
                                     'tags'    : ['tag1', 'tag2'],
                                     'name'    : 'work'})]

        user_mobiles = [Mobile({'number' : '+358401234567'}),
                        Mobile({'number' : '+358401234569',
                                 'tags' : ['tag1', 'tag2'],
                                 'name' : 'work'})]

        user_consents = Consents({'marketingEmail' : True})

        user.memberOf   = user_groups
        user.consents   = user_consents
        user.emails     = user_emails
        user.mobiles    = user_mobiles
        user.addresses  = user_addresses
        user.name       = user_names

        api.user_service.update(user)

        api.user_service.create(User({'nsCode' : nsCode}))
        filt = Filter(Filter.EQUAL, 'nsCode', nsCode)
        users = api.user_service.get_all(filt).resources

        assert len(users) == 2

        user2 = api.user_service.get(userId)

        assert user2.consents.serialize() == user_consents.serialize()
        assert user2.emails[0].serialize() == user_emails[0].serialize()
        assert user2.emails[1].serialize() == user_emails[1].serialize()
        assert user2.mobiles[0].serialize() == user_mobiles[0].serialize()
        assert user2.mobiles[1].serialize() == user_mobiles[1].serialize()
        assert user2.addresses[0].serialize() == user_addresses[0].serialize()
        assert user2.name.serialize() == user_names.serialize()
        assert len(user2.memberOf) == 2

        enterprise = Enterprise({'businessId' : 'testId'})

        api.user_service.update_enterprise(userId, enterprise)
        e = api.user_service.get_enterprise(userId)

        assert e.businessId == enterprise.businessId

        custom_fields = {'testKey' : 'test', 'testValue' : 'test2'}

        api.user_service.update_custom_fields(userId, custom_fields)
        cf = api.user_service.get_custom_fields(userId)

        api.user_service.delete_custom_fields(userId)
        cf2 = api.user_service.get_custom_fields(userId)

        assert json.loads(cf) == custom_fields
        assert json.loads(cf2) == {}

        pr = api.user_service.get_password_requirements(userId)

        print('\n==================')
        print('| Profile Service |')
        print('==================\n')

        p = api.profile_service.get()

        if len(p.emails) > 1:
            p.emails = [p.emails[0]]
        if len(p.mobiles) > 1:
            p.mobiles = [p.mobiles[0]]

        a = Address()
        a.country = 'FI'
        a.postalCode = 'test2'
        a.region = 'test3'

        e = ProfileEmail({'address' : 'example@trivore.com'})
        m = ProfileMobile({'number' : '+3584012345678'})

        p.addresses.append(a)
        p.emails.append(e)
        p.mobiles.append(m)

        api.profile_service.update(p)
        p = api.profile_service.get()

        containsEmail = False
        for email in p.emails:
            if e.serialize() == email.serialize():
                containsEmail = True
                p.emails.remove(email)
                break

        containsMobile = False
        for mobile in p.mobiles:
            if m.serialize() == mobile.serialize():
                containsMobile = True
                p.mobiles.remove(mobile)
                break

        containsAddress = False
        for addr in p.addresses:
            if a.serialize() == addr.serialize():
                containsAddress = True
                p.addresses.remove(addr)
                break

        assert containsEmail
        assert containsMobile
        assert containsAddress

        api.profile_service.update(p)

        print('\n=================')
        print('| Group Service |')
        print('=================\n')

        filt = Filter(Filter.EQUAL, 'nsCode', nsCode)
        groups = api.group_service.get_all(filt).resources
        group_ids = user.memberOf

        assert len(groups) == len(user_groups)

        new_group = Group({'name'       : 'gr003',
                          'description' : 'test description',
                          'nsCode'      : nsCode})
        g = api.group_service.create(new_group)

        new_group.name = 'gr004'
        api.group_service.update(new_group, g.id)

        g2 = api.group_service.get(g.id)

        g2.id = None

        assert g2.description == 'test description'
        assert g2.name == 'gr004'

        api.group_service.delete(g.id)

        print('\n========================')
        print('| Access Right Service |')
        print('========================\n')

        permissions = api.access_right_service.get_all_permissions()
        perm = api.access_right_service.get_permission(permissions[0].id)
        perms = [perm.id]

        api.user_service.update_custom_permissions(userId, add=perms)
        assert perms[0] in api.user_service.get_custom_permissions(userId)
        assert perms[0] in api.user_service.get_effective_permissions(userId)

        api.user_service.update_custom_permissions(userId, remove=perms)
        assert perms[0] not in api.user_service.get_custom_permissions(userId)

        builtin_roles = api.access_right_service.get_all_builtin_roles()
        role = builtin_roles[0]
        roles = [role.id]

        api.user_service.update_builtin_roles(userId, add=roles)
        assert roles[0] in api.user_service.get_builtin_roles(userId)

        api.user_service.update_builtin_roles(userId, remove=roles)
        assert roles[0] not in api.user_service.get_builtin_roles(userId)

        print('\n==================')
        print('| MyData Service |')
        print('==================\n')

        api.mydata_service.request(userId)
        api.mydata_service.get_package(userId)

        print('\n========================')
        print('| Data Storage Service |')
        print('========================\n')

        ds_name = 'testSDK'
        new_ds = DataStorage(storage_fields={'name' : ds_name},
                             data={'test' : 'test'})
        ds1 = api.datastorage_service.create(new_ds)
        api.datastorage_service.delete(ds1.id)

        new_ds = api.datastorage_service.create(DataStorage(
                                            storage_fields={'name' : ds_name}))

        filt = Filter(Filter.EQUAL, 'name', ds_name)
        dss = api.datastorage_service.get_all(filt).resources

        assert len(dss) >= 1

        ds = dss[0]

        test_data = {'key1' : 'value1', 'key2' : 'value2'}
        ds.data = test_data
        ds.description = 'test description'

        api.datastorage_service.update(ds)

        dsId = ds.id

        ds2 = api.datastorage_service.get(dsId)
        data = api.datastorage_service.get_data(dsId)

        assert test_data == json.loads(data)
        assert ds.description == ds2.description

        data = {'key1' : 'modified'}
        api.datastorage_service.update_data(dsId, data)
        api.datastorage_service.delete_value(dsId, 'key2')

        val1 = api.datastorage_service.get_value(dsId, 'key1')
        val2 = api.datastorage_service.get_value(dsId, 'key2')

        assert val1 == 'modified'
        assert val2 == None

        api.datastorage_service.delete(dsId)

        filt = Filter(Filter.EQUAL, 'id', dsId)
        dss = api.datastorage_service.get_all(filt).resources

        assert len(dss) == 0

        print('\n=========================')
        print('| Authorisation Service |')
        print('=========================\n')

        authType = api.authorization_service.get_all_types().resources[0]

        auth = Authorisation()
        auth.authType = authType.code
        auth.authSubject.type = 'User'
        auth.authObject.type = 'User'

        auth = api.authorization_service.create(auth)

        assert auth.authType == authType.code
        assert auth.authSubject.type == 'User'
        assert auth.authObject.type == 'User'

        fil = Filter(Filter.EQUAL, 'id', auth.id)
        page = api.authorization_service.get_all(fil)

        assert page.totalResults == 1

        validFrom = '2018-10-20T07:17:17.606Z'
        validTo = '2022-10-20T07:17:17.606Z'

        auth.validFrom = validFrom
        auth.validTo = validTo

        api.authorization_service.revoke(auth.id)
        auth = api.authorization_service.update(auth)

        auth = api.authorization_service.get(auth.id)

        assert auth.revoked == True
        assert auth.validFrom == validFrom
        assert auth.validTo == validTo

        api.authorization_service.delete(auth.id)

        page = api.authorization_service.get_all(fil)

        assert page.totalResults == 0

        typeCode = 'test'

        auth_type = AuthorisationType()
        auth_type.nsCode = nsCode
        auth_type.code = typeCode

        auth_type = api.authorization_service.create_type(auth_type)
        typeId = auth_type.id

        assert auth_type.nsCode == nsCode
        assert auth_type.code == typeCode

        auth_type.description = 'TEST'
        api.authorization_service.update_type(auth_type)
        auth_type = api.authorization_service.get_type(typeId)

        assert auth_type.description == 'TEST'

        filt = Filter(Filter.EQUAL, 'id', typeId)
        page = api.authorization_service.get_all_types(filt)

        assert page.totalResults == 1

        api.authorization_service.delete_type(typeId)
        page = api.authorization_service.get_all_types(filt)

        assert page.totalResults == 0

        auth_source = AuthorisationType()
        auth_source.nsCode=nsCode
        auth_source.code=typeCode

        auth_source = api.authorization_service.create_source(auth_source)
        sourceId = auth_type.id

        assert auth_type.nsCode == nsCode
        assert auth_type.code == typeCode

        auth_source.description = 'TEST'
        api.authorization_service.update_source(auth_source)
        auth_source = api.authorization_service.get_source(auth_source.id)

        assert auth_type.description == 'TEST'

        filt = Filter(Filter.EQUAL, 'id', auth_source.id)
        page = api.authorization_service.get_all_sources(filt)

        assert page.totalResults == 1

        api.authorization_service.delete_source(auth_source.id)
        page = api.authorization_service.get_all_sources(filt)

        assert page.totalResults == 0

        print('\n====================')
        print('| Contract Service |')
        print('====================\n')

        contracts = api.contract_service.get_all()

        initialNum = contracts.totalResults

        title = 'exampleTitle'
        notice_days = 2
        version = '1.0.0'
        validFrom = '2018-04-26T08:38:02.730Z'
        validTo = '2020-04-26T08:38:02.730Z'
        code = 'testcontract'
        scope = 'testScope'
        termsOfDelivery = 'testTerms'
        links = ['test1', 'test2']
        addendumFor = 'testAddendum'
        contractRefs = ['ref1', 'ref2']
        frameworkAgreementRef = 'testRef'
        notes = 'Test notes.'

        body_text = 'Test text.'
        externalFileRef = 'testRef'

        billingTerms = 'billingTerms'
        paymentTerms = 'paymentTerms'
        penaltyInterest = 'penaltyInterest'

        contract = Contract()

        contract.termOfNoticeDays = notice_days
        contract.terminationMode = TerminationMode.AFTER_ALL_PARTIES_TERMINATE
        contract.title = title
        contract.version = version
        contract.validFrom = validFrom
        contract.validTo = validTo
        contract.code = code
        contract.scope = scope
        contract.termsOfDelivery = termsOfDelivery
        contract.links = links
        contract.addendumFor = addendumFor
        contract.contractRefs = contractRefs
        contract.frameworkAgreementRef = frameworkAgreementRef
        contract.notes = notes

        contract.financialTerms.billingTerms = billingTerms
        contract.financialTerms.paymentTerms = paymentTerms
        contract.financialTerms.penaltyInterest = penaltyInterest

        contract = api.contract_service.create(contract)
        contractId = contract.id

        page = api.contract_service.get_all()

        assert page.totalResults == initialNum + 1

        filt = Filter(Filter.EQUAL, 'id', contractId)
        page = api.contract_service.get_all(filt)

        assert page.totalResults == 1

        assert contract.termOfNoticeDays == notice_days
        assert contract.terminationMode == TerminationMode.AFTER_ALL_PARTIES_TERMINATE
        assert contract.title == title
        assert contract.version == version
        assert contract.validFrom == validFrom
        assert contract.validTo == validTo
        assert contract.code == code
        assert contract.scope == scope
        assert contract.termsOfDelivery == termsOfDelivery
        assert contract.links == links
        assert contract.addendumFor == addendumFor
        assert contract.contractRefs == contractRefs
        assert contract.frameworkAgreementRef == frameworkAgreementRef
        assert contract.notes == notes

        assert contract.financialTerms.billingTerms == billingTerms
        assert contract.financialTerms.paymentTerms == paymentTerms
        assert contract.financialTerms.penaltyInterest == penaltyInterest

        modified = 'modified'

        contract.scope = modified
        contract.title = modified

        api.contract_service.update(contract)
        contract = api.contract_service.get(contractId)

        assert contract.scope == modified
        assert contract.title == modified

        b = bytearray('test',  'utf-8')

        api.contract_service.upload_body_file(contractId, b)
        result = api.contract_service.get_body_file(contractId)
        contract = api.contract_service.get(contractId)

        assert result == b
        assert contract.body.hasInternalFile

        api.contract_service.delete_body_file(contractId)
        contract = api.contract_service.get(contractId)

        assert not contract.body.hasInternalFile

        party = Party()

        party = api.contract_service.create_party(contractId, party)

        partyId = party.id

        name = 'testName'
        address = 'testAddress'
        mobile = 'testMobile'
        email = 'testEmail'

        party.name = name
        party.address = address
        party.mobile = mobile
        party.email = email

        api.contract_service.update_party(contractId, party)

        party = api.contract_service.get_party(contractId, partyId)

        assert party.name == name
        assert party.address == address
        assert party.mobile == mobile
        assert party.email == email

        parties = api.contract_service.get_all_parties(contractId)

        assert len(parties) == 1

        party.terminationMode = 'AFTER_SINGLE_SIGNER_TERMINATES'
        party.mobile = modified
        party = api.contract_service.update_party(contractId, party)

        assert party.terminationMode == 'AFTER_SINGLE_SIGNER_TERMINATES'
        assert party.mobile == modified

        for _ in range(3):
            signer = api.contract_service.create_party_signer(contractId, partyId, Signer())

        signerId = signer.id

        for _ in range(3):
            contact = api.contract_service.create_party_contact(contractId, partyId, PartyContact())
        contactId = contact.id

        party = api.contract_service.get_party(contractId, partyId)

        assert len(party.signers) == 3
        assert len(party.contacts) == 3

        signers = api.contract_service.get_all_party_signers(contractId, partyId)
        contacts = api.contract_service.get_all_party_contacts(contractId, partyId)

        assert len(signers) == 3
        assert len(contacts) == 3

        signer.name = name
        signer.address = address
        signer.mobile = mobile
        signer.email = email

        contact.name = name
        contact.address = address
        contact.mobile = mobile
        contact.email = email

        api.contract_service.update_party_signer(contractId, partyId, signer)
        api.contract_service.update_party_contact(contractId, partyId, contact)

        signer = api.contract_service.get_party_signer(contractId, partyId, signerId)
        contact = api.contract_service.get_party_contact(contractId, partyId, contactId)

        assert signer.name == name
        assert signer.address == address
        assert signer.mobile == mobile
        assert signer.email == email

        assert contact.name == name
        assert contact.address == address
        assert contact.mobile == mobile
        assert contact.email == email

        api.contract_service.delete_party_signer(contractId, partyId, signerId)
        api.contract_service.delete_party_contact(contractId, partyId, contactId)

        party = api.contract_service.get_party(contractId, partyId)

        assert len(party.signers) == 2
        assert len(party.contacts) == 2

        signers = api.contract_service.get_all_party_signers(contractId, partyId)
        contacts = api.contract_service.get_all_party_contacts(contractId, partyId)

        assert len(signers) == 2
        assert len(contacts) == 2

        appendix = Appendix()
        appendix.title = title

        appendix = api.contract_service.create_appendix(contractId, appendix)
        appendixId = appendix.id

        b = bytearray('test',  'utf-8')
        api.contract_service.upload_appendix_file(contractId, appendixId, b)

        result = api.contract_service.get_appendix_file(contractId, appendixId)
        appendix = api.contract_service.get_appendix(contractId, appendixId)

        assert appendix.hasInternalFile
        assert result == b

        api.contract_service.delete_appendix_file(contractId, appendixId)
        appendix = api.contract_service.get_appendix(contractId, appendixId)

        assert not appendix.hasInternalFile

        appendix.text = body_text

        api.contract_service.update_appendix(contractId, appendix)

        appendix = api.contract_service.get_appendix(contractId, appendixId)

        assert appendix.text == body_text
        assert appendix.title == title

        ids = [appendixId]
        for _ in range(3):
            ids.append(api.contract_service.create_appendix(contractId, Appendix()).id)
        ids_reversed = ids[::-1]

        api.contract_service.change_appendix_order(contractId, ids_reversed)
        appendices = api.contract_service.get_all_appendices(contractId)

        assert len(appendices) == 4

        for i in range(4):
            assert appendices[i].id == ids_reversed[i]

        api.contract_service.delete_appendix(contractId, appendixId)

        appendices = api.contract_service.get_all_appendices(contractId)

        assert len(appendices) == 3

        actions = api.contract_service.get_allowed_actions(contractId)

        api.contract_service.delete(contractId)
        page = api.contract_service.get_all()

        assert page.totalResults == initialNum

        filt = Filter(Filter.EQUAL, 'id', contractId)
        page = api.contract_service.get_all(filt)

        assert page.totalResults == 0

        print('\n==========================')
        print('| Access Control Service |')
        print('==========================\n')

        ac = AccessControl()

        initialNum = api.accesscontrol_service.get_all().totalResults
        ac = api.accesscontrol_service.create(ac)

        afterCreate = api.accesscontrol_service.get_all().totalResults

        assert afterCreate == initialNum + 1

        ac.description = 'Example description.'
        api.accesscontrol_service.update(ac)

        ac = api.accesscontrol_service.get(ac.id)

        assert ac.description == 'Example description.'

        api.accesscontrol_service.delete(ac.id)
        afterDelete = api.accesscontrol_service.get_all().totalResults

        assert afterDelete == initialNum

        print('\n====================')
        print('| Products Service |')
        print('====================\n')

        p1 = api.product_service.get_all_catalogs()
        initialNum1 = p1.totalResults

        p2 = api.product_service.get_all_products()
        initialNum2 = p2.totalResults

        p3 = api.product_service.get_all_pricing_plans()
        initialNum3 = p3.totalResults

        p4 = api.product_service.get_all_catalogs_and_items()
        initialNum4 = len(p4.catalogs)

        testDate = '2019-12-01T00:00:00Z'
        testDate2 = '2022-12-01T00:00:00Z'

        planToCreate = PricingPlan()

        planToCreate.title = 'Test'
        planToCreate.description = 'Test'
        planToCreate.publishDate = testDate
        planToCreate.customFields['key1'] = 'value1'
        planToCreate.customFields['key2'] = 2
        planToCreate.unpublishDate = testDate2

        plan = api.product_service.create_pricing_plan(planToCreate)

        codeDiscounts = CodeDiscount()

        codeDiscounts.title = 'Test'
        codeDiscounts.discountPercentage = 10.0
        codeDiscounts.code = 'test'

        volumeDiscounts = VolumeDiscount()

        volumeDiscounts.title = 'Test'
        volumeDiscounts.rangeStart = 5.0
        volumeDiscounts.rangeEnd = 10.0
        volumeDiscounts.discountPercentage = 5.0

        customerSegmentDiscounts = CustomerSegmentDiscount()

        customerSegmentDiscounts.title = 'Test'
        customerSegmentDiscounts.customerSegment = 'test'
        customerSegmentDiscounts.discountAmount = 5

        paymentMethodDiscounts = PaymentMethodDiscount()

        paymentMethodDiscounts.title = 'Test'
        paymentMethodDiscounts.discountAmountPerItem = 1
        paymentMethodDiscounts.paymentMethod = 'card'

        variableDiscounts = VariableDiscount()

        variableDiscounts.title = 'Test'
        variableDiscounts.discountPercentageEval = 'test'
        variableDiscounts.discountAmountEval = 'test'
        variableDiscounts.discountAmountPerItemEval = 'test'

        pricing = Pricing()

        pricing.codeDiscounts.append(codeDiscounts)
        pricing.volumeDiscounts.append(volumeDiscounts)
        pricing.customerSegmentDiscounts.append(customerSegmentDiscounts)
        pricing.paymentMethodDiscounts.append(paymentMethodDiscounts)
        pricing.variableDiscounts.append(variableDiscounts)

        plan.pricings.append(pricing)

        api.product_service.update_pricing_plan(plan)

        plan = api.product_service.get_pricing_plan(plan.id)

        assert plan.title == planToCreate.title
        assert plan.description == planToCreate.description
        assert plan.publishDate == planToCreate.publishDate
        assert plan.customFields == planToCreate.customFields
        assert plan.unpublishDate == planToCreate.unpublishDate

        assert plan.pricings[0].codeDiscounts[0].serialize() == pricing.codeDiscounts[0].serialize()
        assert plan.pricings[0].volumeDiscounts[0].serialize() == pricing.volumeDiscounts[0].serialize()
        assert plan.pricings[0].customerSegmentDiscounts[0].serialize() == pricing.customerSegmentDiscounts[0].serialize()
        assert plan.pricings[0].paymentMethodDiscounts[0].serialize() == pricing.paymentMethodDiscounts[0].serialize()
        assert plan.pricings[0].variableDiscounts[0].serialize() == pricing.variableDiscounts[0].serialize()

        productToCreate = Product()

        productToCreate.serialize()

        valid = Validity()
        valid.title = 'Test'

        productToCreate.pricingPlans.append(plan.id)
        productToCreate.validityLength = 100000
        productToCreate.sellable.append(valid)

        valid.daysOfWeek.append('SUNDAY')
        productToCreate.usable.append(valid)

        product = api.product_service.create_product(productToCreate)

        product.serialize()

        product.sku = 'test'
        descr = LocalisedDescription()
        descr.locale = 'fi'
        descr.name = 'Test'

        product.translations.append(descr)

        api.product_service.update_product(product)
        product = api.product_service.get_product(product.id)

        assert product.sku == 'test'
        assert product.translations[0].locale == 'fi'
        assert product.translations[0].name == 'Test'
        assert product.pricingPlans[0] == plan.id
        assert product.sellable[0].title == product.usable[0].title == valid.title
        assert product.usable[0].daysOfWeek == valid.daysOfWeek

        catalogToCreate = Catalog()

        catalogToCreate.name = 'Test'

        catalog = api.product_service.create_catalog(catalogToCreate)

        item = CatalogItem()

        item.productId = product.id
        item.productValuesInherited = True

        item.serialize()

        catalog.products.append(item)

        catalog.customFields['key1'] = 'value1'
        catalog.customFields['key2'] = 2

        api.product_service.update_catalog(catalog)

        catalog = api.product_service.get_catalog(catalog.id)

        assert catalog.name == catalogToCreate.name
        assert catalog.products[0].productId == item.productId
        assert catalog.products[0].productValuesInherited == item.productValuesInherited
        assert catalog.products[0].productSku == product.sku
        assert catalog.customFields['key1'] == 'value1'
        assert catalog.customFields['key2'] == 2

        assert api.product_service.get_all_catalogs().totalResults == initialNum1 + 1
        assert api.product_service.get_all_products().totalResults == initialNum2 + 1
        assert api.product_service.get_all_pricing_plans().totalResults == initialNum3 + 1

        all_catalogs = api.product_service.get_all_catalogs_and_items()
        cat = None
        for c in all_catalogs.catalogs:
            if len(c.products) > 0:
                cat = c
                break
        if len(all_catalogs.catalogs) > 0 and cat == None:
            cat = all_catalogs.catalogs[0]

        if cat != None:
            details = api.product_service.get_catalog_details(cat.catalogId)
            assert details != None
            if len(details.products) > 0:
                details2 = api.product_service.get_product_details(cat.catalogId, details.products[0].productId)
                assert details2 != None

        assert len(all_catalogs.catalogs) == initialNum4 + 1

        api.product_service.delete_catalog(catalog.id)
        api.product_service.delete_product(product.id)
        api.product_service.delete_pricing_plan(plan.id)

        assert api.product_service.get_all_catalogs().totalResults == initialNum1
        assert api.product_service.get_all_products().totalResults == initialNum2
        assert api.product_service.get_all_pricing_plans().totalResults == initialNum3
        assert len(api.product_service.get_all_catalogs_and_items().catalogs) == initialNum4

        # print('\n==================')
        # print('| Wallet Service |')
        # print('==================\n')
        #
        # ac = AccessControl()
        # ac.title = 'TestMgmtApiWallet'
        # ac.userIdRead.append(api.oidc_user.id)
        # ac.userIdWrite.append(api.oidc_user.id)
        #
        # ac = api.accesscontrol_service.create(ac)
        #
        # initialNum = api.wallet_service.get_all().totalResults
        #
        # wallet = Wallet()
        # wallet.ownerId = userId
        # wallet.accessControlIds.append(ac.id)
        # wallet.holderIds.append(api.oidc_user.id)
        # wallet.name = 'Test'
        # wallet.currency = 'EUR'
        #
        # wallet = api.wallet_service.create(wallet)
        #
        # assert api.wallet_service.get_all().totalResults == initialNum + 1
        # assert wallet.name == 'Test'
        # assert wallet.currency == 'EUR'
        #
        # wallet.name = 'Updated'
        #
        # api.wallet_service.update(wallet)
        # wallet = api.wallet_service.get(wallet.id)
        #
        # assert wallet.name == 'Updated'
        #
        # api.wallet_service.delete(wallet.id)
        # api.accesscontrol_service.delete(ac.id)
        #
        # assert api.wallet_service.get_all().totalResults == initialNum

        print('\nSucccessfully finished TrivoreID SDK test\n')

    finally:
        print('\nDeleting namespace and users.')
        filt = Filter(Filter.EQUAL, 'nsCode', nsCode)
        users_to_delete = api.user_service.get_all(filt).resources
        for u in users_to_delete:
            api.user_service.delete(u.id)

        api.namespace_service.delete(nsCode)
        print('\n')

        seconds = int(time.time() - initialTime)
        minutes = math.floor(seconds / 60)
        print('Test took {} minutes and {} seconds'.format(minutes, seconds))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
