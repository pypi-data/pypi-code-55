import unittest

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

import example
from phiskills.grpc import Api, Status

GRPC_PORT = 50051


class ApiTestCase(unittest.TestCase):
    def test_api(self):
        print('# Initialize test API')
        a = Api('test-api')
        a.use_port(GRPC_PORT)
        self.assertEqual(a.status, Status.UNKNOWN, 'New API failed: wrong status')
        print('# Register services')
        example.add_ServiceServicer_to_server(ExampleServer(), a.server)
        print('# Start API')
        a.start()
        self.assertEqual(a.status, Status.SERVING, 'Start API failed: wrong status')
        print('# Dial API')
        with grpc.insecure_channel(f'localhost:{GRPC_PORT}') as conn:
            print('# Initialize health client')
            self.health_client = health_pb2_grpc.HealthStub(conn)

            self.__call_health_check()

            print('# Initialize main client')
            self.client = example.ServiceStub(conn)

            self.__call_simple_request()
            self.__call_server_stream()
            self.__call_client_stream()
            self.__call_bidirectional_stream()

        print('# Stop API')
        a.stop()
        self.assertEqual(a.status, Status.NOT_SERVING, 'Stop API failed: wrong status')

    def __call_health_check(self):
        print('## Test Health Check')
        request = health_pb2.HealthCheckRequest(service='test-api')
        response = self.health_client.Check(request)
        print(f'- Response: {response}', end='')
        expected = health_pb2.HealthCheckResponse.SERVING
        self.assertEqual(response.status, expected, 'Health Check failed')

    def __call_simple_request(self):
        print('## Test Simple Request')
        response = self.client.Simple(example.Request(value='Test'))
        print(f'- Response: {response}', end='')
        self.assertEqual(response.value, 'Test', 'Simple Request failed')

    def __call_server_stream(self):
        print('## Test Server Stream')
        i = 1
        for response in self.client.ServerStream(example.Request(value='Test')):
            print(f'- Response: {response}', end='')
            self.assertEqual(response.value, f"Test {i}", 'Server Stream failed')
            i += 1

    def __call_client_stream(self):
        print('## Test Client Stream')
        response = self.client.ClientStream(generate_stream())
        print(f'- Response: {response}', end='')
        expected = ', '.join([f'Test {i}' for i in range(1, 4)])
        self.assertEqual(response.value, expected, 'Client Stream failed')

    def __call_bidirectional_stream(self):
        print('## Test Bidirectional Stream')
        i = 0
        for response in self.client.BidirectionalStream(generate_stream()):
            print(f'- Response: {response}', end='')
            x = i // 3 + 1
            y = i % 3 + 1
            self.assertEqual(response.value, f"Test {x}.{y}", 'Server Stream failed')
            i += 1


def generate_stream():
    for i in range(1, 4):
        yield example.Request(value=f'Test {i}')


class ExampleServer(example.ServiceServicer):
    def Simple(self, request, _):
        return example.Response(value=request.value)

    def ServerStream(self, request, _):
        for i in range(1, 4):
            yield example.Response(value=f'{request.value} {i}')

    def ClientStream(self, request_iterator, _):
        requests = []
        for request in request_iterator:
            requests.append(request.value)
        return example.Response(value=', '.join(requests))

    def BidirectionalStream(self, request_iterator, _):
        for request in request_iterator:
            for i in range(1, 4):
                yield example.Response(value=f'{request.value}.{i}')


if __name__ == '__main__':
    unittest.main()
