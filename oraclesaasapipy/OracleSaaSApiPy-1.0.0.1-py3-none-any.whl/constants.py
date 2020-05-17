"""
    OracleSaaSApiPy - constants.py

    includes the list of
    1/ All Valid UCM Account
    2/ All Valid UCM Security Groups
    3/ All valid scheduled jobs along with job details

    In case your job is not in the list, you can add it to the
    dict JOBS.
"""

UCM_ACCOUNTS = [
    'crm$/accessgroups$/import$',
    'crm$/agreement$/import$',
    'crm$/appointment$/import$',
    'crm$/asset$/import$',
    'crm$/atcproductcatalog$/export$',
    'crm$/atcproductcatalog$/images$',
    'crm$/atcproductcatalog$/import$',
    'crm$/atcproductcatalog$/schema$',
    'crm$/classificationcode$/import$',
    'crm$/commoncustomobject$/import$',
    'crm$/consumer$/import$',
    'crm$/contact$/import$',
    'crm$/contract$/import$',
    'crm$/countrystructure$/import$',
    'crm$/cssroles$/import$',
    'crm$/customer$/import$',
    'crm$/customerhierarchy$/import$',
    'crm$/customerhierarchymember$/import$',
    'crm$/dealregistration$/import$',
    'crm$/employeeresource$/import$',
    'crm$/geography$/import$',
    'crm$/groupcustomer$/import$',
    'crm$/interaction$/import$',
    'crm$/iotasset$/import$',
    'crm$/iotreg$/import$',
    'crm$/lead$/import$',
    'crm$/legalentity$/import$',
    'crm$/mctagentconnparams$/import$',
    'crm$/mctctdagent$/import$',
    'crm$/mktactadvertising$/import$',
    'crm$/mktactevent$/import$',
    'crm$/mktactinteraction$/import$',
    'crm$/mktbudget$/import$',
    'crm$/mktcampaigns$/import$',
    'crm$/mktcampmembers$/import$',
    'crm$/mktlist$/import$',
    'crm$/mkttopextn$/import$',
    'crm$/mootopextn$/import$',
    'crm$/note$/import$',
    'crm$/opportunity$/import$',
    'crm$/partner$/import$',
    'crm$/partnercontact$/import$',
    'crm$/productgroup$/import$',
    'crm$/programenrollments$/import$',
    'crm$/promotion$/import$',
    'crm$/quota$/import$',
    'crm$/resourceteam$/import$',
    'crm$/response$/import$',
    'crm$/salesaccountresourceteam$/import$',
    'crm$/salesbusinessplan$/import$',
    'crm$/salesobjective$/import$',
    'crm$/simplifiedaccount$/import$',
    'crm$/simplifiedcontact$/import$',
    'crm$/simplifiedhousehold$/import$',
    'crm$/sourcesystemreference$/import$',
    'crm$/subscription$/import$',
    'crm$/task$/import$',
    'crm$/territory$/import$',
    'crm$/zcatopextn$/export$',
    'csm$/archive$',
    'fin$/assets$/export$',
    'fin$/assets$/import$',
    'fin$/budgetarycontrol$/import$',
    'fin$/budgetbalance$/import$',
    'fin$/cashmanagement$/export$',
    'fin$/cashmanagement$/import$',
    'fin$/generalledger$/export$',
    'fin$/generalledger$/import$',
    'fin$/intercompany$/import$',
    'fin$/payables$/export$',
    'fin$/payables$/import$',
    'fin$/payments$/export$',
    'fin$/payments$/import$',
    'fin$/receivables$/export$',
    'fin$/receivables$/import$',
    'fin$/tax$/export$',
    'fin$/tax$/import$',
    'hcm$/common$/content$',
    'hcm$/dataloader$/export$',
    'hcm$/dataloader$/import$',
    'hed$/data$/export$',
    'hed$/data$/import$',
    'ic$/incentivecompensationcurrencyexchangerates$/import$',
    'ic$/incentivecompensationparticipant$/import$',
    'ic$/incentivecompensationparticipantcompensationplan$/import$',
    'ic$/incentivecompensationparticipantgoal$/import$',
    'ic$/incentivecompensationtransaction$/import$',
    'prc$/blanketpurchaseagreement$/import$',
    'prc$/contractpurchaseagreement$/import$',
    'prc$/purchaseorder$/import$',
    'prc$/requisition$/import$',
    'prc$/supplier$/import$',
    'prj$/grantsmanagement$/import$',
    'prj$/projectbilling$/import$',
    'prj$/projectcontrol$/import$',
    'prj$/projectcosting$/import$',
    'prj$/projectenterpriseresource$/import$',
    'prj$/projectfoundation$/import$',
    'prj$/projectmanagement$/import$',
    'prj$/projectresourcemanagement$/import$',
    'prj$/projectsetup$/import$',
    'psc$/commoncomponents$/import$',
    'scm$/b2bconfiguration$/import$',
    'scm$/brazilsefazpartnermessages$/export$',
    'scm$/brazilsefazpartnermessages$/import$',
    'scm$/brazilsefazsuppliermessages$/import$',
    'scm$/cmkoutboundmessagequeue$/export$',
    'scm$/collaborationorderforecast$/export$',
    'scm$/collaborationorderforecast$/import$',
    'scm$/customerasset$/import$',
    'scm$/cyclecount$/import$',
    'scm$/installedbaseasset$/import$',
    'scm$/inventorybalance$/import$',
    'scm$/inventoryreservation$/import$',
    'scm$/inventorytransaction$/import$',
    'scm$/item$/import$',
    'scm$/maintenanceasset$/import$',
    'scm$/maintenanceworkdefinition$/import$',
    'scm$/maintenanceworkorder$/import$',
    'scm$/oagis10partnermessages$/export$',
    'scm$/oagis10partnermessages$/import$',
    'scm$/oagis7partnermessages$/export$',
    'scm$/oagis7partnermessages$/import$',
    'scm$/orderfulfillmentrequest$/export$',
    'scm$/orderfulfillmentresponse$/import$',
    'scm$/performshippingtransaction$/import$',
    'scm$/planningdataloader$/export$',
    'scm$/planningdataloader$/import$',
    'scm$/pricelists$/import$',
    'scm$/productgenealogy$/import$',
    'scm$/receivingreceipt$/import$',
    'scm$/shipmentrequest$/import$',
    'scm$/sourcesalesorder$/import$',
    'scm$/standardcost$/import$',
    'scm$/supplyorder$/import$',
    'scm$/vmirelationship$/export$',
    'scm$/vmirelationship$/import$',
    'scm$/workdefinition$/import$',
    'scm$/workorder$/import$',
    'scm$/workordermaterialtransaction$/import$',
    'scm$/workorderoperationtransaction$/import$',
    'scm$/workorderresourcetransaction$/import$',
    'setup$/functionalsetupmanager$/export$',
    'setup$/functionalsetupmanager$/import$'
]

