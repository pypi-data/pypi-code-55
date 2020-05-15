"""
Main interface for appmesh service client

Usage::

    import boto3
    from mypy_boto3.appmesh import AppMeshClient

    session = boto3.Session()

    client: AppMeshClient = boto3.client("appmesh")
    session_client: AppMeshClient = session.client("appmesh")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_appmesh.paginator import (
    ListMeshesPaginator,
    ListRoutesPaginator,
    ListTagsForResourcePaginator,
    ListVirtualNodesPaginator,
    ListVirtualRoutersPaginator,
    ListVirtualServicesPaginator,
)
from mypy_boto3_appmesh.type_defs import (
    CreateMeshOutputTypeDef,
    CreateRouteOutputTypeDef,
    CreateVirtualNodeOutputTypeDef,
    CreateVirtualRouterOutputTypeDef,
    CreateVirtualServiceOutputTypeDef,
    DeleteMeshOutputTypeDef,
    DeleteRouteOutputTypeDef,
    DeleteVirtualNodeOutputTypeDef,
    DeleteVirtualRouterOutputTypeDef,
    DeleteVirtualServiceOutputTypeDef,
    DescribeMeshOutputTypeDef,
    DescribeRouteOutputTypeDef,
    DescribeVirtualNodeOutputTypeDef,
    DescribeVirtualRouterOutputTypeDef,
    DescribeVirtualServiceOutputTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesOutputTypeDef,
    MeshSpecTypeDef,
    RouteSpecTypeDef,
    TagRefTypeDef,
    UpdateMeshOutputTypeDef,
    UpdateRouteOutputTypeDef,
    UpdateVirtualNodeOutputTypeDef,
    UpdateVirtualRouterOutputTypeDef,
    UpdateVirtualServiceOutputTypeDef,
    VirtualNodeSpecTypeDef,
    VirtualRouterSpecTypeDef,
    VirtualServiceSpecTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppMeshClient",)


class Exceptions:
    BadRequestException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    ForbiddenException: Type[Boto3ClientError]
    InternalServerErrorException: Type[Boto3ClientError]
    LimitExceededException: Type[Boto3ClientError]
    NotFoundException: Type[Boto3ClientError]
    ResourceInUseException: Type[Boto3ClientError]
    ServiceUnavailableException: Type[Boto3ClientError]
    TooManyRequestsException: Type[Boto3ClientError]
    TooManyTagsException: Type[Boto3ClientError]


class AppMeshClient:
    """
    [AppMesh.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.can_paginate)
        """

    def create_mesh(
        self,
        meshName: str,
        clientToken: str = None,
        spec: MeshSpecTypeDef = None,
        tags: List[TagRefTypeDef] = None,
    ) -> CreateMeshOutputTypeDef:
        """
        [Client.create_mesh documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.create_mesh)
        """

    def create_route(
        self,
        meshName: str,
        routeName: str,
        spec: RouteSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = None,
        meshOwner: str = None,
        tags: List[TagRefTypeDef] = None,
    ) -> CreateRouteOutputTypeDef:
        """
        [Client.create_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.create_route)
        """

    def create_virtual_node(
        self,
        meshName: str,
        spec: VirtualNodeSpecTypeDef,
        virtualNodeName: str,
        clientToken: str = None,
        meshOwner: str = None,
        tags: List[TagRefTypeDef] = None,
    ) -> CreateVirtualNodeOutputTypeDef:
        """
        [Client.create_virtual_node documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.create_virtual_node)
        """

    def create_virtual_router(
        self,
        meshName: str,
        spec: VirtualRouterSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = None,
        meshOwner: str = None,
        tags: List[TagRefTypeDef] = None,
    ) -> CreateVirtualRouterOutputTypeDef:
        """
        [Client.create_virtual_router documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.create_virtual_router)
        """

    def create_virtual_service(
        self,
        meshName: str,
        spec: VirtualServiceSpecTypeDef,
        virtualServiceName: str,
        clientToken: str = None,
        meshOwner: str = None,
        tags: List[TagRefTypeDef] = None,
    ) -> CreateVirtualServiceOutputTypeDef:
        """
        [Client.create_virtual_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.create_virtual_service)
        """

    def delete_mesh(self, meshName: str) -> DeleteMeshOutputTypeDef:
        """
        [Client.delete_mesh documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.delete_mesh)
        """

    def delete_route(
        self, meshName: str, routeName: str, virtualRouterName: str, meshOwner: str = None
    ) -> DeleteRouteOutputTypeDef:
        """
        [Client.delete_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.delete_route)
        """

    def delete_virtual_node(
        self, meshName: str, virtualNodeName: str, meshOwner: str = None
    ) -> DeleteVirtualNodeOutputTypeDef:
        """
        [Client.delete_virtual_node documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.delete_virtual_node)
        """

    def delete_virtual_router(
        self, meshName: str, virtualRouterName: str, meshOwner: str = None
    ) -> DeleteVirtualRouterOutputTypeDef:
        """
        [Client.delete_virtual_router documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.delete_virtual_router)
        """

    def delete_virtual_service(
        self, meshName: str, virtualServiceName: str, meshOwner: str = None
    ) -> DeleteVirtualServiceOutputTypeDef:
        """
        [Client.delete_virtual_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.delete_virtual_service)
        """

    def describe_mesh(self, meshName: str, meshOwner: str = None) -> DescribeMeshOutputTypeDef:
        """
        [Client.describe_mesh documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.describe_mesh)
        """

    def describe_route(
        self, meshName: str, routeName: str, virtualRouterName: str, meshOwner: str = None
    ) -> DescribeRouteOutputTypeDef:
        """
        [Client.describe_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.describe_route)
        """

    def describe_virtual_node(
        self, meshName: str, virtualNodeName: str, meshOwner: str = None
    ) -> DescribeVirtualNodeOutputTypeDef:
        """
        [Client.describe_virtual_node documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.describe_virtual_node)
        """

    def describe_virtual_router(
        self, meshName: str, virtualRouterName: str, meshOwner: str = None
    ) -> DescribeVirtualRouterOutputTypeDef:
        """
        [Client.describe_virtual_router documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.describe_virtual_router)
        """

    def describe_virtual_service(
        self, meshName: str, virtualServiceName: str, meshOwner: str = None
    ) -> DescribeVirtualServiceOutputTypeDef:
        """
        [Client.describe_virtual_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.describe_virtual_service)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.generate_presigned_url)
        """

    def list_meshes(self, limit: int = None, nextToken: str = None) -> ListMeshesOutputTypeDef:
        """
        [Client.list_meshes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_meshes)
        """

    def list_routes(
        self,
        meshName: str,
        virtualRouterName: str,
        limit: int = None,
        meshOwner: str = None,
        nextToken: str = None,
    ) -> ListRoutesOutputTypeDef:
        """
        [Client.list_routes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_routes)
        """

    def list_tags_for_resource(
        self, resourceArn: str, limit: int = None, nextToken: str = None
    ) -> ListTagsForResourceOutputTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_tags_for_resource)
        """

    def list_virtual_nodes(
        self, meshName: str, limit: int = None, meshOwner: str = None, nextToken: str = None
    ) -> ListVirtualNodesOutputTypeDef:
        """
        [Client.list_virtual_nodes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_virtual_nodes)
        """

    def list_virtual_routers(
        self, meshName: str, limit: int = None, meshOwner: str = None, nextToken: str = None
    ) -> ListVirtualRoutersOutputTypeDef:
        """
        [Client.list_virtual_routers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_virtual_routers)
        """

    def list_virtual_services(
        self, meshName: str, limit: int = None, meshOwner: str = None, nextToken: str = None
    ) -> ListVirtualServicesOutputTypeDef:
        """
        [Client.list_virtual_services documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.list_virtual_services)
        """

    def tag_resource(self, resourceArn: str, tags: List[TagRefTypeDef]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.untag_resource)
        """

    def update_mesh(
        self, meshName: str, clientToken: str = None, spec: MeshSpecTypeDef = None
    ) -> UpdateMeshOutputTypeDef:
        """
        [Client.update_mesh documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.update_mesh)
        """

    def update_route(
        self,
        meshName: str,
        routeName: str,
        spec: RouteSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = None,
        meshOwner: str = None,
    ) -> UpdateRouteOutputTypeDef:
        """
        [Client.update_route documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.update_route)
        """

    def update_virtual_node(
        self,
        meshName: str,
        spec: VirtualNodeSpecTypeDef,
        virtualNodeName: str,
        clientToken: str = None,
        meshOwner: str = None,
    ) -> UpdateVirtualNodeOutputTypeDef:
        """
        [Client.update_virtual_node documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.update_virtual_node)
        """

    def update_virtual_router(
        self,
        meshName: str,
        spec: VirtualRouterSpecTypeDef,
        virtualRouterName: str,
        clientToken: str = None,
        meshOwner: str = None,
    ) -> UpdateVirtualRouterOutputTypeDef:
        """
        [Client.update_virtual_router documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.update_virtual_router)
        """

    def update_virtual_service(
        self,
        meshName: str,
        spec: VirtualServiceSpecTypeDef,
        virtualServiceName: str,
        clientToken: str = None,
        meshOwner: str = None,
    ) -> UpdateVirtualServiceOutputTypeDef:
        """
        [Client.update_virtual_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Client.update_virtual_service)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_meshes"]) -> ListMeshesPaginator:
        """
        [Paginator.ListMeshes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListMeshes)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_routes"]) -> ListRoutesPaginator:
        """
        [Paginator.ListRoutes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListRoutes)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Paginator.ListTagsForResource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListTagsForResource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_nodes"]
    ) -> ListVirtualNodesPaginator:
        """
        [Paginator.ListVirtualNodes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualNodes)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_routers"]
    ) -> ListVirtualRoutersPaginator:
        """
        [Paginator.ListVirtualRouters documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualRouters)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_services"]
    ) -> ListVirtualServicesPaginator:
        """
        [Paginator.ListVirtualServices documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualServices)
        """
