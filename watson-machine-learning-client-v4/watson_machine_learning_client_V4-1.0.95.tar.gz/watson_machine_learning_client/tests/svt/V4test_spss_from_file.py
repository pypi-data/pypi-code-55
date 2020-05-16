import unittest
from watson_machine_learning_client.utils.log_util import get_logger
from preparation_and_cleaning import *


class TestWMLClientWithSPSS(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    scoring_url = None
    scoring_uid = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestWMLClientWithSPSS.logger.info("Service Instance: setting up credentials")
        self.wml_credentials = get_wml_credentials()
        self.client = get_client()
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'customer-satisfaction-prediction.str')

    def test_01_service_instance_details(self):
        TestWMLClientWithSPSS.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        TestWMLClientWithSPSS.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()
        TestWMLClientWithSPSS.logger.debug(details)

        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_02_publish_local_model_in_repository(self):
        TestWMLClientWithSPSS.logger.info("Saving trained model in repo ...")
        TestWMLClientWithSPSS.logger.debug("Model path: {}".format(self.model_path))

        self.client.repository.ModelMetaNames.show()

        model_meta_props = {self.client.repository.ModelMetaNames.NAME: "LOCALLY created agaricus prediction model",
                       self.client.repository.ModelMetaNames.TYPE: "spss-modeler_18.1",
                       self.client.repository.ModelMetaNames.RUNTIME_UID: "spss-modeler_18.1"
                            }
        published_model = self.client.repository.store_model(model=self.model_path, meta_props=model_meta_props)
        TestWMLClientWithSPSS.model_uid = self.client.repository.get_model_uid(published_model)
        TestWMLClientWithSPSS.logger.info("Published model ID:" + str(TestWMLClientWithSPSS.model_uid))
        self.assertIsNotNone(TestWMLClientWithSPSS.model_uid)

    def test_03_load_model(self):
        TestWMLClientWithSPSS.logger.info("Load model from repository: {}".format(TestWMLClientWithSPSS.model_uid))
        self.tf_model = self.client.repository.load(TestWMLClientWithSPSS.model_uid)
        TestWMLClientWithSPSS.logger.debug("SPSS type: {}".format(type(self.tf_model)))
        self.assertTrue(self.tf_model)

    def test_04_get_details(self):
        TestWMLClientWithSPSS.logger.info("Get details")
        self.assertIsNotNone(self.client.repository.get_details(TestWMLClientWithSPSS.model_uid))

    def test_05_get_model_details(self):
        TestWMLClientWithSPSS.logger.info("Get model details")
        self.assertIsNotNone(self.client.repository.get_model_details(TestWMLClientWithSPSS.model_uid))

    def test_07_create_deployment(self):
        TestWMLClientWithSPSS.logger.info("Create deployment")
        deployment_details = self.client.deployments.create(TestWMLClientWithSPSS.model_uid, meta_props={self.client.deployments.ConfigurationMetaNames.NAME: "Test deployment",self.client.deployments.ConfigurationMetaNames.ONLINE:{}})

        TestWMLClientWithSPSS.logger.debug("Deployment details: {}".format(deployment_details))

        TestWMLClientWithSPSS.deployment_uid = self.client.deployments.get_uid(deployment_details)
        TestWMLClientWithSPSS.logger.debug("Deployment uid: {}".format(TestWMLClientWithSPSS.deployment_uid))

        TestWMLClientWithSPSS.scoring_url = self.client.deployments.get_scoring_href(deployment_details)
        TestWMLClientWithSPSS.logger.debug("Scoring url: {}".format(TestWMLClientWithSPSS.scoring_url))

        self.assertTrue('online' in str(deployment_details))

    def test_08_get_deployment_details(self):
        TestWMLClientWithSPSS.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details(deployment_uid=TestWMLClientWithSPSS.deployment_uid)
        self.assertIsNotNone(deployment_details)

    def test_09_scoring(self):
        TestWMLClientWithSPSS.logger.info("Score the model")
        scoring_payload = {
            self.client.deployments.ScoringMetaNames.INPUT_DATA: [
                {
                    "fields": ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
                               "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
                               "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
                               "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
                               "SampleWeight"],
                    "values":[["3638-WEABW","Female",0,"Yes","No",58,"Yes","Yes","DSL","No","Yes","No","Yes","No","No","Two year","Yes","Credit card (automatic)",59.9,3505.1,"No",2.768]]
                }
            ]
        }

        scores = self.client.deployments.score(TestWMLClientWithSPSS.deployment_uid, scoring_payload)
        self.assertIsNotNone(scores)

    def test_10_delete_deployment(self):
        TestWMLClientWithSPSS.logger.info("Delete deployment")
        self.client.deployments.delete(TestWMLClientWithSPSS.deployment_uid)

    def test_11_delete_model(self):
        TestWMLClientWithSPSS.logger.info("Delete model")
        self.client.repository.delete(TestWMLClientWithSPSS.model_uid)


if __name__ == '__main__':
    unittest.main()
