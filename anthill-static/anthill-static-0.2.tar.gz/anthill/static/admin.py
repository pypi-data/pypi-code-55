
import anthill.common.admin as a

from . model.deploy import DeploymentMethods, DeploymentModel
from . model.settings import SettingsError, NoSuchSettingsError


class RootAdminController(a.AdminController):
    def render(self, data):
        return [
            a.breadcrumbs([], "File Hosting"),
            a.links("Navigate", [
                a.link("settings", "Deployment Settings", icon="cog")
            ])
        ]

    def access_scopes(self):
        return ["static_admin"]


class SettingsController(a.AdminController):
    async def get(self):

        try:
            settings = await self.application.deployment_settings.get_settings(self.gamespace)
        except NoSuchSettingsError:
            deployment_method = ""
            deployment_data = {}
        except SettingsError as e:
            raise a.ActionError(e.message)
        else:
            deployment_method = settings.deployment_method
            deployment_data = settings.deployment_data

        deployment_methods = {t: t for t in DeploymentMethods.types()}

        if not deployment_method:
            deployment_methods[""] = "< SELECT >"

        result = {
            "deployment_methods": deployment_methods,
            "deployment_method": deployment_method,
            "deployment_data": deployment_data
        }

        return result

    async def update_deployment_method(self, deployment_method):

        if not DeploymentMethods.valid(deployment_method):
            raise a.ActionError("Not a valid deployment method")

        try:
            stt = await self.application.deployment_settings.get_settings(self.gamespace)
        except NoSuchSettingsError:
            deployment_data = {}
        else:
            deployment_data = stt.deployment_data

        try:
            await self.application.deployment_settings.update_settings(
                self.gamespace, deployment_method, deployment_data)
        except SettingsError as e:
            raise a.ActionError(e.message)

        raise a.Redirect("settings", message="Deployment method has been updated")

    async def update_deployment(self, **kwargs):

        try:
            settings = await self.application.deployment_settings.get_settings(self.gamespace)
        except NoSuchSettingsError:
            raise a.ActionError("Please select deployment method first")
        except SettingsError as e:
            raise a.ActionError(e.message)
        else:
            deployment_method = settings.deployment_method
            deployment_data = settings.deployment_data

        m = DeploymentMethods.get(deployment_method)()

        m.load(deployment_data)
        await m.update(**kwargs)

        try:
            await self.application.deployment_settings.update_settings(
                self.gamespace, deployment_method, m.dump())
        except SettingsError as e:
            raise a.ActionError(e.message)

        raise a.Redirect("settings", message="Deployment settings have been updated")

    def render(self, data):

        r = [
            a.breadcrumbs([
                a.link("index", "File Hosting"),
            ], "Settings"),
            a.form("Deployment method", fields={
                "deployment_method": a.field(
                    "Deployment method", "select", "primary", "non-empty", values=data["deployment_methods"]
                )
            }, methods={
                "update_deployment_method": a.method("Switch deployment method", "primary")
            }, data=data)
        ]

        deployment_method = data["deployment_method"]
        deployment_data = data["deployment_data"]

        if deployment_method:
            m = DeploymentMethods.get(deployment_method)
            if m.has_admin():
                r.append(a.form("Update deployment", fields=m.render(a), methods={
                    "update_deployment": a.method("Update", "primary")
                }, data=deployment_data))
        else:
            r.append(a.notice(
                "Please select deployment method",
                """
                    Players cannot upload files until the deployment is configured
                """))

        r.extend([
            a.links("Navigate", [
                a.link("index", "Back", icon="chevron-left"),
            ])
        ])

        return r

    def access_scopes(self):
        return ["static_admin"]
