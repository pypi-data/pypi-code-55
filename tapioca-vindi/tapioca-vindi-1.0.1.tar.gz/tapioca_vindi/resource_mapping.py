# coding: utf-8

RESOURCE_MAPPING = {
    'customers': {
        'resource': 'customers',
        'docs': 'https://vindi.github.io/api-docs/dist/#/customers',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'customers_unarchive': {
        'resource': 'customers/{id}/unarchive',
        'docs': 'https://vindi.github.io/api-docs/dist/#/customers',
        'methods': ['POST']
    },
    'plans':{
        'resource': 'plans',
        'docs': 'https://vindi.github.io/api-docs/dist/#/plans',
        'methods': ['GET', 'POST', 'PUT']
    },
    'plans_items':{
        'resource': 'plans/{id}/plan_items',
        'docs': 'https://vindi.github.io/api-docs/dist/#/plans',
        'methods': ['GET']
    },
    'products':{
        'resource': 'products',
        'docs': 'https://vindi.github.io/api-docs/dist/#/products',
        'methods': ['GET', 'POST', 'PUT']
    },
    'payment_methods':{
        'resource': 'payment_methods',
        'docs': 'https://vindi.github.io/api-docs/dist/#//payment_methods',
        'methods': ['GET']
    },
    'discounts':{
        'resource': 'discounts',
        'docs': 'https://vindi.github.io/api-docs/dist/#//discounts',
        'methods': ['GET', 'POST', 'DELETE']
    },
    'subscriptions':{
        'resource': 'subscriptions',
        'docs': 'https://vindi.github.io/api-docs/dist/#//subscriptions',
        'methods': ['GET', 'POST', 'PUT', "DELETE"]
    },
    'subscriptions_product_items':{
        'resource': 'subscriptions/{id}/product_items',
        'docs': 'https://vindi.github.io/api-docs/dist/#//subscriptions',
        'methods': ['GET']
    },
    'subscriptions_product_reactivate':{
        'resource': 'subscriptions/{id}/reactivate',
        'docs': 'https://vindi.github.io/api-docs/dist/#//subscriptions',
        'methods': ['POST']
    },
    'subscriptions_product_renew':{
        'resource': 'subscriptions/{id}/renew',
        'docs': 'https://vindi.github.io/api-docs/dist/#//subscriptions',
        'methods': ['POST']
    },    
    'product_itens':{
        'resource': 'product_itens',
        'docs': 'https://vindi.github.io/api-docs/dist/#//product_itens',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'periods':{
        'resource': 'periods',
        'docs': 'https://vindi.github.io/api-docs/dist/#//periods',
        'methods': ['GET', 'PUT']
    },
    'periods_bill':{
        'resource': 'periods/{id}/bill',
        'docs': 'https://vindi.github.io/api-docs/dist/#//periods',
        'methods': ['POST']
    },
    'periods_usages':{
        'resource': 'periods/{id}/usages',
        'docs': 'https://vindi.github.io/api-docs/dist/#//periods',
        'methods': ['POST']
    },
    'bills':{
        'resource': 'bills',
        'docs': 'https://vindi.github.io/api-docs/dist/#//bills',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'bills_approve':{
        'resource': 'bills/{id}/approve',
        'docs': 'https://vindi.github.io/api-docs/dist/#//bills',
        'methods': ['POST']
    },
    'bills_items':{
        'resource': 'bills/{id}/bill_items',
        'docs': 'https://vindi.github.io/api-docs/dist/#//bills',
        'methods': ['GET']
    },
    'bills_charge':{
        'resource': 'bills/{id}/charge',
        'docs': 'https://vindi.github.io/api-docs/dist/#//bills',
        'methods': ['POST']
    },
    'bills_invoice':{
        'resource': 'bills/{id}/invoice',
        'docs': 'https://vindi.github.io/api-docs/dist/#//bills',
        'methods': ['GET']
    },
    'bill_items': {
        'resource': 'bill_items',
        'docs': 'https://vindi.github.io/api-docs/dist/#/bill_items',
        'methods': ['GET']
    },
    'charges': {
        'resource': 'charges',
        'docs': 'https://vindi.github.io/api-docs/dist/#/charges',
        'methods': ['GET']
    },
    'transactions': {
        'resource': 'transactions',
        'docs': 'https://vindi.github.io/api-docs/dist/#/transactions',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'payment_profile': {
        'resource': 'payment_profile',
        'docs': 'https://vindi.github.io/api-docs/dist/#/payment_profile',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'usage': {
        'resource': 'usage',
        'docs': 'https://vindi.github.io/api-docs/dist/#/usage',
        'methods': ['POST', 'DELETE']
    },
    'invoice': {
        'resource': 'invoice',
        'docs': 'https://vindi.github.io/api-docs/dist/#/invoice',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'movements': {
        'resource': 'movements',
        'docs': 'https://vindi.github.io/api-docs/dist/#/movements',
        'methods': ['POST']
    },
    'messages': {
        'resource': 'messages',
        'docs': 'https://vindi.github.io/api-docs/dist/#/messages',
        'methods': ['GET', 'POST']
    },
    'export_batchs': {
        'resource': 'export_batchs',
        'docs': 'https://vindi.github.io/api-docs/dist/#/export_batchs',
        'methods': ['GET', 'POST']
    },
    'import_batchs': {
        'resource': 'import_batchs',
        'docs': 'https://vindi.github.io/api-docs/dist/#/import_batchs',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'issues': {
        'resource': 'issues',
        'docs': 'https://vindi.github.io/api-docs/dist/#/issues',
        'methods': ['GET', 'PUT', ]
    },
    'notifications': {
        'resource': 'notifications',
        'docs': 'https://vindi.github.io/api-docs/dist/#/notifications',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'merchants': {
        'resource': 'merchants',
        'docs': 'https://vindi.github.io/api-docs/dist/#/merchants',
        'methods': ['GET']
    },
    'merchants_users': {
        'resource': 'merchants_users',
        'docs': 'https://vindi.github.io/api-docs/dist/#/merchants_users',
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    },
    'roles': {
        'resource': 'roles',
        'docs': 'https://vindi.github.io/api-docs/dist/#/roles',
        'methods': ['GET']
    },
    'users': {
        'resource': 'users/current',
        'docs': 'https://vindi.github.io/api-docs/dist/#/users',
        'methods': ['GET']
    },
    'public': {
        'resource': 'public/payment_profile',
        'docs': 'https://vindi.github.io/api-docs/dist/#/public',
        'methods': ['POST']
    },

}

