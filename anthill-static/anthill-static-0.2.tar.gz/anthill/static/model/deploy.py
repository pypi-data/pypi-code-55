
from anthill.common.model import Model
from anthill.common.validate import validate
from anthill.common.deployment import DeploymentError, DeploymentMethods

from . settings import NoSuchSettingsError, SettingsError

import os


class DeploymentModel(Model):
    def __init__(self, settings):
        self.settings = settings

    @validate(gamespace_id="int", account_id="int", file_path="str", file_name="str")
    async def deploy(self, gamespace_id, account_id, file_path, file_name):

        try:
            settings = await self.settings.get_settings(gamespace_id)
        except NoSuchSettingsError:
            raise DeploymentError("Please select deployment method first (in settings)")
        except SettingsError as e:
            raise DeploymentError(e.message)

        m = DeploymentMethods.get(settings.deployment_method)()
        m.load(settings.deployment_data)

        url = await m.deploy(gamespace_id, file_path, str(account_id), file_name)

        return url
