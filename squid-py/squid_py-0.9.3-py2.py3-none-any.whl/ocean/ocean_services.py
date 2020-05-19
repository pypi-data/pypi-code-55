"""Ocean module."""
#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes

from squid_py.ocean.keeper import SquidKeeper as Keeper


class OceanServices:
    """Ocean services class."""

    @staticmethod
    def create_access_service(attributes, service_endpoint):
        """
        Publish an asset with an `Access` service according to the supplied attributes.

        :param attributes: attributes of the access service, dict
        :param service_endpoint: str URL for initiating service access request
        :return: Service instance or None
        """
        service = ServiceDescriptor.access_service_descriptor(
            attributes,
            service_endpoint,
            Keeper.get_instance().get_agreement_template_id(ServiceTypes.ASSET_ACCESS)
        )
        return service

    @staticmethod
    def create_compute_service(attributes, service_endpoint):
        return ServiceDescriptor.compute_service_descriptor(
            attributes,
            service_endpoint,
            Keeper.get_instance().get_agreement_template_id(ServiceTypes.CLOUD_COMPUTE)
        )
