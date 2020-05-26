#!/usr/bin/env python
# coding: utf-8

class Catalog(object):
    '''
    Wrapper for the Catalog.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : catalog fields
        Dictionary keys:
            'id' (str)
            'ownerId' (str)
            'accessControlIds' (list)
            'name' (str)
            'products' (list) list of CatalogItem objects
            'customFields' (dict)
        '''
        self.products = []
        for item in data.pop('products', []):
            self.products.append(CatalogItem(item))

        self.id = data.pop('id', None)
        self.ownerId = data.pop('ownerId', None)
        self.accessControlIds = data.pop('id', [])
        self.name = data.pop('name', None)
        self.customFields = data.pop('customFields', {})

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        products = []
        for item in self.products:
            products.append(item.serialize())

        return {
            'id'                : self.id,
            'ownerId'           : self.ownerId,
            'accessControlIds'  : self.accessControlIds,
            'name'              : self.name,
            'products'          : products,
            'customFields'      : self.customFields
            }

class CatalogItem(object):
    '''
    Wrapper for the Catalog Item.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : catalog item fields
        Dictionary keys:
            'id' (str) Unique ID of catalog item.
            'productId' (str) Reference to a Product ID.
            'productSku' (str) Product SKU. ReadOnly.
            'productValuesInherited' (boolean) True: Empty or null fields values
                                               are replaced with values from
                                               original product
            'customFields' (dict) Extra key-value attributes.
            'translations' (list) list of LocalisedDescription objects.
            'sellable' (list) List of Validity objects. Times when sellable. If
                              null or empty, base product sellable value is
                              used.
            'usable' (list) List of Validity objects. times when usable. If null
                            or empty, base product usable value is used.
            'pricingPlans' (list) pricing plan ID values. If null or empty,
                                  base product value is used.
            'validityLength' (int) product validity time length, in seconds.
                                   Time start depends on validityStartFrom.
            'validityStartFrom' (str) product validity start from option.
                                      See ValidityStartFrom for help
        '''
        self.sellable = []
        for validity in data.pop('sellable', []):
            self.sellable.append(Validity(validity))

        self.usable = []
        for validity in data.pop('usable', []):
            self.usable.append(Validity(validity))

        self.translations = []
        for translation in data.pop('translations', []):
            self.translations.append(LocalisedDescription(translation))

        self.id = data.pop('id', None)
        self.productId = data.pop('productId', None)
        self.productSku = data.pop('productSku', None)
        self.productValuesInherited = data.pop('productValuesInherited', None)
        self.customFields = data.pop('customFields', {})
        self.pricingPlans = data.pop('pricingPlans', [])
        self.validityLength = data.pop('validityLength', None)
        self.validityStartFrom = data.pop('validityStartFrom', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        sellable = []
        for validity in self.sellable:
            sellable.append(validity.serialize())

        usable = []
        for validity in self.usable:
            usable.append(validity.serialize())

        translations = []
        for translation in self.translations:
            translations.append(translation.serialize())

        return {
            'id'                        : self.id,
            'productId'                 : self.productId,
            'productSku'                : self.productSku,
            'productValuesInherited'    : self.productValuesInherited,
            'customFields'              : self.customFields,
            'pricingPlans'              : self.pricingPlans,
            'validityLength'            : self.validityLength,
            'validityStartFrom'         : self.validityStartFrom,
            'sellable'                  : sellable,
            'usable'                    : usable,
            'translations'              : translations
            }

class ValidityStartFrom(object):
    '''
    Validity start from.
    '''
    PURCHASE = 'PURCHASE'
    FIRST_USE = 'FIRST_USE'

class LocalisedDescription(object):
    '''
    Product name and description.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : localised description fields
        Dictionary keys:
            locale (str) ex. 'fi' or 'fi_FI'
            name (str) Product name
            shortName (str) Short product name
            description (str) Product description
        '''
        self.locale = data.pop('locale', None)
        self.name = data.pop('name', None)
        self.shortName = data.pop('shortName', None)
        self.description = data.pop('description', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
        'locale'        : self.locale,
        'name'          : self.name,
        'shortName'     : self.shortName,
        'description'   : self.description
        }

class Validity(object):
    '''
    Wrapper for the Validity.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : validity fields
        Dictionary keys:
            'title' (str) short title for this validity configuration.
            'validFrom' (str) valid starting from this datetime.
            'validUntil' (str) valid until this datetime.
            'daysOfWeek' (list) if set, is valid only on these days.
                                see DaysOfWeek for help.
            'timeOfDayFrom' (str) If set, is valid only if time of day is
                                  at least this. example: 16:10:31.938
            'timeOfDayUntil' (str) If set, is valid only if time of day is
                                   before this. example: 16:10:31.938
            'zoneId' (str) time zone for daysOfWeek check.
            'exceptions' (list) exceptions to validity. If any exception is
                                currently valid, this is not valid.
            'validNow' (bool) ReadOnly
        '''
        self.title = data.pop('title', None)
        self.validFrom = data.pop('validFrom', None)
        self.validUntil = data.pop('validUntil', None)
        self.daysOfWeek = data.pop('daysOfWeek', [])
        self.zoneId = data.pop('zoneId', None)
        self.exceptions = data.pop('exceptions', [])
        self.validNow = data.pop('validNow', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title'             : self.title,
            'validFrom'         : self.validFrom,
            'validUntil'        : self.validUntil,
            'daysOfWeek'        : self.daysOfWeek,
            'timeOfDayFrom'     : self.exceptions,
            'timeOfDayUntil'    : self.exceptions,
            'zoneId'            : self.zoneId,
            'exceptions'        : self.exceptions,
            'validNow'          : self.validNow
            }

class DaysOfWeek(object):
    '''
    Days of the week.
    '''
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'

class PricingPlan(object):
    '''
    Wrapper for the Pricing Plan.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : pricing plan fields
        Dictionary keys:
            'id' (str)
            'ownerId' (str)
            'accessControlIds' (list) list with access control IDs
            'pricings' (list) list of Pricing objects
            'customFields' (dict)
            'enabled' (bool)
            'title' (str)
            'description' (str)
            'availability' (list) list of Validity objects
            'publishDate' (str)
            'unpublishDate' (str)
        '''
        self.pricings = []
        for pricing in data.pop('pricings', []):
            self.pricings.append(Pricing(pricing))

        self.availability = []
        for a in data.pop('availability', []):
            self.availability.append(Validity(a))

        self.id = data.pop('id', None)
        self.ownerId = data.pop('ownerId', None)
        self.accessControlIds = data.pop('id', [])
        self.customFields = data.pop('customFields', {})
        self.enabled = data.pop('enabled', None)
        self.title = data.pop('title', None)
        self.description = data.pop('description', None)
        self.publishDate = data.pop('publishDate', None)
        self.unpublishDate = data.pop('unpublishDate', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        pricings = []
        for pricing in self.pricings:
            pricings.append(pricing.serialize())

        availability = []
        for a in self.availability:
            availability.append(pricing.serialize())

        return {
            'id'                : self.id,
            'ownerId'           : self.ownerId,
            'accessControlIds'  : self.accessControlIds,
            'customFields'      : self.customFields,
            'pricings'          : pricings,
            'availability'      : availability,
            'enabled'           : self.enabled,
            'title'             : self.title,
            'description'       : self.description,
            'publishDate'       : self.publishDate,
            'unpublishDate'     : self.unpublishDate
            }

class Pricing(object):
    '''
    Wrapper for the Pricing.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : pricing fields
        Dictionary keys:
            'enabled' (bool)
            'title' (str)
            'description' (str)
            'price' (double)
            'currency' (str) ISO 4217 currency code. example: EUR
            'vatIncluded' (bool)
            'vatPercent' (double)
            'codeDiscounts' (list) list of CodeDiscount
            'volumeDiscounts' (list) list of VolumeDiscount
            'customerSegmentDiscounts' (list) list of CustomerSegmentDiscount
            'paymentMethodDiscounts' (list) list of PaymentMethodDiscount
            'variableDiscounts' (list) list of VariableDiscount
            'codeDiscountStacking' (bool)
            'volumeDiscountStacking' (bool)
            'customerSegmentDiscountStacking' (bool)
            'variableDiscountStacking' (bool)
        '''
        self.codeDiscounts = []
        for d in data.pop('codeDiscounts', []):
            self.codeDiscounts.append(CodeDiscount(d))

        self.volumeDiscounts = []
        for d in data.pop('volumeDiscounts', []):
            self.volumeDiscounts.append(VolumeDiscount(d))

        self.customerSegmentDiscounts = []
        for d in data.pop('customerSegmentDiscounts', []):
            self.customerSegmentDiscounts.append(CustomerSegmentDiscount(d))

        self.paymentMethodDiscounts = []
        for d in data.pop('paymentMethodDiscounts', []):
            self.paymentMethodDiscounts.append(PaymentMethodDiscount(d))

        self.variableDiscounts = []
        for d in data.pop('variableDiscounts', []):
            self.variableDiscounts.append(VariableDiscount(d))

        self.enabled = data.pop('enabled', None)
        self.title = data.pop('title', None)
        self.description = data.pop('description', None)
        self.price = data.pop('price', None)
        self.currency = data.pop('currency', None)
        self.vatIncluded = data.pop('vatIncluded', None)
        self.vatPercent = data.pop('vatPercent', None)
        self.codeDiscountStacking = data.pop('codeDiscountStacking', None)
        self.volumeDiscountStacking = data.pop('volumeDiscountStacking', None)
        self.customerSegmentDiscountStacking = data.pop(
                                        'customerSegmentDiscountStacking', None)
        self.variableDiscountStacking = data.pop(
                                        'variableDiscountStacking', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        codeDiscounts = []
        for d in self.codeDiscounts:
            codeDiscounts.append(d.serialize())

        volumeDiscounts = []
        for d in self.volumeDiscounts:
            volumeDiscounts.append(d.serialize())

        customerSegmentDiscounts = []
        for d in self.customerSegmentDiscounts:
            customerSegmentDiscounts.append(d.serialize())

        paymentMethodDiscounts = []
        for d in self.paymentMethodDiscounts:
            paymentMethodDiscounts.append(d.serialize())

        variableDiscounts = []
        for d in self.variableDiscounts:
            variableDiscounts.append(d.serialize())

        return {
            'enabled' : self.enabled,
            'title' : self.title,
            'description' : self.description,
            'price' : self.price,
            'currency' : self.currency,
            'vatIncluded' : self.vatIncluded,
            'vatPercent' : self.vatPercent,
            'codeDiscountStacking' : self.codeDiscountStacking,
            'volumeDiscountStacking' : self.volumeDiscountStacking,
            'customerSegmentDiscountStacking' : self.customerSegmentDiscountStacking,
            'variableDiscountStacking' : self.variableDiscountStacking,
            'codeDiscounts' : codeDiscounts,
            'volumeDiscounts' : volumeDiscounts,
            'customerSegmentDiscounts' : customerSegmentDiscounts,
            'paymentMethodDiscounts' : paymentMethodDiscounts,
            'variableDiscounts' : variableDiscounts
            }

class CodeDiscount(object):
    '''
    Wrapper for the Code Discount.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : code discount fields
        Dictionary keys:
            'title' (str)
            'discountPercentage' (double)
            'discountAmount' (double)
            'discountAmountPerItem' (double)
            'limitedToApiClients' (list)
            'limitedToUsers' (list)
            'limitedToUserGroups' (list)
            'code' (str)
        '''
        self.title = data.pop('title', None)
        self.discountPercentage = data.pop('discountPercentage', None)
        self.discountAmount = data.pop('discountAmount', None)
        self.discountAmountPerItem = data.pop('discountAmountPerItem', None)
        self.limitedToApiClients = data.pop('limitedToApiClients', [])
        self.limitedToUsers = data.pop('limitedToUsers', [])
        self.limitedToUserGroups = data.pop('limitedToUserGroups', [])
        self.code = data.pop('code', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title' : self.title,
            'discountPercentage' : self.discountPercentage,
            'discountAmount' : self.discountAmount,
            'discountAmountPerItem' : self.discountAmountPerItem,
            'limitedToApiClients' : self.limitedToApiClients,
            'limitedToUsers' : self.limitedToUsers,
            'limitedToUserGroups' : self.limitedToUserGroups,
            'code' : self.code
            }

class VolumeDiscount(object):
    '''
    Wrapper for the Volume Discount.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : volume discount fields
        Dictionary keys:
            'title' (str)
            'discountPercentage' (double)
            'discountAmount' (double)
            'discountAmountPerItem' (double)
            'limitedToApiClients' (list)
            'limitedToUsers' (list)
            'limitedToUserGroups' (list)
            'rangeStart' (int)
            'rangeEnd' (int)
        '''
        self.title = data.pop('title', None)
        self.discountPercentage = data.pop('discountPercentage', None)
        self.discountAmount = data.pop('discountAmount', None)
        self.discountAmountPerItem = data.pop('discountAmountPerItem', None)
        self.limitedToApiClients = data.pop('limitedToApiClients', [])
        self.limitedToUsers = data.pop('limitedToUsers', [])
        self.limitedToUserGroups = data.pop('limitedToUserGroups', [])
        self.rangeStart = data.pop('rangeStart', None)
        self.rangeEnd = data.pop('rangeEnd', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title' : self.title,
            'discountPercentage' : self.discountPercentage,
            'discountAmount' : self.discountAmount,
            'discountAmountPerItem' : self.discountAmountPerItem,
            'limitedToApiClients' : self.limitedToApiClients,
            'limitedToUsers' : self.limitedToUsers,
            'limitedToUserGroups' : self.limitedToUserGroups,
            'rangeStart' : self.rangeStart,
            'rangeEnd' : self.rangeEnd
            }

class CustomerSegmentDiscount(object):
    '''
    Wrapper for the Customer Segment Discount.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : customer segment discount fields
        Dictionary keys:
            'title' (str)
            'discountPercentage' (double)
            'discountAmount' (double)
            'discountAmountPerItem' (double)
            'limitedToApiClients' (list)
            'limitedToUsers' (list)
            'limitedToUserGroups' (list)
            'customerSegment' (str)
        '''
        self.title = data.pop('title', None)
        self.discountPercentage = data.pop('discountPercentage', None)
        self.discountAmount = data.pop('discountAmount', None)
        self.discountAmountPerItem = data.pop('discountAmountPerItem', None)
        self.limitedToApiClients = data.pop('limitedToApiClients', [])
        self.limitedToUsers = data.pop('limitedToUsers', [])
        self.limitedToUserGroups = data.pop('limitedToUserGroups', [])
        self.customerSegment = data.pop('customerSegment', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title' : self.title,
            'discountPercentage' : self.discountPercentage,
            'discountAmount' : self.discountAmount,
            'discountAmountPerItem' : self.discountAmountPerItem,
            'limitedToApiClients' : self.limitedToApiClients,
            'limitedToUsers' : self.limitedToUsers,
            'limitedToUserGroups' : self.limitedToUserGroups,
            'customerSegment' : self.customerSegment
            }

class PaymentMethodDiscount(object):
    '''
    Wrapper for the Payment Method Discount.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : payment method discount fields
        Dictionary keys:
            'title' (str)
            'discountPercentage' (double)
            'discountAmount' (double)
            'discountAmountPerItem' (double)
            'limitedToApiClients' (list)
            'limitedToUsers' (list)
            'limitedToUserGroups' (list)
            'paymentMethod' (str)
        '''
        self.title = data.pop('title', None)
        self.discountPercentage = data.pop('discountPercentage', None)
        self.discountAmount = data.pop('discountAmount', None)
        self.discountAmountPerItem = data.pop('discountAmountPerItem', None)
        self.limitedToApiClients = data.pop('limitedToApiClients', [])
        self.limitedToUsers = data.pop('limitedToUsers', [])
        self.limitedToUserGroups = data.pop('limitedToUserGroups', [])
        self.paymentMethod = data.pop('paymentMethod', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title' : self.title,
            'discountPercentage' : self.discountPercentage,
            'discountAmount' : self.discountAmount,
            'discountAmountPerItem' : self.discountAmountPerItem,
            'limitedToApiClients' : self.limitedToApiClients,
            'limitedToUsers' : self.limitedToUsers,
            'limitedToUserGroups' : self.limitedToUserGroups,
            'paymentMethod' : self.paymentMethod
            }

class VariableDiscount(object):
    '''
    Wrapper for the Variable Discount.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : variable discount fields
        Dictionary keys:
            'title' (str)
            'discountPercentageEval' (str)
            'discountAmountEval' (str)
            'discountAmountPerItemEval' (str)
        '''
        self.title = data.pop('title', None)
        self.discountPercentageEval = data.pop('discountPercentageEval', None)
        self.discountAmountEval = data.pop('discountAmountEval', None)
        self.discountAmountPerItemEval = data.pop(
                                            'discountAmountPerItemEval', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title' : self.title,
            'discountPercentageEval' : self.discountPercentageEval,
            'discountAmountEval' : self.discountAmountEval,
            'discountAmountPerItemEval' : self.discountAmountPerItemEval
            }

class Product(object):
    '''
    Wrapper for the Product.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : product fields
        Dictionary keys:
            'id' (str) Entity ID.
            'ownerId' (str) Owner User ID.
            'accessControlIds' (list)
            'sku' (str) External product/service identifier.
            'translations' (list) list of LocalisedDescription objects.
            'customFields' (dict)
            'sellable' (list) list of Validity. Times when sellable. If null
                              or empty, base product sellable value is used.
            'usable' (list) list of Validity. Times when usable.
            'pricingPlans' (list) pricing plan ID values.
            'validityLength' (int) product validity time length, in seconds.
                                   Time start depends on validityStartFrom.
            'validityStartFrom' (str) product validity start from option.
                                      Check ValidityStartFrom for values.
        '''
        self.sellable = []
        for validity in data.pop('sellable', []):
            self.sellable.append(Validity(validity))

        self.usable = []
        for validity in data.pop('usable', []):
            self.usable.append(Validity(validity))

        self.translations = []
        for translation in data.pop('translations', []):
            self.translations.append(LocalisedDescription(translation))

        self.id = data.pop('id', None)
        self.ownerId = data.pop('ownerId', None)
        self.accessControlIds = data.pop('id', [])
        self.productId = data.pop('productId', None)
        self.sku = data.pop('sku', None)
        self.descriptions = data.pop('descriptions', {})
        self.customFields = data.pop('customFields', {})
        self.pricingPlans = data.pop('pricingPlans', [])
        self.validityLength = data.pop('validityLength', None)
        self.validityStartFrom = data.pop('validityStartFrom', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        sellable = []
        for validity in self.sellable:
            sellable.append(validity.serialize())

        usable = []
        for validity in self.usable:
            usable.append(validity.serialize())

        translations = []
        for translation in self.translations:
            translations.append(translation.serialize())

        return {
            'id'                        : self.id,
            'ownerId'                   : self.ownerId,
            'accessControlIds'          : self.accessControlIds,
            'sku'                       : self.sku,
            'descriptions'              : self.descriptions,
            'customFields'              : self.customFields,
            'pricingPlans'              : self.pricingPlans,
            'validityLength'            : self.validityLength,
            'validityStartFrom'         : self.validityStartFrom,
            'sellable'                  : sellable,
            'usable'                    : usable,
            'translations'              : translations
            }

class AllCatalogs(object):
    '''
    Wrapper for all accessible catalogs and their product item details.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : all accessible catalogs fields
        Dictionary keys:
            catalogs (list) list with CatalogDetails objects
        '''
        self.catalogs = []
        for catalog in data.pop('catalogs', []):
            self.catalogs.append(CatalogDetails(catalog))

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        catalogs = []
        for catalog in self.catalogs:
            catalogs.append(catalog.serialize())

        return {
            'catalogs' : catalogs
            }

class CatalogDetails(object):
    '''
    Wrapper for the catalog details.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : catalog details fields
        Dictionary keys:
            catalogId (str) Catalog ID
            name (str) Catalog name
            customFields (dict)
            products (list) list of ProductDetails. Catalog products. Only
                            currently sellable products included.
        '''
        self.products = []
        for product in data.pop('products', []):
            self.products.append(ProductDetails(product))

        self.catalogId = data.pop('catalogId', None)
        self.name = data.pop('name', None)
        self.customFields = data.pop('customFields', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        products = []
        for product in self.products:
            products.append(product.serialize())

        return {
            'catalogId'     : self.catalogId,
            'name'          : self.name,
            'customFields'  : self.customFields,
            'products'      : products
            }

class ProductDetails(object):
    '''
    Wrapper for catalog products.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : catalog products fields
        Dictionary keys:
            name (str) Product name in selected language.
            shortName (str) Short product name in selected language.
            description (str) Product description in selected language.
            customFields (str)
            usable (str) List of Validity objects. Times when product is
                         expected to be usable.
            validityLength (int) Product validity length in seconds, from
                                 validityStartFrom event.
            validityStartFrom (str) Event from which validityLength counting
                                    starts. Check ValidityStartFrom for
                                    values.
            productId (str) Internal ID for product this item is based on.
            productSku (str) SKU of the product this item is based on.
            catalogId (str) ID of product catalog where this item is.
            pricingPlanId (str) ID of pricing plan whose price is selected.
            price (str) PriceEvaluation object. Evaluated lowest price from the
                        indicated pricing plan.
            priceToken (str) Token passed to Sale API if price is accepted.
                             Contains enough information to make a sale,
                             including item identity, discounted price with VAT.
                             Has an expiration time, token must be used before
                             this time or sale will be blocked.
            priceTokenExpires (str) Time when priceToken will expire and
                                    becomes unusable.
            translations (list) list of LocalisedDescription objects.
        '''

        self.translations = []
        for translation in data.pop('translations', []):
            self.translations.append(LocalisedDescription(translation))

        self.usable = []
        for u in data.pop('usable', []):
            self.usable.append(Validity(u))

        self.name = data.pop('name', None)
        self.shortName = data.pop('shortName', None)
        self.description = data.pop('description', None)
        self.customFields = data.pop('customFields', None)
        self.validityLength = data.pop('validityLength', None)
        self.validityStartFrom = data.pop('validityStartFrom', None)
        self.productId = data.pop('productId', None)
        self.productSku = data.pop('productSku', None)
        self.catalogId = data.pop('catalogId', None)
        self.pricingPlanId = data.pop('pricingPlanId', None)
        self.price = PriceEvaluation(data.pop('price', {}))
        self.priceToken = data.pop('priceToken', None)
        self.priceTokenExpires = data.pop('priceTokenExpires', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        usable = []
        for validity in self.usable:
            usable.append(validity.serialize())

        translations = []
        for translation in self.translations:
            translations.append(translation.serialize())

        return {
            'name'              : self.name,
            'shortName'         : self.shortName,
            'description'       : self.description,
            'customFields'      : self.customFields,
            'validityLength'    : self.validityLength,
            'validityStartFrom' : self.validityStartFrom,
            'productId'         : self.productId,
            'productSku'        : self.productSku,
            'catalogId'         : self.catalogId,
            'pricingPlanId'     : self.pricingPlanId,
            'price'             : self.price.serialize(),
            'priceToken'        : self.priceToken,
            'priceToken'        : self.priceToken,
            'priceTokenExpires' : self.priceTokenExpires,
            'usable'            : usable,
            'translations'      : translations
            }

class PriceEvaluation(object):
    '''
    Wrapper for evaluated lowest price from the indicated pricing plan.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : catalog products fields
        Dictionary keys:
            basePriceWithVat (double) Base price per unit without volume or
                                      discounts, with VAT.
            basePriceWithoutVat (double) Base price per unit without volume or
                                         discounts, without VAT.
            baseVatAmount (double) VAT amount for base price per unit without
                                   volume or discounts.
            totalPriceWithVat (double) Final total price for given parameters
                                       with volume and discounts, with VAT.
            totalPriceWithoutVat (double) Final total price for given parameters
                                          with volume and discounts, without
                                          VAT.
            totalVatAmount (double) VAT amount for final total price per unit
                                    with volume and discounts.
            pricePerUnitWithVat (double) Final price per unit for given
                                         parameters with discounts, with VAT.
            pricePerUnitWithoutVat (double) Final price per unit for given
                                            parameters with discounts, without
                                            VAT.
            pricePerUnitVatAmount (double) VAT amount for final price per unit
                                           with discounts, with VAT.
            vatPercent (double) Value Added Tax percentage included in prices.
            currency (str) Currency prices are in.
            discounts (list) list of DiscountInfo objects. Discounts applied to
                             the final total price.
        '''
        self.discounts = []
        for discount in data.pop('discounts', []):
            self.discounts.append(DiscountInfo(discount))

        self.basePriceWithVat = data.pop('basePriceWithVat', None)
        self.basePriceWithoutVat = data.pop('basePriceWithoutVat', None)
        self.baseVatAmount = data.pop('baseVatAmount', None)
        self.totalPriceWithVat = data.pop('totalPriceWithVat', None)
        self.totalPriceWithoutVat = data.pop('totalPriceWithoutVat', None)
        self.totalVatAmount = data.pop('totalVatAmount', None)
        self.pricePerUnitWithVat = data.pop('pricePerUnitWithVat', None)
        self.pricePerUnitWithoutVat = data.pop('pricePerUnitWithoutVat', None)
        self.pricePerUnitVatAmount = data.pop('pricePerUnitVatAmount', None)
        self.vatPercent = data.pop('vatPercent', None)
        self.currency = data.pop('currency', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''

        discounts = []
        for discount in self.discounts:
            discounts.append(discount.serialize())

        return {
            'basePriceWithVat' : self.basePriceWithVat,
            'basePriceWithoutVat' : self.basePriceWithoutVat,
            'baseVatAmount' : self.baseVatAmount,
            'totalPriceWithVat' : self.totalPriceWithVat,
            'totalPriceWithoutVat' : self.totalPriceWithoutVat,
            'totalVatAmount' : self.totalVatAmount,
            'pricePerUnitWithVat' : self.pricePerUnitWithVat,
            'pricePerUnitWithoutVat' : self.pricePerUnitWithoutVat,
            'pricePerUnitVatAmount' : self.pricePerUnitVatAmount,
            'vatPercent' : self.vatPercent,
            'currency' : self.currency,
            'discounts' : discounts
            }

class DiscountInfo(object):
    '''
    Wrapper for the discount info.
    '''
    def __init__(self, data={}):
        '''
        Args:
            data (dict) : discount info fields
        Dictionary keys:
            'title' (str) Discount title
            'amount' (double) Discount amount
            'vatIncluded' (bool) Is VAT included in discount amount
        '''
        self.title = data.pop('title', None)
        self.amount = data.pop('amount', None)
        self.vatIncluded = data.pop('vatIncluded', None)

    def serialize(self):
        '''
        Make object JSON serializable.
        '''
        return {
            'title'         : self.title,
            'amount'        : self.amount,
            'vatIncluded'   : self.vatIncluded
            }
