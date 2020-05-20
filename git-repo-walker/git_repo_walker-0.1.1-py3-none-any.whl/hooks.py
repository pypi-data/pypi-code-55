#  Copyright (c) 2020. Daniel Elsner.
import logging
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from time import time
from typing import Optional, List, Dict

import pandas as pd
from git import Repo, InvalidGitRepositoryError


class Hook(ABC):
    """
    Hook interface for execution inside walker.
    """

    @abstractmethod
    def run(self: "Hook"):
        pass


class PrintAddedOrChangedFilesHook(Hook):

    def __init__(self, repository_path: str) -> None:
        self.repo: Optional[Repo] = None
        try:
            self.repo = Repo(repository_path)
        except InvalidGitRepositoryError as e:
            raise InvalidGitRepositoryError(f"{str(e)} is not a git repository")

    def run(self: "PrintAddedOrChangedFilesHook"):
        # include all untracked files
        files = self.repo.git.ls_files(others=True,
                                       exclude_standard=True).splitlines()

        # include all changed files
        files += self.repo.git.diff(name_only=True).splitlines()

        # filter out only non-cache files
        files = list(filter(lambda f: ".starts-walker" not in f and
                                      ".starts" not in f and
                                      "jdeps-cache" not in f, files))

        # log touched files
        logging.debug(f"Touched files: {files}")


class STARTSHook(Hook):

    def __init__(self: "STARTSHook",
                 repository_path: str) -> None:
        self.repository_path = repository_path

    def _update_pom(self: "STARTSHook"):
        """
        Adjust `pom.xml` to contain STARTS maven plugin.

        :return:
        """
        filename = "pom.xml"
        filepath = os.path.join(self.repository_path, filename)

        if os.path.isfile(filepath):

            def _namespace(el: ET.Element):
                m = re.match(r'\{.*\}', el.tag)
                return m.group(0)[1:-1] if m else ''

            # get ns from xml
            tree = ET.parse(filepath)
            ns = _namespace(tree.getroot())
            # set default namespace
            ET.register_namespace("", ns)
            # re-parse xml
            tree = ET.parse(filepath)
            root = tree.getroot()

            # search for child node in element
            def _search_node(el: ET.Element, node: str):
                searched_node = None
                for child in el:
                    tag = child.tag
                    if "{" in tag:
                        _, _, tag = tag.rpartition("}")
                    if tag == node:
                        searched_node = child
                        break
                return searched_node

            build_node = _search_node(root, "build")
            plugins_node = _search_node(build_node, "plugins")

            # append maven plugin
            plugin = ET.Element("plugin")
            group = ET.Element("groupId")
            group.text = "org.apache.maven.plugins"
            plugin.append(group)
            artifact = ET.Element("artifactId")
            artifact.text = "maven-surefire-plugin"
            plugin.append(artifact)
            version = ET.Element("version")
            version.text = "2.19.1"
            plugin.append(version)
            plugins_node.append(plugin)

            # write back to file
            tree.write(filepath)

    def _run_starts(self: "STARTSHook"):
        """
        Run STARTS tool.

        :return:
        """
        # keep track of current working directory
        tmp_path = os.getcwd()

        # navigate into repo
        os.chdir(self.repository_path)

        # prepare cache dir/file
        cache_dir = ".starts-walker"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)  # recursively create dirs
        cache_file = f"run_{int(time() * 1000)}.log"  # run identified by timestamp
        cache_file_path = os.path.join(os.getcwd(), cache_dir, cache_file)

        # run mvn proc and store result into log file
        with open(cache_file_path, "wb") as log_file:
            p = subprocess.Popen(["mvn",
                                  "edu.illinois:starts-maven-plugin:1.3:starts"],
                                 stdout=log_file)
            p.wait()

        # return to previous directory
        os.chdir(tmp_path)

    def run(self: "STARTSHook"):
        self._update_pom()
        self._run_starts()


class STARTSPostEvaluationHook(Hook):
    def __init__(self: "STARTSPostEvaluationHook",
                 repository_path: str,
                 output_path: Optional[str]) -> None:
        self.repository_path = repository_path
        self.output_path = output_path

    def run(self: "STARTSPostEvaluationHook"):
        """
        Run evaluation on STARTS execution cache.

        :return:
        """
        # keep track of current working directory
        tmp_path = os.getcwd()

        # navigate into repo
        os.chdir(self.repository_path)

        # check for cache dir
        cache_dir = ".starts-walker"
        if os.path.exists(cache_dir):
            # iterate over files in cache
            starts_results: List[Dict] = []
            for file in sorted(os.listdir(cache_dir)):
                with open(os.path.join(os.getcwd(), cache_dir, file), "r") as f:
                    content = f.read()
                    affected_tests = re.findall("STARTS:AffectedTests: (\d+)", content)
                    affected_tests = int(affected_tests[0]) if len(affected_tests) > 0 else None
                    total_tests = re.findall("STARTS:TotalTests: (\d+)", content)
                    total_tests = int(total_tests[0]) if len(total_tests) > 0 else None
                    starts_results.append({
                        "id": file.split(".log")[0],
                        "affected_tests": affected_tests,
                        "total_tests": total_tests
                    })
            df = pd.DataFrame(starts_results)
            df = df.set_index("id")
            p = df.plot()
            fig = p.get_figure()
            outpath = tmp_path
            if self.output_path is not None:
                outpath = self.output_path
            fig.savefig(os.path.join(outpath, "plot.png"))
        # return to previous directory
        os.chdir(tmp_path)
