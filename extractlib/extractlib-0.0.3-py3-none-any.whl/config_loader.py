import os
import yaml


class ConfigException(Exception):
    pass


class ConfigLoader(object):
    """Class for loading sensitive config variables, either from a YAML file if available, or from 
        shell environnment variables
    """

    common_vars = {
        "user_pk": 1,
        "upload_bucket": "adaptive-data-lake",
        "spark_driver_cores": 1,
        "spark_driver_memory": "2G",
        "spark_executor_cores": 2,
        "spark_executor_memory": "4G",
        "spark_num_executors": 2,
        "spark_queue": "default",
    }

    staging_vars = {
        "env_code": "staging",
        "jar_file": "s3n://adaptive-mgmt/code/adm/staging/jobs-assembly-latest.jar",
        "oasis_url": "http://st-oasis.dm",
        "start_spark_url": "http://elb.st-oasis.dm/orchestrator/api/v1/messages/run_spark_messages/",
    }

    prod_vars = {
        "env_code": "prod",
        "jar_file": "s3n://adaptive-mgmt/code/adm/prod/jobs-assembly-latest.jar",
        "oasis_url": "http://oasis.dm",
        "start_spark_url": "http://elb.oasis.dm/orchestrator/api/v1/messages/run_spark_messages/",
    }

    @classmethod
    def get_config(cls, env):
        cfg = {}
        cfg.update(cls.common_vars)
        if env == "staging":
            cfg.update(cls.staging_vars)
        elif env == "production":
            cfg.update(cls.prod_vars)
        else:
            raise ValueError

        if "config.yml" in os.listdir():
            with open("config.yml", "r") as ymlfile:
                cfg.update(yaml.load(ymlfile)[env])
        elif os.getenv("auth_token") is not None:
            cfg.update(os.environ)
        else:
            raise ConfigException("Nowhere from which to load configs.")

        return cfg
