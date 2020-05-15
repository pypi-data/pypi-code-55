# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetServicePrincipalResult:
    """
    A collection of values returned by getServicePrincipal.
    """
    def __init__(__self__, app_roles=None, application_id=None, display_name=None, id=None, oauth2_permissions=None, object_id=None):
        if app_roles and not isinstance(app_roles, list):
            raise TypeError("Expected argument 'app_roles' to be a list")
        __self__.app_roles = app_roles
        if application_id and not isinstance(application_id, str):
            raise TypeError("Expected argument 'application_id' to be a str")
        __self__.application_id = application_id
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        __self__.display_name = display_name
        """
        Display name for the permission that appears in the admin consent and app assignment experiences.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if oauth2_permissions and not isinstance(oauth2_permissions, list):
            raise TypeError("Expected argument 'oauth2_permissions' to be a list")
        __self__.oauth2_permissions = oauth2_permissions
        if object_id and not isinstance(object_id, str):
            raise TypeError("Expected argument 'object_id' to be a str")
        __self__.object_id = object_id
class AwaitableGetServicePrincipalResult(GetServicePrincipalResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServicePrincipalResult(
            app_roles=self.app_roles,
            application_id=self.application_id,
            display_name=self.display_name,
            id=self.id,
            oauth2_permissions=self.oauth2_permissions,
            object_id=self.object_id)

def get_service_principal(application_id=None,display_name=None,oauth2_permissions=None,object_id=None,opts=None):
    """
    Gets information about an existing Service Principal associated with an Application within Azure Active Directory.

    > **NOTE:** If you're authenticating using a Service Principal then it must have permissions to both `Read and write all applications` and `Sign in and read user profile` within the `Windows Azure Active Directory` API.

    ## Example Usage (by Application Display Name)

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_service_principal(display_name="my-awesome-application")
    ```

    ## Example Usage (by Application ID)

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_service_principal(application_id="00000000-0000-0000-0000-000000000000")
    ```

    ## Example Usage (by Object ID)

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_service_principal(object_id="00000000-0000-0000-0000-000000000000")
    ```


    :param str application_id: The ID of the Azure AD Application.
    :param str display_name: The Display Name of the Azure AD Application associated with this Service Principal.
    :param list oauth2_permissions: A collection of OAuth 2.0 permissions exposed by the associated application. Each permission is covered by a `oauth2_permission` block as documented below.
    :param str object_id: The ID of the Azure AD Service Principal.

    The **oauth2_permissions** object supports the following:

      * `adminConsentDescription` (`str`) - The description of the admin consent
      * `adminConsentDisplayName` (`str`) - The display name of the admin consent
      * `id` (`str`) - The unique identifier of the `app_role`.
      * `isEnabled` (`bool`) - Determines if the app role is enabled.
      * `type` (`str`) - The type of the permission
      * `userConsentDescription` (`str`) - The description of the user consent
      * `userConsentDisplayName` (`str`) - The display name of the user consent
      * `value` (`str`) - Specifies the value of the roles claim that the application should expect in the authentication and access tokens.
    """
    __args__ = dict()


    __args__['applicationId'] = application_id
    __args__['displayName'] = display_name
    __args__['oauth2Permissions'] = oauth2_permissions
    __args__['objectId'] = object_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azuread:index/getServicePrincipal:getServicePrincipal', __args__, opts=opts).value

    return AwaitableGetServicePrincipalResult(
        app_roles=__ret__.get('appRoles'),
        application_id=__ret__.get('applicationId'),
        display_name=__ret__.get('displayName'),
        id=__ret__.get('id'),
        oauth2_permissions=__ret__.get('oauth2Permissions'),
        object_id=__ret__.get('objectId'))
