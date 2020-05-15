# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetDomainsResult:
    """
    A collection of values returned by getDomains.
    """
    def __init__(__self__, domains=None, id=None, include_unverified=None, only_default=None, only_initial=None):
        if domains and not isinstance(domains, list):
            raise TypeError("Expected argument 'domains' to be a list")
        __self__.domains = domains
        """
        One or more `domain` blocks as defined below.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if include_unverified and not isinstance(include_unverified, bool):
            raise TypeError("Expected argument 'include_unverified' to be a bool")
        __self__.include_unverified = include_unverified
        if only_default and not isinstance(only_default, bool):
            raise TypeError("Expected argument 'only_default' to be a bool")
        __self__.only_default = only_default
        if only_initial and not isinstance(only_initial, bool):
            raise TypeError("Expected argument 'only_initial' to be a bool")
        __self__.only_initial = only_initial
class AwaitableGetDomainsResult(GetDomainsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainsResult(
            domains=self.domains,
            id=self.id,
            include_unverified=self.include_unverified,
            only_default=self.only_default,
            only_initial=self.only_initial)

def get_domains(include_unverified=None,only_default=None,only_initial=None,opts=None):
    """
    Use this data source to access information about an existing Domains within Azure Active Directory.

    > **NOTE:** If you're authenticating using a Service Principal then it must have permissions to `Directory.Read.All` within the `Windows Azure Active Directory` API.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_azuread as azuread

    aad_domains = azuread.get_domains()
    pulumi.export("domains", aad_domains.domains)
    ```



    :param bool include_unverified: Set to `true` if unverified Azure AD Domains should be included. Defaults to `false`.
    :param bool only_default: Set to `true` to only return the default domain.
    :param bool only_initial: Set to `true` to only return the initial domain, which is your primary Azure Active Directory tenant domain. Defaults to `false`.
    """
    __args__ = dict()


    __args__['includeUnverified'] = include_unverified
    __args__['onlyDefault'] = only_default
    __args__['onlyInitial'] = only_initial
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azuread:index/getDomains:getDomains', __args__, opts=opts).value

    return AwaitableGetDomainsResult(
        domains=__ret__.get('domains'),
        id=__ret__.get('id'),
        include_unverified=__ret__.get('includeUnverified'),
        only_default=__ret__.get('onlyDefault'),
        only_initial=__ret__.get('onlyInitial'))
