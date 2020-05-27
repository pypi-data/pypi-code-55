"""
"""
import boto3
from datascientist.special.s3session import check_bucket
from datascientist.workflow.tracker import s3_isfile
import yaml
import pickle
import subprocess
import logging
import json
from pathlib import Path

logger = logging.getLogger('training_job')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

HM = str(Path.home())

def configure_access(bucket, cluster, region):
	"""
	"""
	
	if check_bucket(bucket):
		logger.info("It appears that AWS credentials are already set")
	else:
		logger.info("Attempting to set AWS credentials")
		try:
			subprocess.run(["aws", "configure", "set", "aws_access_key_id" "$AWS_ACCESS_KEY_ID"])
			subprocess.run(["aws", "configure", "set", "aws_secret_access_key" "$AWS_SECRET_ACCESS_KEY"])
		except Exception as e:
			logging.error("Exception {} occurred".format(e), exc_info=True)
	try:
		cdict = yaml.load(open("{}/.kube/config".format(HM), "r"), Loader=yaml.BaseLoader)
		contexts = cdict['contexts']
		notfound = True
		for context in contexts:
			if cluster in context['name'] and "@" in context['name']:
				subprocess.run(['kubectl', 'config', 'use-context', context['name']])
				logger.info("Set the kubernetes config to use the {} context".format(cluster))
				notfound = False
		if notfound:
			logger.info("Couldn't find the {} cluster in the config... setting it up now.".format(cluster))
			subprocess.run(['aws', 'eks', '--region', region, 'update-kubeconfig', '--name', cluster])
			logger.info("Set the kubernetes config to use the {} context".format(cluster))

	except FileNotFoundError:
		logger.info("Attempting to configure kubectl to work with our cluster")
		subprocess.run(['aws', 'eks', '--region', region, 'update-kubeconfig', '--name', cluster])
		logger.info("Set the kubernetes config to use the {} context".format(cluster))

	return

with open("/tmp/blank_training_job_spec", "r") as file:
	JOB = file.read()

class Trainer:
	"""
	"""
	def __init__(
		self,
		name,
		bucket,
		image_tag,
		mem_guarantee='65G',
		mem_limit='124G',
		cluster_name='cdse-demo',
		region='us-east-2',
		repo="cloudframedotio/trainers"
		):
		"""
		"""
		self.name = name
		self.bucket = bucket
		self.image_tag = image_tag
		self.cluster_name = cluster_name
		self.region = region
		configure_access(bucket, cluster_name, region)
		self.bucket_obj = boto3.resource('s3').Bucket(bucket)
		self.repo = repo
		self.model_location = None
		self.mem_guarantee = mem_guarantee
		self.mem_limit = mem_limit

	def store_params(self, params):
		"""
		"""
		name = self.name
		bucket_obj = self.bucket_obj
		bucket = self.bucket
		filename = "params/{}_params.json".format(name)
		if s3_isfile(filename, bucket_obj):
			logger.warning("It looks like the hyperparameters file already exists.  It's being overwritten.")
			logger.warning("The old file can be accessed at params/{0}_params_old.json on the {1} bucket".format(name, bucket))
			bucket_obj.download_file(Key=filename, Filename="/tmp/{}_params_old.json".format(name))
			bucket_obj.upload_file(Filename="/tmp/{}_params_old.json".format(name), Key="params/{}_params_old.json".format(name))
		json.dump(params, open("/tmp/{}_params.json".format(name), "w"), indent=4)
		bucket_obj.upload_file(Filename="/tmp/{}_params.json".format(name), Key=filename)
		logger.info("Params uploaded to {0} on bucket {1}".format(filename, bucket))
		return filename

	def fetch_model(self, filename):
		"""
		"""
		mod_location = self.model_location
		bucket_obj = self.bucket_obj

		if mod_location is None:
			logger.info("no model location yet for this job")
			return
		if s3_isfile(mod_location, self.bucket_obj):
			bucket_obj.download_file(Key=mod_location, Filename=filename)
			model = pickle.load(open(filename, "rb"))
		else:
			logger.info("the model isn't at {}... give it more time to be written".format(mod_location))
			return
		return model

	def run_job(
		self,
		algorithm,
		hyperparameters,
		scoring,
		x_data,
		y_data,
		parts=None,
		cv=5,
		n_jobs=1
		):
		"""
		"""
		image = "{0}:{1}".format(self.repo, self.image_tag)
		params = self.store_params(hyperparameters)
		name = self.name
		bucket = self.bucket
		mem_guarantee = self.mem_guarantee
		mem_limit = self.mem_limit

		commands = [
			"python",
			"/tmp/training_utility.py",
			"-a={}".format(algorithm),
			"-b={}".format(bucket),
			"-p={}".format(params),
			"-s={}".format(scoring),
			"-x={}".format(x_data),
			"-y={}".format(y_data),
			"-t={}".format(parts),
			"-c={}".format(cv),
			"-n={}".format(n_jobs),
			"-m={}".format(name)
		]
		this_job = JOB.format(name, image, mem_guarantee, mem_limit, commands)
		js_name = "/tmp/jobspec_{}.yaml".format(name)
		with open(js_name, "w") as file:
			file.write(this_job)
		logger.info("Wrote job podspec to {}".format(js_name))
		job_cmd = ["kubectl", "apply", "-f", js_name, "-n", "jhub"]
		run_apply = subprocess.run(job_cmd, capture_output=True)
		logger.info("Applied the job with {} status".format(run_apply.stdout))
		logger.info("The model object will be stored in {0}/models/{1}.pkl".format(bucket, name))
		self.model_location = "models/{0}.pkl".format(name)
		return