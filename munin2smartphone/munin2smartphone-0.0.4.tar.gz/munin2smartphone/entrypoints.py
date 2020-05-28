import munin2smartphone.config as config
import munin2smartphone.server as server


def run_from_cli():
    configobj = config.Config(withcli=True)
    serverobj = server.Server(configobj, restore=True)
    serverobj.run()


