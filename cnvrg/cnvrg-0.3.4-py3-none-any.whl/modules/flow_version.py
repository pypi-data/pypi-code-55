from cnvrg.helpers.apis_helper import post as apis_post, get as apis_get, credentials
from cnvrg.modules.cnvrg_files import CnvrgFiles
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.config_helper as config_helper
import cnvrg.helpers.env_helper as env_helper
import cnvrg.helpers.args_helper as args_helper
import cnvrg.helpers.param_build_helper as param_build_helper
from cnvrg.helpers.url_builder_helper import url_join
import cnvrg.helpers.spawn_helper as spawn_helper
from cnvrg.helpers.error_catcher import suppress_exception
import cnvrg.helpers.apis_helper as apis_helper
import json
from cnvrg.modules.cnvrg_job import CnvrgJob
from cnvrg.modules.project import Project
import cnvrg.helpers.string_helper as string_helper
import cnvrg.helpers.param_build_helper as param_build_helper
from cnvrg.helpers.env_helper import CURRENT_JOB_TYPE, CURRENT_JOB_ID, ENDPOINT, POOL_SIZE
from cnvrg.modules.errors import UserError
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.helpers.error_catcher import suppress_exception
import cnvrg.helpers.parallel_helper as parallel_helper
import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.modules.errors as errors
from cnvrg.modules.dataset import Dataset
from cnvrg.modules.errors import CnvrgError
import yaml


class FlowVersion():
    def __init__(self, title=None, flow=None, project=None):
        if not title:
            raise UserError("Cant create an flow version without title")

        if not flow:
            raise UserError("Cant create an flow version without flow")

        owner, project_slug, title = param_build_helper.parse_params(title, param_build_helper.FLOW)
        if isinstance(project, str):
            p = Project(url_join(owner, project))
        elif isinstance(project, Project):
            p = project
        elif project is None:
            p = Project(url_join(owner, project_slug))

        self.title = title
        self.owner = owner
        self.flow = flow
        self.project = p

    def info(self):
        resp = apis_helper.get(
            url_join(self.project.get_base_url(), 'flows', self.flow.slug, "flow_versions", self.title, "info"))
        return resp.get("fv_status")
