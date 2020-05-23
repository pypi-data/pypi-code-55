from localstack.utils.aws import aws_models
pvywi=super
pvywV=None
pvywf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pvywi(LambdaLayer,self).__init__(arn)
  self.cwd=pvywV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,pvywf,env=pvywV):
  pvywi(RDSDatabase,self).__init__(pvywf,env=env)
 def name(self):
  return self.pvywf.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
