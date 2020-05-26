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
from cnvrg.modules.file_uploader import FileUploader
import os
import json
import hashlib
import mimetypes
from pathlib import Path


class Project(CnvrgFiles):
    def __init__(self, project=None, project_url=None, working_dir=None):
        if project_url:
            owner_slug, project_slug = Project.get_owner_and_project_from_url(project_url)
        else:
            owner_slug, project_slug = param_build_helper.parse_params(project, param_build_helper.PROJECT, working_dir=working_dir)
        self.__owner = owner_slug or credentials.owner
        self.__project = project_slug

        in_dir = config_helper.is_in_dir(config_helper.CONFIG_TYPE_PROJECT, project_slug, working_dir)
        super(Project, self).__init__(in_dir=in_dir)
        if in_dir:
            self._set_working_dir(config_helper.find_config_dir(path=working_dir))
            self.in_dir = True
        elif not self.__project or not self.__owner:
            raise CnvrgError("Cant init project without params and outside project directory")

    def __fetch_config(self):
        resp = apis_get(self.get_base_url())
        return {"slug": self.slug, "owner": self.owner, **resp.get("result")}

    def is_git(self):
        resp = apis_get(url_join(self.get_base_url(), 'get_project'))
        if not resp.get("result"):
            return False
        result = json.loads(resp.get("result"))
        return result.get("git")

    def put_files(self, files=None, message="SDK Commit", depth=False, files_path=None, num_processes=10, num_threads=30):
        commit_sha1 = self.start_commit_new(message=message)

        full_paths = []
        for file in files:
            trees = Project.get_recursive_tree(file, depth)
            full_paths += trees
            full_paths.append(file)

        full_paths_set = set(full_paths)
        unique_full_paths = list(full_paths_set)

        try:
            unique_full_paths.remove("./")
            unique_full_paths.remove(".")
            unique_full_paths.remove("/")
            unique_full_paths.remove("//")
        except ValueError as e:
            pass

        fu = FileUploader(self)
        # upload_multiple_files(self, files=None, files_path=None, num_processes=10, num_threads=30):
        fu.upload_multiple_files(files=unique_full_paths, commit_sha1=commit_sha1)
        self.end_commit_new(commit_sha1=commit_sha1)
        return True

    def start_commit_new(self, message="SDK Commit"):
        owner = self.owner
        resp = apis_helper.post_v2(url_join(owner, "files", "start_commit"), data={
            "fileable_type": "Project",
            "fileable_slug": self.slug,
            "message": message
        })
        return resp.json().get("result").get("commit_sha1")

    def create_blob_versions(self, commit_sha1, full_paths):
        owner = self.owner
        files = {}
        for path in full_paths:
            is_file = os.path.isfile(path)
            is_directory = os.path.isdir(path)

            if is_file:
                content_type = mimetypes.guess_type(path, strict=True)
                files.update({
                    path: {
                        "absolute_path": "{}/".format(url_join(os.getcwd(), path)),
                        "content_type": content_type[0] or "plain/text",
                        "file_name": os.path.basename(path),
                        "file_size": os.path.getsize(path),
                        "relative_path": path,
                        "sha1": Project.sha1(path)
                    }
                })
            elif is_directory:
                files.update({
                    path: {
                        "absolute_path": "{}/".format(url_join(os.getcwd(), path)),
                        "relative_path": path
                    }
                })

        resp = apis_helper.post_v2(url_join(owner, "files", "create_blob_versions"), data={
            "fileable_type": "Project",
            "fileable_slug": self.slug,
            "commit": commit_sha1,
            "files": json.dumps(files)
        })

        return resp.json().get("result")

    def connect_blob_versions_to_commit(self, blob_ids, commit_sha1):
        owner = self.owner
        resp = apis_helper.post_v2(url_join(owner, "files", "connect_blob_versions_to_commit"), data={
            "fileable_type": "Project",
            "fileable_slug": self.slug,
            "commit": commit_sha1,
            "blob_ids": blob_ids
        })
        # print(resp.json())
        return resp.json()

    def end_commit_new(self, commit_sha1):
        owner = self.owner
        resp = apis_helper.post_v2(url_join(owner, "files", "end_commit"), data={
            "fileable_type": "Project",
            "fileable_slug": self.slug,
            "commit": commit_sha1
        })
        # print(resp.json())
        return resp.json()

    @staticmethod
    def get_recursive_tree(path, depth):
        trees = []
        if path.startswith("/"):
            if depth:
                while str(path) != "/":
                    tmp_path = Path(path)
                    tmp_parent = tmp_path.parent
                    trees.append("{}/".format(str(tmp_parent)))
                    path = tmp_parent
            else:
                tree = path.split("/")[-1]
                trees.append(tree)
        else:
            while str(path) != ".":
                tmp_path = Path(path)
                tmp_parent = tmp_path.parent
                trees.append("{}/".format(str(tmp_parent)))
                path = tmp_parent

        return trees

    @staticmethod
    @suppress_exception
    def list(owner=None):
        owner_slug = owner or credentials.owner
        projects = []
        resp = apis_helper.get_v2(url_join(owner_slug, "projects"))
        for slug in resp.json():
            projects.append(Project(slug))
        return projects

    @staticmethod
    @suppress_exception
    def create(title, owner=None):
        owner_slug = owner or credentials.owner
        resp = apis_helper.post_v2(url_join(owner_slug, "projects"), data={"title": title})
        status = resp.json().get("status")
        if status == 200:
            slug = resp.json().get("project_slug")
            print("Project {} created successfully".format(slug))
            return Project(slug)
        else:
            raise CnvrgError("Could not create project")

    @staticmethod
    def sha1(full_path):
        BUF_SIZE = 65536
        sha1 = hashlib.sha1()

        with open(full_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)

        return sha1.hexdigest()

    @property
    def owner(self):
        return self.__owner

    @property
    def slug(self):
        return self.__project

    @property
    def git(self):
        config = self.get_config()
        if config:
            return config.get(":git") or False
        return self.__fetch_config().get("git")

    def get_git_commit(self):
        return spawn_helper.run_and_get_output("git rev-parse --verify HEAD")

    def get_git_branch(self):
        return spawn_helper.run_and_get_output("git rev-parse --abbrev-ref HEAD")

    def get_base_url(self, api="v1"):
        if api == "v1":
            return "users/{owner}/projects/{project}".format(owner=self.__owner, project=self.__project)
        else:
            return "{owner}/projects/{project}".format(owner=self.__owner, project=self.__project)

    def _default_config(self):
        return {
            "project": self.__project,
            "owner": self.__owner,
            "commit": None
        }

    def web_url(self):
        return url_join(credentials.web_url(), self.__owner, 'projects', self.__project)

    def get_project_name(self):
        return self.__project

    def get_output_dir(self):
        return self.get_working_dir()

    def run_task(self, cmd, **kwargs):
        #if "grid" in kwargs: kwargs["grid"] = hyper_search_helper.load_hyper_search(kwargs["grid"])
        kwargs = {**env_helper.get_origin_job(), **kwargs}
        resp = apis_post(url_join(self.get_base_url(), "experiments"), data={"cmd": cmd, **kwargs})
        hyper_search = resp.get("hyper_search")
        if not hyper_search:
            error_msg = resp.get("error") or "Can't run experiment"
            raise CnvrgError(error_msg)
        return hyper_search


    def sync(self, **options):
        command = "cnvrg sync {args}".format(args=args_helper.args_to_string(options))
        spawn_helper.run_sync(command, print_output=True)