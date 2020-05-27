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
from cnvrg.modules.flow_version import FlowVersion
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


class Flow():
    def __init__(self, slug=None, project=None, version=None):
        owner, project_slug, slug = param_build_helper.parse_params(slug, param_build_helper.FLOW)
        if isinstance(project, str):
            p = Project(url_join(owner, project))
        elif isinstance(project, Project):
            p = project
        elif project is None:
            p = Project(url_join(owner, project_slug))

        if not slug:
            raise UserError("Cant create an flow without slug")
        self.slug = slug
        self.version = version or "latest"
        self.owner = owner
        self.project = p

    def run(self):
        project = self.project
        resp = apis_helper.post(url_join(project.get_base_url(), 'flows', 'run_flow'), data={"flow_slug": self.slug})
        status = resp.get("status")
        if status == 200:
            fv_title = resp.get("flow_version").get("title")
            return FlowVersion(fv_title, self, project)
        else:
            raise CnvrgError("Could not create flow")

    @staticmethod
    @suppress_exception
    def create(file=None, yaml_content=None, project=None):
        if not file and not yaml_content:
            raise errors.CnvrgError("File or yaml is missing")

        project = project or Project()

        if yaml_content:
            data = yaml.safe_load(yaml_content)
        else:
            with open(file, 'r') as f:
                data = yaml.safe_load(f)
            if not data:
                raise errors.CnvrgError("File can't be empty")

        resp = apis_helper.post(url_join(project.get_base_url(), 'flows'), data={"flow_version": json.dumps(data)})
        status = resp.get("status")
        if status == 200:
            flow_title = resp.get("flow").get("title")
            print("Flow {} created successfully".format(flow_title))
            flow_slug = resp.get("flow").get("slug")
            return Flow(flow_slug, project)
        else:
            raise CnvrgError("Could not create flow")
