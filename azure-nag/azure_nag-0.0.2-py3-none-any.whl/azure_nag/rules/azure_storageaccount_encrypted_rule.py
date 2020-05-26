"""Rule to ensure all StorageAccount resources are encrypted."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    ERROR as RULE_ERROR
)


class AzureStorageAccountEncryptedRule(BaseRule):
    """Create a rule ensuring the encryption property is created."""

    rule_id = '001'
    description = """Ensure all StorageAccount resources are encrypted by \
validating the 'encryption' property is set and configured."""
    severity = RULE_ERROR
    url = 'https://github.com/stelligent/mc-nag/tests/templates/azure/' + \
          'azure_storageAccounts'
    category_tags = {'storage'}
    source_tags = {'stelligent'}
    resolution = """Add 'encryption' property to the storageAccount resource \
and ensure the service type is set to 'enabled'.

Example:
"encryption": {
  "services": {
    "blob": {
      "enabled": true,
      "keyType": "Account"
    }
  },
  "keySource": "Microsoft.Storage"
},"""

    def evaluate(self):
        """Find storageAccount resources and validate 'encryption' property.

        1. Obtain a list of storageAccount resources.
        2. Search their properties for 'encryption'.
        3. Ensure at least one service is enabled.
        4. Ensure keySource subproperty is set.
        """
        violating_resources = []

        # Obtain list of storageAccounts resources
        storage_accounts = [
            res for res in self.template_model.resources
            if res.resource_type == 'Microsoft.Storage/storageAccounts'
        ]

        # Iterate over storageAccount resources
        for resource in storage_accounts:
            try:
                # Try to access keySource property
                _ = resource.properties['encryption']['keySource']

                # Iterate over services subproperty to see if any are enabled
                services = resource.properties['encryption']['services']
                for _, service_dict in services.items():
                    if 'enabled' not in service_dict or \
                            not service_dict['enabled']:
                        violating_resources.append(resource)
            # Add to violating_resources if keys do not exist
            except KeyError:
                violating_resources.append(resource)

        return violating_resources
