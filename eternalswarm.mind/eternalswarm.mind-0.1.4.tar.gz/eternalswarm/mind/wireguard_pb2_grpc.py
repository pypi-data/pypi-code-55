# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import models_pb2 as models__pb2
from . import wireguard_pb2 as wireguard__pb2


class WireguardStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GenKey = channel.unary_unary(
        '/Wireguard/GenKey',
        request_serializer=models__pb2.EmptyMessage.SerializeToString,
        response_deserializer=wireguard__pb2.Key.FromString,
        )
    self.AddPeer = channel.unary_unary(
        '/Wireguard/AddPeer',
        request_serializer=wireguard__pb2.Peer.SerializeToString,
        response_deserializer=wireguard__pb2.Peer.FromString,
        )
    self.ListPeers = channel.unary_unary(
        '/Wireguard/ListPeers',
        request_serializer=models__pb2.EmptyMessage.SerializeToString,
        response_deserializer=wireguard__pb2.Peers.FromString,
        )
    self.RemovePeer = channel.unary_unary(
        '/Wireguard/RemovePeer',
        request_serializer=wireguard__pb2.Peer.SerializeToString,
        response_deserializer=wireguard__pb2.Peer.FromString,
        )
    self.GetInterface = channel.unary_unary(
        '/Wireguard/GetInterface',
        request_serializer=models__pb2.EmptyMessage.SerializeToString,
        response_deserializer=wireguard__pb2.WireguardInterface.FromString,
        )


class WireguardServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GenKey(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddPeer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListPeers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemovePeer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetInterface(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WireguardServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GenKey': grpc.unary_unary_rpc_method_handler(
          servicer.GenKey,
          request_deserializer=models__pb2.EmptyMessage.FromString,
          response_serializer=wireguard__pb2.Key.SerializeToString,
      ),
      'AddPeer': grpc.unary_unary_rpc_method_handler(
          servicer.AddPeer,
          request_deserializer=wireguard__pb2.Peer.FromString,
          response_serializer=wireguard__pb2.Peer.SerializeToString,
      ),
      'ListPeers': grpc.unary_unary_rpc_method_handler(
          servicer.ListPeers,
          request_deserializer=models__pb2.EmptyMessage.FromString,
          response_serializer=wireguard__pb2.Peers.SerializeToString,
      ),
      'RemovePeer': grpc.unary_unary_rpc_method_handler(
          servicer.RemovePeer,
          request_deserializer=wireguard__pb2.Peer.FromString,
          response_serializer=wireguard__pb2.Peer.SerializeToString,
      ),
      'GetInterface': grpc.unary_unary_rpc_method_handler(
          servicer.GetInterface,
          request_deserializer=models__pb2.EmptyMessage.FromString,
          response_serializer=wireguard__pb2.WireguardInterface.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Wireguard', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
