from dataclasses import dataclass
from user_agents import parse

@dataclass(order=False)
class APIDevice:
    """
           Device detection class

           @:param user_agent_string: user agent string
           @:param minified: get all data or minified

           @:method getdevice method return detected device dictionary

     """

    user_agent_string: str
    minified: bool = True

    def getdevice(self) -> dict:
        if not isinstance(self.user_agent_string, str) or len(self.user_agent_string) == 0:
            raise Exception("Incorrect user agent string")

        elif not isinstance(self.minified, bool):
            raise Exception("Incorrect minified")

        user_agent = parse(self.user_agent_string)

        if self.minified:
            if user_agent.is_mobile:
                device_kind = 'Mobile'
            elif user_agent.is_pc:
                device_kind = 'PC'
            elif user_agent.is_tablet:
                device_kind = 'Tablet'
            else:
                device_kind = 'Unknow'

            return {'browser': {'family' : user_agent.browser.family, 'version': user_agent.browser.version_string}, 'os': {'family' : user_agent.os.family, 'version': user_agent.os.version_string}, 'device': {'brand': user_agent.device.brand,'family': user_agent.device.family, 'model': user_agent.device.model, 'kind': device_kind}}

        return user_agent

