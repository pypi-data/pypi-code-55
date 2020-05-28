from ftw.upgrade import UpgradeStep
from plone import api
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class UninstallObsoleteAddressblockJs(UpgradeStep):
    """Uninstall obsolete addressblock.js.
    """

    def __call__(self):

        if IS_PLONE_5:

            to_remove = [u'resource-ftw-addressblock-geo-addressblock-js',
                         u'resource-ftw-simplelayout-mapblock-resources']

            record = 'plone.bundles/plone-legacy.resources'
            resources = api.portal.get_registry_record(record)

            for resource in to_remove:
                if resource in resources:
                    resources.remove(resource)

        else:
            self.install_upgrade_profile(steps=['jsregistry'])
