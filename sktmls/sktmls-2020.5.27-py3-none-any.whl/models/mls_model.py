import json
import os
import shlex
import shutil
import subprocess
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import lightgbm
import xgboost
from joblib import dump


MLS_MODEL_DIR = os.path.join(Path.home(), "mls_temp_dir")
MODEL_BINARY_NAME = "model.joblib"
MODEL_META_NAME = "model.json"
S3_DEFAULT_PATH = "s3a://mls-model-registry"

EDD_OPTIONS = """-Dfs.s3a.proxy.host=awsproxy.datalake.net \
                 -Dfs.s3a.proxy.port=3128 \
                 -Dfs.s3a.endpoint=s3.ap-northeast-2.amazonaws.com \
                 -Dfs.s3a.security.credential.provider.path=jceks:///user/tairflow/s3_mls.jceks \
                 -Dfs.s3a.fast.upload=true -Dfs.s3a.acl.default=BucketOwnerFullControl"""


class AWSENV(Enum):
    STG = "stg"
    PRD = "prd"
    DEV = "dev"


class MLSModelError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MLSModel(metaclass=ABCMeta):
    def __init__(self, model, model_name: str, model_version: str):
        assert type(model_name) == str
        assert type(model_version) == str

        if not bool(re.search("^[A-Za-z0-9_]+_model$", model_name)):
            raise MLSModelError(
                "model_name should follow naming rule. MUST be in alphabet, number, underscore and endwiths '_model'"
            )

        if not bool(re.search("^[A-Za-z0-9_]+$", model_version)):
            raise MLSModelError("model_name should follow naming rule. MUST be in alphabet, number, underscore")

        self.model = model
        self.model_name = model_name
        self.model_version = model_version

    def save(self, aws_env: AWSENV = AWSENV.STG.value, force: bool = False, edd: bool = False,) -> None:
        """
        Upload model_binary (model.joblib) and model_meta (model.json) to MLS model registry.

        Args:
            aws_env (str): AWS ENV
            force (bool): Force to overwrite model files on S3 if exists
            edd (bool): True if the model is uploaded from EDD
        """
        s3_path = S3_DEFAULT_PATH
        if aws_env in (AWSENV.STG.value, AWSENV.PRD.value):
            s3_path = f"{S3_DEFAULT_PATH}-{aws_env}"
        s3_path = f"{s3_path}/{self.model_name}/{self.model_version}"

        model_meta = {
            "name": self.model_name,
            "version": self.model_version,
            "model_lib": self.model_lib,
            "model_lib_version": self.model_lib_version,
            "model_data": f"{s3_path}/{MODEL_BINARY_NAME}",
            "features": self.features,
        }

        model_path = os.path.join(
            MLS_MODEL_DIR,
            f"{aws_env}_{self.model_name}_{self.model_version}_{datetime.today().strftime('%Y%m%d_%H%M%S')}",
        )
        model_binary_path = os.path.join(model_path, MODEL_BINARY_NAME)
        model_meta_path = os.path.join(model_path, MODEL_META_NAME)

        try:
            if not os.path.exists(model_binary_path):
                if not os.path.exists(model_path):
                    os.makedirs(model_path)
                dump(self.model, model_binary_path)
                with open(model_meta_path, "w") as f:
                    json.dump(model_meta, f)
            else:
                raise MLSModelError(f"{self.model_name} / {self.model_version} is already in PATH ({model_path})")

            cmd_mkdir = f"hdfs dfs {EDD_OPTIONS if edd else ''} -mkdir -p {s3_path}"
            cmd_load_model_to_s3 = (
                f"hdfs dfs {EDD_OPTIONS if edd else ''} -put {'-f' if force else ''} {model_binary_path} {s3_path}"
            )
            cmd_load_meta_to_s3 = (
                f"hdfs dfs {EDD_OPTIONS if edd else ''} -put {'-f' if force else ''} {model_meta_path} {s3_path}"
            )

            process_mkdir = subprocess.Popen(shlex.split(cmd_mkdir), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            process_mkdir.wait()
            if process_mkdir.returncode != 0:
                raise MLSModelError(f"Making Directory on S3 ({s3_path}) is FAILED")

            process_model_binary = subprocess.Popen(
                shlex.split(cmd_load_model_to_s3), stdout=subprocess.PIPE, stdin=subprocess.PIPE
            )
            process_model_binary.wait()
            if process_model_binary.returncode != 0:
                raise MLSModelError(
                    f"Load model_binary(model.joblib) to S3 ({s3_path}) is FAILED. (Maybe Already exists on S3)"
                )

            process_model_meta = subprocess.Popen(
                shlex.split(cmd_load_meta_to_s3), stdout=subprocess.PIPE, stdin=subprocess.PIPE
            )
            process_model_meta.wait()
            if process_model_meta.returncode != 0:
                raise MLSModelError(f"Load model_meta(meta.json) to S3 ({s3_path}) is FAILED")
        except MLSModelError as e:
            print("MLSModelError", e)
        finally:
            shutil.rmtree(model_path, ignore_errors=True)

    @abstractmethod
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        pass


class MLSLightGBMModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str):
        super().__init__(model, model_name, model_version)
        self.model_lib = "lightgbm"
        self.model_lib_version = lightgbm.__version__
        self.features = self.model.feature_name()


class MLSXGBoostModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model, model_name, model_version)
        self.model_lib = "xgboost"
        self.model_lib_version = xgboost.__version__

        try:
            if (
                all(isinstance(s, str) for s in features)
                and len(features) == len(self.model.feature_importances_)
                and type(features) == list
            ):
                self.features = features
            else:
                raise MLSModelError(
                    "Input feature list is not matching the number of model input feature or list STRING type"
                )
        except MLSModelError as e:
            print("MLSModelError", e)
