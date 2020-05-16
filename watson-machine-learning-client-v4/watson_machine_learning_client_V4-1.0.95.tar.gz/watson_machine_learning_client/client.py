################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from watson_machine_learning_client.utils.log_util import get_logger
from watson_machine_learning_client.utils import version

#from watson_machine_learning_client.learning_system import LearningSystem
from watson_machine_learning_client.experiments import Experiments
from watson_machine_learning_client.repository import Repository
from watson_machine_learning_client.model_definition import ModelDefinition
from watson_machine_learning_client.models import Models
from watson_machine_learning_client.pipelines import Pipelines
from watson_machine_learning_client.instance import ServiceInstance
from watson_machine_learning_client.deployments import Deployments
from watson_machine_learning_client.training import Training
from watson_machine_learning_client.runtimes import Runtimes
from watson_machine_learning_client.functions import Functions
from watson_machine_learning_client.spaces import Spaces
from watson_machine_learning_client.assets import Assets
from watson_machine_learning_client.connections import Connections
from watson_machine_learning_client.Set import Set
from watson_machine_learning_client.sw_spec import SwSpec
from watson_machine_learning_client.hw_spec import HwSpec
from watson_machine_learning_client.pkg_extn import PkgExtn
from watson_machine_learning_client.shiny import Shiny
from watson_machine_learning_client.script import Script
from watson_machine_learning_client.wml_client_error import NoWMLCredentialsProvided
from watson_machine_learning_client.wml_client_error import WMLClientError

import copy
import os

'''
.. module:: WatsonMachineLearningAPIClient
   :platform: Unix, Windows
   :synopsis: Watson Machine Learning API Client.

.. moduleauthor:: IBM
'''


