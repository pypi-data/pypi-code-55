import os

CURRENT_DIR = os.path.dirname(__file__)
TEMPLATES_PATH = os.path.join(CURRENT_DIR, "templates")

# Schema paths
SCHEMA_FOLDER = os.path.join(CURRENT_DIR, "schema")
YAML_CONFIG_SCHEMA_PATH = os.path.join(SCHEMA_FOLDER, "config_schema.yaml")
YAML_SECRETS_SCHEMA_PATH = os.path.join(SCHEMA_FOLDER, "secrets_schema.yaml")

# Config paths
YAML_CONFIG_PATH = "config.yaml"
YAML_SECRETS_PATH = "secrets.yaml"

# Databricks paths
DATABRICKS_TEMPLATE_PATH = os.path.join(TEMPLATES_PATH, "databricks" + os.sep)
DATABRICKS_PATH = "databricks" + os.sep
notebooks_to_copy = [
    (
        os.path.join(DATABRICKS_TEMPLATE_PATH, "setup", "setup-environment-template.py"),
        os.path.join(DATABRICKS_PATH, "setup", "setup-environment.py"),
    ),
    (
        os.path.join(DATABRICKS_TEMPLATE_PATH, "setup", "basemodel-template.py"),
        os.path.join(DATABRICKS_PATH, "setup", "basemodel.py"),
    ),
    (
        os.path.join(DATABRICKS_TEMPLATE_PATH, "jobs", "powerbi-dataset-refresh-template.py"),
        os.path.join(DATABRICKS_PATH, "jobs", "powerbi-dataset-refresh.py"),
    ),
    (
        os.path.join(DATABRICKS_TEMPLATE_PATH, "notebooks", "sample-spark-model-template.py"),
        os.path.join(DATABRICKS_PATH, "notebooks", "sample-spark-model.py"),
    ),
]

# Power BI paths
POWERBI_TEMPLATE_PATH = os.path.join(TEMPLATES_PATH, "powerbi" + os.sep)
POWERBI_PATH = "powerbi" + os.sep
POWERBI_BASE_DATASET_PATH = os.path.join(POWERBI_PATH, "datasets", "base_dataset.pbix")
POWERBI_BASE_REPORT_PATH = os.path.join(POWERBI_PATH, "reports", "base_report.pbix")

# Github Actions paths
SCRIPT_TEMPLATE_FOLDER = os.path.join(TEMPLATES_PATH, "infra_scripts")
POWERBI_SCRIPT_NAME = "deploy_powerbi.py"
DATABRICKS_SCRIPT_NAME = "deploy_databricks.py"
POWERBI_SCRIPT_PATH = os.path.join(SCRIPT_TEMPLATE_FOLDER, POWERBI_SCRIPT_NAME)
DATABRICKS_SCRIPT_PATH = os.path.join(SCRIPT_TEMPLATE_FOLDER, DATABRICKS_SCRIPT_NAME)

WORKFLOW_TEMPLATE_FOLDER = os.path.join(TEMPLATES_PATH, "github_workflows")
POWERBI_WORKFLOW_TEMPLATE_NAME = "deploy_powerbi.yaml"
DATABRICKS_WORKFLOW_TEMPLATE_NAME = "deploy_databricks.yaml"
POWERBI_WORKFLOW_TEMPLATE_PATH = os.path.join(WORKFLOW_TEMPLATE_FOLDER, POWERBI_WORKFLOW_TEMPLATE_NAME)
DATABRICKS_WORKFLOW_TEMPLATE_PATH = os.path.join(WORKFLOW_TEMPLATE_FOLDER, DATABRICKS_WORKFLOW_TEMPLATE_NAME)

SCRIPT_OUTPUT_FOLDER = "pipeline_scripts"
POWERBI_SCRIPT_OUTPUT_PATH = os.path.join(SCRIPT_OUTPUT_FOLDER, POWERBI_SCRIPT_NAME)
DATABRICKS_SCRIPT_OUTPUT_PATH = os.path.join(SCRIPT_OUTPUT_FOLDER, DATABRICKS_SCRIPT_NAME)

WORKFLOW_OUTPUT_FOLDER = os.path.join(".github", "workflows")
POWERBI_WORFKLOW_OUTPUT_PATH = os.path.join(WORKFLOW_OUTPUT_FOLDER, POWERBI_WORKFLOW_TEMPLATE_NAME)
DATABRICKS_WORFKLOW_OUTPUT_PATH = os.path.join(WORKFLOW_OUTPUT_FOLDER, DATABRICKS_WORKFLOW_TEMPLATE_NAME)
