import json
import uuid


class Check:

    def __init__(self, name, identifier, check):
        self.name = f"{name}-{uuid.uuid4().hex}"
        self.identifier = f"{identifier}-{uuid.uuid4().hex}"
        self.check = check

    def json(self):
        response = dict(id=self.identifier)
        response.update(self.check)
        return json.dumps(response)


def script(args, interval="10s", timeout="5s"):
    return {"args": args, "interval": interval, "timeout": timeout}


def http(url, interval="10s", timeout="5s", deregister_after="1m"):
    return {
        "http": url,
        "interval": interval,
        "timeout": timeout,
        "DeregisterCriticalServiceAfter": deregister_after,
    }


def tcp(tcp, interval="10s", timeout="5s"):    
    return {"tcp": tcp, "interval": interval, "timeout": timeout}


def ttl(self, notes, ttl="30s"):
    return {"notes": notes, "ttl": ttl}


def docker(container_id, args, interval="10s"):
    return {"docker_container_id": container_id, "args": args, "interval": interval}


def grpc(grpc, tls=True, interval="10s"):
    return {"grpc": grpc, "grpc_use_tls": tls, "interval": interval}


def alias(alias_service):    
    return {"alias_service": alias_service}
