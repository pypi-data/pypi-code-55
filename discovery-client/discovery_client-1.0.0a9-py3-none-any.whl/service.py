import json
import logging
import socket
from functools import singledispatch
from uuid import uuid4


def service(
    name,
    port,
    dc="",
    address=None,
    tags=None,
    meta=None,
    namespace="default",
    check=None,
):
    service_id = f"{name}-{uuid4().hex}"
    address = address = f"{socket.gethostbyname(socket.gethostname())}"
    meta = meta or {}
    tags = tags or []
    response = {
        "name": name,
        "id": service_id,
        "address": address,
        "port": port,
        "tags": tags,
        "meta": meta,
    }
    if check:
        logging.debug(f"CHK: {json.dumps(register_check(check))}")
        response.update(register_check(check))
    return json.dumps(response)


@singledispatch
def register_check(check):
    response = {"check": check}
    return response


@register_check.register(list)
def _(check):
    response = {"checks": []}
    for chk in check:
        response["checks"].append(chk)
    return response


def script(args, name=None, interval="10s", timeout="5s"):
    script_id = f"script-{uuid4().hex}"
    response = {"args": args, "interval": interval, "timeout": timeout}
    if name:
        response.update({"name": name})
    else:
        response.update({"name": script_id})
    return response


def http(
    url,
    name=None,
    tls_skip_verify=True,
    method="GET",
    header={},
    body="",
    interval="10s",
    timeout="5s",
    deregister_after="1m",
):
    http_id = f"http-{uuid4().hex}"
    response = {
        "http": url,
        "tls_skip_verify": tls_skip_verify,
        "method": method,
        "header": header,
        "body": body,
        "interval": interval,
        "timeout": timeout,
        "deregister_critical_service_after": deregister_after,
    }
    if name:
        response.update({"name": name})
    else:
        response.update({"name": http_id})
    return response


def tcp(tcp, name=None, interval="10s", timeout="5s"):
    tcp_id = f"tcp-{uuid4().hex}"
    response = {"tcp": tcp, "interval": interval, "timeout": timeout}
    if name:
        response.update({"name": name})
    else:
        response.update({"name": tcp_id})
    return response


def ttl(notes, name=None, ttl="30s"):
    ttl_id = f"ttl-{uuid4().hex}"
    response = {"notes": notes, "ttl": ttl}
    if name:
        response.update({"name": name})
    else:
        response.update({"name": ttl_id})
    return response


def docker(container_id, args, shell=None, name=None, interval="10s"):
    docker_id = f"docker-{uuid4().hex}"
    response = {
        "docker_container_id": container_id,
        "shell": shell,
        "args": args,
        "interval": interval,
    }
    if name:
        response.update({"name": name})
    else:
        response.update({"name": f"{docker_id}"})
    return response


def grpc(grpc, name=None, tls=True, interval="10s"):
    grpc_id = f"grpc-{uuid4().hex}"
    response = {"grpc": grpc, "grpc_use_tls": tls, "interval": interval}
    if name:
        response.update({"name": name})
    else:
        response.update({"name": grpc_id})
    return response


def alias(service_id, alias_service, name=None):
    """Consul's alias check.

    alias_service: backend
    service_id: frontent
    """
    name = name or f"alias-{uuid4().hex}"
    return {
        "name": name,
        "service_id": service_id,
        "alias_service": alias_service,
    }
