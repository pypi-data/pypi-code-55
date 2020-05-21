from localstack.utils.aws import aws_models
bcBXU=super
bcBXa=None
bcBXH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bcBXU(LambdaLayer,self).__init__(arn)
  self.cwd=bcBXa
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,bcBXH,env=bcBXa):
  bcBXU(RDSDatabase,self).__init__(bcBXH,env=env)
 def name(self):
  return self.bcBXH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