class WatsonMachineLearningAPIClient:

    def __init__(self, wml_credentials, project_id=None):
        self._logger = get_logger(__name__)
        self.wml_credentials = copy.deepcopy(wml_credentials)
        self.CAMS = None
        self.WSD = None
        self.ICP_30 = None
        self.ICP = None
        self.default_space_id = None
        self.default_project_id = None

        os.environ['WSD_PLATFORM'] = 'False'
        if wml_credentials is None:
            raise NoWMLCredentialsProvided()
        if self.wml_credentials['url'][-1] == "/":
            self.wml_credentials['url'] = self.wml_credentials['url'].rstrip('/')
        if 'icp' == wml_credentials[u'instance_id'].lower() or 'openshift' == wml_credentials[u'instance_id'].lower() or 'wml_local' == wml_credentials[u'instance_id'].lower():
            self.ICP = True
            os.environ["DEPLOYMENT_PLATFORM"] = "private"
            ##Condition for CAMS related changes to take effect (Might change)
            if 'version' in wml_credentials.keys() and ('2.0.1' == wml_credentials[u'version'].lower() or '2.5.0' == wml_credentials[u'version'].lower() or
                                                        '3.0.0' == wml_credentials[u'version'].lower() or
                                                        '1.1' == wml_credentials[u'version'].lower()):
                self.CAMS = True
                os.environ["DEPLOYMENT_PRIVATE"] = "icp4d"
                if 'wml_local' == wml_credentials[u'instance_id'].lower() and '1.1' == wml_credentials[u'version'].lower():
                    url_port = wml_credentials[u'url'].split(':')[-1]
                    if not url_port.isdigit():
                        raise WMLClientError("It is mandatory to have port number as part of url for wml_local.")
                if '3.0.0' == wml_credentials[u'version'].lower():
                    self.ICP_30 = True
            else:
                self.CAMS = False
        else:
            if ('wsd_local' == wml_credentials[u'instance_id'].lower()) and ('1.1' == wml_credentials[u'version'].lower()):
                self.WSD = True
                os.environ['WSD_PLATFORM'] = 'True'
            else:
                self.ICP = False
                self.CAMS = False
        if "token" in wml_credentials:
            self.proceed = True
        else:
            self.proceed = False
        self.project_id = project_id
        self.wml_token = None
       # if not self.ICP and not self.ICP_30 and not self.WSD:
        if not self.WSD:
            self.service_instance = ServiceInstance(self)
            self.service_instance.details = self.service_instance.get_details()

        ##Initialize Assets and Model_Definitions only for CAMS
        if self.CAMS or self.WSD:
            self.set = Set(self)
            self.data_assets = Assets(self)
            self.model_definitions = ModelDefinition(self)
            if self.ICP_30:
                self.connections = Connections(self)
                self.software_specifications = SwSpec(self)
                self.hardware_specifications = HwSpec(self)
                self.package_extensions = PkgExtn(self)
                self.shiny = Shiny(self)
                self.script = Script(self)
        #    self.learning_system = LearningSystem(self)
        self.repository = Repository(self)
        self._models = Models(self)
        self.pipelines = Pipelines(self)
        self._functions = Functions(self)
        if not self.WSD:
            self.runtimes = Runtimes(self)
            self.deployments = Deployments(self)
            self.training = Training(self)
            self.spaces = Spaces(self)
            self.experiments = Experiments(self)
            self.connections = Connections(self)


        self._logger.info(u'Client successfully initialized')
        self.version = version()

    def _check_if_either_is_set(self):
        if self.CAMS:
            if self.default_space_id is None and self.default_project_id is None:
                raise WMLClientError("It is mandatory to set the space/project id. Use client.set.default_space(<SPACE_UID>)/client.set.default_project(<PROJECT_UID>) to proceed.")

    def _check_if_space_is_set(self):
        if self.CAMS:
            if self.default_space_id is None:
                raise WMLClientError("It is mandatory to set the space. Use client.set.default_space(<SPACE_UID>) to proceed.")

    def _params(self):
        params = {}
        if self.CAMS:
            if self.default_space_id is not None:
                params.update({'space_id': self.default_space_id})
            elif self.default_project_id is not None:
                params.update({'project_id': self.default_project_id})
            else:
                raise WMLClientError("It is mandatory to set the space/project id. Use client.set.default_space(<SPACE_UID>)/client.set.default_project(<PROJECT_UID>) to proceed.")

        if self.WSD:
            if self.default_project_id is not None:
                params.update({'project_id': self.default_project_id})
            else:
                raise WMLClientError(
                    "It is mandatory to set the project id. Use client.set.default_project(<PROJECT_UID>) to proceed.")
        return params

    def _get_headers(self, content_type='application/json', no_content_type=False):
        if self.WSD:
                headers = {'X-WML-User-Client': 'PythonClient'}
                if self.project_id is not None:
                    headers.update({'X-Watson-Project-ID': self.project_id})
                if not no_content_type:
                    headers.update({'Content-Type': content_type})
        else:
            if self.proceed is True:
                token = "Bearer "+ self.wml_credentials["token"]
            else:
                token = "Bearer " + self.service_instance._get_token()
            headers = {
                'Authorization': token,
                'X-WML-User-Client': 'PythonClient'
            }
            if self._is_IAM() or (self.service_instance._is_iam() is None):
                headers['ML-Instance-ID'] = self.wml_credentials['instance_id']

            headers.update({'x-wml-internal-switch-to-new-v4': "true"})
            if not self.ICP:
                #headers.update({'x-wml-internal-switch-to-new-v4': "true"})
                if self.project_id is not None:
                    headers.update({'X-Watson-Project-ID': self.project_id})

            if not no_content_type:
                headers.update({'Content-Type': content_type})

        return headers

    def _get_icptoken(self):
        return self.service_instance._create_token()

    def _is_default_space_set(self):
        if self.default_space_id is not None:
            return True
        return False

    def _is_IAM(self):
        if('apikey' in self.wml_credentials.keys()):
            if (self.wml_credentials['apikey'] != ''):
                return True
            else:
                raise WMLClientError('apikey value cannot be \'\'. Pass a valid apikey for IAM token.')

        else:
            return False