UCM_SECURITY_GROUPS = [
    'crm',
    'crmstage',
    'csmimportexport',
    'faauthpubcontent',
    'fafusionimportexport',
    'personalspaces',
    'ucm_spaces'
]

JOBS = {
    'Import Blanket Agreements': {
        'interfaceId': '23',
        'jobPackageName': '/oracle/apps/ess/prc/po/pdoi',
        'jobDefinitionName': 'ImportBPAJob',
        'ucmAccount': 'prc$/blanketpurchaseagreement$/import$'
    },

    'Item Import': {
        'interfaceId': '29',
        'jobPackageName': '/oracle/apps/ess/scm/productModel/items/',
        'jobDefinitionName': 'ItemImportJobDef',
        'ucmAccount': 'prc$/blanketpurchaseagreement$/import$'
    },

    'Import Suppliers': {
        'interfaceId': '24',
        'jobPackageName': '/oracle/apps/ess/prc/poz/supplierImport',
        'jobDefinitionName': 'ImportSuppliers',
        'ucmAccount': 'prc$/supplier$/import$'
    },

    'Import Supplier Contacts': {
        'interfaceId': '26',
        'jobPackageName': '/oracle/apps/ess/prc/poz/supplierImport',
        'jobDefinitionName': 'ImportSupplierContacts',
        'ucmAccount': 'prc$/supplier$/import$'
    },

    'Import Supplier Sites': {
        'interfaceId': '25',
        'jobPackageName': '/oracle/apps/ess/prc/poz/supplierImport',
        'jobDefinitionName': 'ImportSupplierSites',
        'ucmAccount': 'prc$/supplier$/import$'
    },

    'Import Supplier Site Assignments': {
        'interfaceId': '27',
        'jobPackageName': '/oracle/apps/ess/prc/poz/supplierImport',
        'jobDefinitionName': 'ImportSupplierSiteAssignments',
        'ucmAccount': 'prc$/supplier$/import$'
    },

    'Import Supplier Addresses': {
        'interfaceId': '56',
        'jobPackageName': '/oracle/apps/ess/prc/poz/supplierImport',
        'jobDefinitionName': 'ImportSupplierAddresses',
        'ucmAccount': 'prc$/supplier$/import$'
    },

    'Import Requisitions': {
        'interfaceId': '28',
        'jobPackageName': '/oracle/apps/ess/prc/por/createReq/reqImport',
        'jobDefinitionName': 'RequisitionImportJob',
        'ucmAccount': 'prc$/requisition$/import$'
    }


}
