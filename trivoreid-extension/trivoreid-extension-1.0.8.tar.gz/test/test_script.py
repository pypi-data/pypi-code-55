#!/usr/bin/env python
# coding: utf-8

import json
import sys
import getopt
import logging
import time
import math

from importlib import reload

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


def main():
    '''
    Example of a command:
    python /path/to/test_script.py -p <path>

    path - optional parameter. If not defined, then the default
           /etc/trivoreid/client_sdk.properties will be used

    In the properties file there should be defined management API credentials.

    Example of the properties file:

        service.address=<placeholder>
        mgmtapi.id=<placeholder>
        mgmtapi.secret=<placeholder>

    '''

    reload(logging)
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

    opts, args = getopt.getopt(sys.argv[1:], 'p:')

    path = '/etc/trivoreid/client_sdk.properties'
    path = '/etc/trivoreid_tmp/client_sdk.properties'

    for key, value in opts:
        if key == '-p':
            path = value

    api = TrivoreID(path)

    initialTime = time.time()

    nsCode = 'testsdk004'

    try:
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

        user = api.user_service.create(User({
                    'nsCode' : nsCode
                }))
        userId = user.id

        api.user_service.report_strong_identification(userId,
                                                      'personalId',
                                                      'remarks')

        si = api.user_service.get_strong_identification(user.id)

        # assert si.personalId == 'personalId'
        # assert si.remarks == 'remarks'

        r = api.user_service.change_password(userId, 'a')
        assert not r.success

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

        user = api.user_service.get(userId)

        assert user.consents.serialize() == user_consents.serialize()
        assert user.emails[0].serialize() == user_emails[0].serialize()
        assert user.emails[1].serialize() == user_emails[1].serialize()
        assert user.mobiles[0].serialize() == user_mobiles[0].serialize()
        assert user.mobiles[1].serialize() == user_mobiles[1].serialize()
        assert user.addresses[0].serialize() == user_addresses[0].serialize()
        assert user.name.serialize() == user_names.serialize()

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

        assert api.user_service.verify_sms_code_check(userId, '1234') == False

        print('\n=================')
        print('| Group Service |')
        print('=================\n')

        filt = Filter(Filter.EQUAL, 'nsCode', nsCode)
        groups = api.group_service.get_all(filt).resources
        group_ids = user.memberOf

        new_group = Group({'name'       : 'gr003',
                          'description' : 'test description',
                          'nsCode'      : nsCode})

        g = api.group_service.create(new_group)

        new_group.name = 'gr004'
        api.group_service.update(new_group, g.id)

        g2 = api.group_service.get(g.id)

        groupId = g.id
        g2.id = None

        assert g2.description == 'test description'
        assert g2.name == 'gr004'

        print('\n========================')
        print('| Access Right Service |')
        print('========================\n')

        role = CustomRole()

        role.nsCode = nsCode
        role.name = 'EXAMPLE_ROLE'
        role.memberOf = [groupId]

        role.serialize()

        initialNum = api.access_right_service.get_all_custom_roles().totalResults

        role = api.access_right_service.create_custom_role(role)
        afterCreate = api.access_right_service.get_all_custom_roles().totalResults

        role = api.access_right_service.get_custom_role(role.id)
        assert role.name == 'EXAMPLE_ROLE'

        api.user_service.update_custom_roles(userId, add=[role.id])
        assert role.id in api.user_service.get_custom_roles(userId)

        api.user_service.update_custom_roles(userId, remove=[role.id])
        assert role.id not in api.user_service.get_custom_roles(userId)

        role.name = 'MODIFIED NAME'
        api.access_right_service.update_custom_role(role)
        role = api.access_right_service.get_custom_role(role.id)

        assert role.name == 'MODIFIED NAME'

        api.access_right_service.delete_custom_role(role.id)
        afterDelete = api.access_right_service.get_all_custom_roles().totalResults
        assert afterCreate == initialNum + 1
        assert afterDelete == initialNum

        api.group_service.delete(groupId)

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

        auth.validFrom=validFrom
        auth.validTo=validTo

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

        print('\n========================')
        print('| Subscription Service |')
        print('========================\n')

        page = api.subscription_service.get_all()
        initialNum = page.totalResults

        sub = Subscription()
        sub.subscriberId = userId

        sub = api.subscription_service.create(sub)
        subId = sub.id

        sub.customFields = {'key1' : 'value1', 'key2' : 'value2'}
        api.subscription_service.update(sub)

        sub = api.subscription_service.get(subId)

        page = api.subscription_service.get_all()

        assert page.totalResults == initialNum + 1
        assert sub.subscriberId == userId
        assert sub.customFields['key1'] == 'value1'
        assert sub.customFields['key2'] == 'value2'
        assert sub.active
        assert sub.terminated == None

        period = Period()

        period = api.subscription_service.create_period(subId, period)
        periodId = period.id

        period.externalId = 'test'
        period.customFields['key1'] = 'value1'
        period.customFields['key2'] = 'value2'

        api.subscription_service.update_period(subId, period)

        period = api.subscription_service.get_period(subId, periodId)

        assert period.externalId == 'test'
        assert period.customFields['key1'] == 'value1'
        assert period.customFields['key2'] == 'value2'

        filt = Filter(Filter.EQUAL, 'id', subId)
        page = api.subscription_service.get_all(filt)

        assert page.totalResults == 1

        sub = api.subscription_service.terminate(subId)

        assert not sub.active
        assert sub.terminated != None

        print('\n=========================')
        print('| Location/Site Service |')
        print('=========================\n')

        initialNum = api.locationsites_service.get_all().totalResults

        ls = LocationSite()
        ls.name = 'ExampleName'

        ls = api.locationsites_service.create(ls)
        afterCreate = api.locationsites_service.get_all().totalResults

        assert afterCreate == initialNum + 1
        assert ls.name == 'ExampleName'

        ls.description = 'Example Description'
        api.locationsites_service.update(ls)

        ls = api.locationsites_service.get(ls.id)

        assert ls.description == 'Example Description'

        api.locationsites_service.delete(ls.id)

        afterDelete = api.locationsites_service.get_all().totalResults
        assert afterDelete == initialNum

        print('\n==================')
        print('| Target Service |')
        print('==================\n')

        target = Target()
        target.name = 'ExampleName'

        initialNum = api.target_service.get_all().totalResults
        target = api.target_service.create(target)

        afterCreate = api.target_service.get_all().totalResults

        assert afterCreate == initialNum + 1
        assert target.name == 'ExampleName'

        target.name = 'ModifiedName'
        target = api.target_service.update(target)

        assert target.name == 'ModifiedName'

        api.target_service.delete(target.id)
        afterDelete = api.target_service.get_all().totalResults

        assert afterDelete == initialNum

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

        print('\n===================')
        print('| Contact Service |')
        print('===================\n')

        address = Address()
        address.country = 'FI'
        address.streetAddress = 'Street Address'

        contact = Contact()
        contact.addresses.append(address)
        initialNum = api.contact_service.get_all().totalResults

        contact = api.contact_service.create(contact)
        afterCreate = api.contact_service.get_all().totalResults

        contact.middleName = 'Middle Name'
        api.contact_service.update(contact)
        contact = api.contact_service.get(contact.id)

        enterprise = Enterprise()
        enterprise.vatId = 'vatId'

        api.contact_service.update_enterprise_info(contact.id, enterprise)
        enterprise = api.contact_service.get_enterprise_info(contact.id)

        api.contact_service.delete(contact.id)
        afterDelete = api.contact_service.get_all().totalResults

        assert afterCreate == initialNum + 1
        assert contact.addresses[0].streetAddress == 'Street Address'
        assert contact.addresses[0].country == 'FI'
        assert contact.middleName == 'Middle Name'
        assert enterprise.vatId == 'vatId'
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

        print('\n==================')
        print('| Wallet Service |')
        print('==================\n')

        ac = AccessControl()
        ac.title = 'TestMgmtApiWallet'
        ac.apiClientIdRead.append(api.client_id)
        ac.apiClientIdWrite.append(api.client_id)

        ac = api.accesscontrol_service.create(ac)

        initialNum = api.wallet_service.get_all().totalResults

        wallet = Wallet()
        wallet.ownerId = userId
        wallet.accessControlIds.append(ac.id)
        wallet.holderIds.append(api.client_id)
        wallet.name = 'Test'
        wallet.currency = 'EUR'

        wallet = api.wallet_service.create(wallet)

        assert api.wallet_service.get_all().totalResults == initialNum + 1
        assert wallet.name == 'Test'
        assert wallet.currency == 'EUR'

        wallet.name = 'Updated'

        api.wallet_service.update(wallet)
        wallet = api.wallet_service.get(wallet.id)

        assert wallet.name == 'Updated'

        api.wallet_service.delete(wallet.id)
        api.accesscontrol_service.delete(ac.id)

        assert api.wallet_service.get_all().totalResults == initialNum

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
