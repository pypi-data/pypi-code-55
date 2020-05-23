"""
# cdk8s-flux

Manage your kubernetes cluster in a GitOps fashion with [Flux](https://fluxcd.io/), construct library for [cdk8s project](https://cdk8s.io/)🚀

## Overview

**cdk8s-flux** is a [cdk8s](https://cdk8s.io/) library which allows you to deploy define a installation of a Flux daemon in your kubernetes cluster with just a few lines of code.
This could be used as an alternative to the [Flux Helm Chart](https://docs.fluxcd.io/en/latest/tutorials/get-started-helm/) or the `fluxctl install` command.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Flux(self, "flux",
    ns="flux",
    name="flux",
    image="fluxcd/flux",
    tag="1.19.0",
    replicas=1,
    arguments=["--memcached-service=", "--ssh-keygen-dir=/etc/fluxd/keygen", "--git-url=git@github.com:rafaribe/cdk8s-k3s-gitops.git", "--git-branch=master", "--git-path=cluster", "--git-label=flux", "--git-user=flux", "--git-email=flux@rafaribe.com", "--git-poll-interval=5m", "--sync-garbage-collection"
    ]
)
```

<details>
<summary>flux.k8s.yaml</summary>

```yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    name: flux
  name: flux
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    name: flux
  name: flux
  namespace: flux
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    name: flux
  name: flux
rules:
  - apiGroups:
      - "*"
    resources:
      - "*"
    verbs:
      - "*"
  - nonResourceURLs:
      - "*"
    verbs:
      - "*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    name: flux
  name: flux
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flux
subjects:
  - kind: ServiceAccount
    name: flux
    namespace: flux
---
apiVersion: v1
kind: Secret
metadata:
  name: flux-git-deploy
  namespace: flux
type: Opaque
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flux
  namespace: flux
spec:
  replicas: 1
  selector:
    matchLabels:
      name: flux
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        name: flux
    spec:
      containers:
        - args:
            - --memcached-service=
            - --ssh-keygen-dir=/etc/fluxd/keygen
            - --git-url=git@github.com:rafaribe/cdk8s-k3s-gitops.git
            - --git-branch=master
            - --git-path=cluster
            - --git-label=flux
            - --git-user=flux
            - --git-email=flux@rafaribe.com
            - --git-poll-interval=5m
            - --sync-garbage-collection
          image: raspbernetes/flux:1.19.0
          imagePullPolicy: IfNotPresent
          livenessProbe:
            httpGet:
              path: api/flux/v6/identity.pub
              port: 3030
            initialDelaySeconds: 5
            timeoutSeconds: 5
          name: flux
          ports:
            - containerPort: 3030
          readinessProbe:
            httpGet:
              path: api/flux/v6/identity.pub
              port: 3030
            initialDelaySeconds: 5
            timeoutSeconds: 5
          resources:
            limits:
              cpu: 150m
              memory: 256Mi
          volumeMounts:
            - mountPath: /etc/fluxd/ssh
              name: git-key
              readOnly: true
            - mountPath: /etc/fluxd/keygen
              name: git-keygen
      serviceAccountName: flux
      volumes:
        - name: git-key
          secret:
            defaultMode: 256
            secretName: flux-git-deploy
        - emptyDir:
            medium: Memory
          name: git-keygen
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memcached
  namespace: flux
spec:
  replicas: 1
  selector:
    matchLabels:
      name: memcached
  template:
    metadata:
      labels:
        name: memcached
    spec:
      containers:
        - args:
            - -m 512
            - -I 5m
            - -p 11211
          image: memcached:1.5.20
          name: memcached
          ports:
            - containerPort: 11211
              name: clients
          securityContext:
            allowPrivilegeEscalation: false
            runAsGroup: 11211
            runAsUser: 11211
---
apiVersion: v1
kind: Service
metadata:
  name: memcached
  namespace: flux
spec:
  ports:
    - name: memcached
      port: 11211
  selector:
    name: memcached
```

</details>

## Installation

[cdk8s](https://cdk8s.io) supports TypeScript and Python at this point, so as cdk8s-flux.

We'd recommend to walk through the [cdk8s Getting Started guide](https://cdk8s.io/getting-started/) before using this library, if you're very new to cdk8s world.

### TypeScript

Use `npm` or `yarn` to install.

```shell
$ npm install -s cdk8s-flux
```

or

```shell
$ yarn add cdk8s-flux
```

### Python

```shell
$ pip install cdk8s-flux
```

## Contribution

1. Fork ([https://github.com/toricls/cdk8s-debore/fork](https://github.com/toricls/cdk8s-debore/fork))
2. Bootstrap the repo:

   ```bash
   yarn install # installs dependencies
   ```
3. Development scripts:

| Command            	| Description                                             	|
|--------------------	|---------------------------------------------------------	|
| `yarn compile`     	| Compiles jsii                                           	|
| `yarn watch`       	| Watch & compile                                         	|
| `yarn test`        	| Runs the jest unit tests                                	|
| `yarn test -u`     	| Updates jest snapshots                                  	|
| `yarn run package` 	| Outputs the `jsii` generated packages in TS and Python  	|
| `yarn build`       	| Compile + Test + Package                                	|
| `yarn bump`        	| Bumps version                                           	|
| `yarn release`     	| Bump + push to master                                   	|
| `yarn rmist`       	| Deletes node_modules and runs installs dependencies     	|
| `yarn lint`        	| Lint with eslinter                                      	|
| `yarn prettier`    	| Runs prettier and updates the files in place            	|
| `yarn run import`  	| cdk8s imports k8s and crds into the `imports` directory 	|
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## License

[Apache License, Version 2.0](./LICENSE)

## Author

[Rafael Ribeiro](https://github.com/rafaribe)

## Thank you:

Thank you to the `devs` of the following projects, from where I got some inspiration to create this library:

* [cdk8s-redis](https://github.com/eladb/cdk8s-redis)
* [cdk8s-debore](https://github.com/toricls/cdk8s-debore)
* [jsii-library-template](https://github.com/eladb/jsii-library-template)
* [cdk8s](https://github.com/awslabs/cdk8s)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import cdk8s
import constructs

from ._jsii import *


class Flux(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s-flux.Flux"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, construct_id: str, *, arguments: typing.List[str], image: str, name: str, ns: str, tag: str, memcached_tag: typing.Optional[str]=None, replicas: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param construct_id: -
        :param arguments: Flux Arguments.
        :param image: The image for flux (docker hub only).
        :param name: The name for the flux container.
        :param ns: The Namespace that should be used for the resources.
        :param tag: The tag for the flux image.
        :param memcached_tag: The tag for the memcached image * @default 1.5.20.
        :param replicas: Number of replicas. Default: 1

        stability
        :stability: experimental
        """
        options = FluxOptions(arguments=arguments, image=image, name=name, ns=ns, tag=tag, memcached_tag=memcached_tag, replicas=replicas)

        jsii.create(Flux, self, [scope, construct_id, options])


