from localstack.utils.aws import aws_models
mlfes=super
mlfek=None
mlfeD=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mlfes(LambdaLayer,self).__init__(arn)
  self.cwd=mlfek
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,mlfeD,env=mlfek):
  mlfes(RDSDatabase,self).__init__(mlfeD,env=env)
 def name(self):
  return self.mlfeD.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
