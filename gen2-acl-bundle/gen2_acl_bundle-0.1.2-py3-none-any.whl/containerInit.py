from consolebundle.ConsoleBundle import ConsoleBundle
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from typing import List
from pyfony.kernel.BaseKernel import BaseKernel
from pyfonybundles.Bundle import Bundle
from gen2aclbundle.Gen2AclBundle import Gen2AclBundle

def initContainer(appEnv) -> ContainerInterface:
    class Kernel(BaseKernel):

        def _registerBundles(self) -> List[Bundle]:
            return [
                ConsoleBundle(),
                Gen2AclBundle()
            ]

    kernel = Kernel(
        appEnv,
        resolvePath('gen2aclbundle') + '/_config',
        YamlConfigReader()
    )

    return kernel.initContainer()
