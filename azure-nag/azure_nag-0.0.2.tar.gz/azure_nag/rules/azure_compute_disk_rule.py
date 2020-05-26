"""Rule to ensure all Azure Compute Disk resources are encrypted."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    ERROR as RULE_ERROR
)


class AzureComputeDiskEncryptedRule(BaseRule):
    """Create a rule ensuring the encryptionSettingsCollection property has 'enabled' as true."""

    rule_id = '002'
    description = """Ensure all AzureComputeDisk resources are encrypted by \
validating the 'encryptionSettingsCollection' property is set and configured \
with the 'enabled' sub-property set to true."""
    severity = RULE_ERROR
    url = 'https://github.com/stelligent/mc-nag/tests/templates/azure/' + \
          'azure_compute_disk'
    category_tags = {'compute-disk'}
    source_tags = {'stelligent'}
    resolution = """Add 'encryptionSettingsCollection' dictionary property to the \
AzureComputeDisk resource and ensure the 'enabled' key is set to true.

Example:
"encryptionSettingsCollection": {
    "enabled": true,
    ....
},"""

    def evaluate(self):
        """Find azureComputeDisk resources and validate 'encryptionSettingsCollection' property.

        1. Obtain a list of azureComputeDisk resources.
        2. Search their properties for 'encryptionSettingsCollection'.
        3. Ensure that the 'encryptionSettingsCollection' property is defined.
        4. Ensure 'enabled' sub-property is set to true.
        """
        violating_resources = []

        # Obtain list of storageAccounts resources
        azure_compute_disks = [
            res for res in self.template_model.resources
            if res.resource_type == 'Microsoft.Compute/disks'
        ]

        # Iterate over azureComputeDisk resources
        for compute_disk in azure_compute_disks:
            try:
                # Try to access encryptionSettingsCollection property
                _ = compute_disk.properties['encryptionSettingsCollection']

                # Check to see if sub-property 'enabled' is set to true
                enabled_key = compute_disk.properties['encryptionSettingsCollection']['enabled']
                if enabled_key is not True:
                    violating_resources.append(compute_disk)

            # Add to violating_resources if keys do not exist
            except KeyError:
                violating_resources.append(compute_disk)

        return violating_resources
