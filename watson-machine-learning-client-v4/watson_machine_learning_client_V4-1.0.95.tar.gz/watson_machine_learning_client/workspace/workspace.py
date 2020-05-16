from watson_machine_learning_client import WatsonMachineLearningAPIClient
from watson_machine_learning_client.wml_client_error import MissingArgument


class WorkSpace:
    """
    WorkSpace class for WML authentication and project/space manipulation.

    Parameters
    ----------
    wml_credentials: dictionary, required
        Credentials to Watson Machine Learning instance.

    project_id: str, optional
        ID of the Watson Studio project.

    space_id: str, optional
        ID of the Watson Studio Space.

    Example
    -------
    >>> from watson_machine_learning_client.workspace import WorkSpace
    >>>
    >>> ws = WorkSpace(
    >>>        wml_credentials={
    >>>              "apikey": "...",
    >>>              "iam_apikey_description": "...",
    >>>              "iam_apikey_name": "...",
    >>>              "iam_role_crn": "...",
    >>>              "iam_serviceid_crn": "...",
    >>>              "instance_id": "...",
    >>>              "url": "https://us-south.ml.cloud.ibm.com"
    >>>            },
    >>>         project_id="...",
    >>>         space_id="...")
    """
    def __init__(self, wml_credentials: dict, project_id: str = None, space_id: str = None) -> None:
        self.wml_credentials = wml_credentials.copy()
        self.project_id = project_id
        self.space_id = space_id
        self.WMLS = False
        self.wml_client = WatsonMachineLearningAPIClient(wml_credentials=wml_credentials)

        if wml_credentials[u'instance_id'].lower() == 'wml_local':
            if self.space_id is None:
                raise MissingArgument(
                    'space_id',
                    reason="These credentials are from WML Server environment, "
                           "please specify the \"space_id\"")
            else:
                self.wml_client.set.default_space(self.space_id)
                self.WMLS = True

        if wml_credentials[u'instance_id'].lower() in ('icp', 'openshift'):
            if self.project_id is None or self.space_id is None:
                raise MissingArgument(
                    'project_id',
                    reason="These credentials are from CP4D environment, "
                           "please also specify \"project_id\" and \"space_id\"")
            else:
                self.wml_client.set.default_project(self.project_id)