@jsii.data_type(jsii_type="cdk8s-flux.FluxOptions", jsii_struct_bases=[], name_mapping={'arguments': 'arguments', 'image': 'image', 'name': 'name', 'ns': 'ns', 'tag': 'tag', 'memcached_tag': 'memcachedTag', 'replicas': 'replicas'})
class FluxOptions():
    def __init__(self, *, arguments: typing.List[str], image: str, name: str, ns: str, tag: str, memcached_tag: typing.Optional[str]=None, replicas: typing.Optional[jsii.Number]=None) -> None:
        """
        :param arguments: Flux Arguments.
        :param image: The image for flux (docker hub only).
        :param name: The name for the flux container.
        :param ns: The Namespace that should be used for the resources.
        :param tag: The tag for the flux image.
        :param memcached_tag: The tag for the memcached image * @default 1.5.20.
        :param replicas: Number of replicas. Default: 1

        stability
        :stability: experimental
        """
        self._values = {
            'arguments': arguments,
            'image': image,
            'name': name,
            'ns': ns,
            'tag': tag,
        }
        if memcached_tag is not None: self._values["memcached_tag"] = memcached_tag
        if replicas is not None: self._values["replicas"] = replicas

    @builtins.property
    def arguments(self) -> typing.List[str]:
        """Flux Arguments.

        stability
        :stability: experimental
        """
        return self._values.get('arguments')

    @builtins.property
    def image(self) -> str:
        """The image for flux (docker hub only).

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def name(self) -> str:
        """The name for the flux container.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def ns(self) -> str:
        """The Namespace that should be used for the resources.

        stability
        :stability: experimental
        """
        return self._values.get('ns')

    @builtins.property
    def tag(self) -> str:
        """The tag for the flux image.

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def memcached_tag(self) -> typing.Optional[str]:
        """The tag for the memcached image   * @default 1.5.20.

        stability
        :stability: experimental
        """
        return self._values.get('memcached_tag')

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        """Number of replicas.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('replicas')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FluxOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "Flux",
    "FluxOptions",
]

publication.publish()
