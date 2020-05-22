from ehelply_bootstrapper.utils.environment import Environment


def _get_environment_name() -> str:
    environment_name: str = Environment.stage()
    if environment_name == "dev":
        environment_name = "test"
    return environment_name


def secret_name_database():
    return "ehelply-{environment}.db-rds.ehelply-{environment}-main.ehelply-secure-microservice".format(
        environment=_get_environment_name())


def secret_name_facts_vault():
    return "ehelply-{environment}.microservices.ehelply-facts.vault".format(environment=_get_environment_name())


def secret_name_security_vault():
    return "ehelply-{environment}.microservices.ehelply-security.vault".format(environment=_get_environment_name())


def secret_name_updater_vault():
    return "ehelply-all.microservices.ehelply-updater.vault".format(environment=_get_environment_name())
